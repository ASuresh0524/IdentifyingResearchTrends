"""
Statistical analysis and visualization module for DDW research trends.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import logging
from pathlib import Path
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from src.config import (
    PROCESSED_DATA_DIR,
    FIGURES_DIR,
    STATISTICAL_SIGNIFICANCE_LEVEL,
    COVID_START_DATE,
    FIGURE_DPI,
    FIGURE_FORMAT,
    COLOR_PALETTE
)

logger = logging.getLogger(__name__)

class TrendAnalyzer:
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the trend analyzer.
        
        Args:
            data (pd.DataFrame): Processed abstract data
        """
        self.data = data
        self.covid_date = datetime.strptime(COVID_START_DATE, '%Y-%m-%d')
        
    def analyze_temporal_trends(self) -> Dict:
        """
        Analyze trends over time.
        
        Returns:
            Dict: Dictionary containing temporal analysis results
        """
        # Convert presentation_date to datetime
        self.data['date'] = pd.to_datetime(self.data['presentation_date'])
        
        # Group by year and calculate metrics
        yearly_stats = self.data.groupby(self.data['date'].dt.year).agg({
            'abstract': 'count',
            'contains_covid': 'sum',
            'research_category': lambda x: x.value_counts().to_dict(),
            'geography': lambda x: x.value_counts().to_dict()
        }).reset_index()
        
        # Calculate year-over-year changes
        yearly_stats['yoy_change'] = yearly_stats['abstract'].pct_change()
        
        return yearly_stats.to_dict()
    
    def analyze_covid_impact(self) -> Dict:
        """
        Analyze the impact of COVID-19 on research trends.
        
        Returns:
            Dict: Dictionary containing COVID-19 impact analysis
        """
        # Split data into pre and post COVID periods
        pre_covid = self.data[self.data['date'] < self.covid_date]
        post_covid = self.data[self.data['date'] >= self.covid_date]
        
        # Perform statistical tests
        stats_results = {
            'pre_covid_count': len(pre_covid),
            'post_covid_count': len(post_covid),
            'covid_related_percentage': (post_covid['contains_covid'].sum() / len(post_covid)) * 100
        }
        
        # Compare research categories
        category_comparison = self._compare_distributions(
            pre_covid['research_category'],
            post_covid['research_category']
        )
        
        stats_results['category_changes'] = category_comparison
        
        return stats_results
    
    def analyze_geographical_distribution(self) -> Dict:
        """
        Analyze geographical distribution of research.
        
        Returns:
            Dict: Dictionary containing geographical analysis
        """
        # Calculate overall distribution
        geo_dist = self.data['geography'].value_counts()
        
        # Calculate temporal changes in distribution
        yearly_geo = self.data.groupby([self.data['date'].dt.year, 'geography']).size().unstack()
        
        return {
            'overall_distribution': geo_dist.to_dict(),
            'temporal_changes': yearly_geo.to_dict()
        }
    
    def create_visualizations(self):
        """Create and save visualizations of the analysis results."""
        # Set style
        plt.style.use('seaborn')
        sns.set_palette(COLOR_PALETTE)
        
        # 1. Temporal trends plot
        self._plot_temporal_trends()
        
        # 2. Research category distribution
        self._plot_category_distribution()
        
        # 3. COVID-19 impact visualization
        self._plot_covid_impact()
        
        # 4. Geographical distribution
        self._plot_geographical_distribution()
        
        # 5. Interactive trends dashboard
        self._create_interactive_dashboard()
    
    def _plot_temporal_trends(self):
        """Create and save temporal trends visualization."""
        plt.figure(figsize=(12, 6))
        
        # Plot total abstracts per year
        yearly_counts = self.data.groupby(self.data['date'].dt.year)['abstract'].count()
        
        plt.plot(yearly_counts.index, yearly_counts.values, marker='o')
        plt.title('Number of DDW Abstracts Over Time')
        plt.xlabel('Year')
        plt.ylabel('Number of Abstracts')
        plt.grid(True)
        
        # Save plot
        plt.savefig(FIGURES_DIR / f'temporal_trends.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
    
    def _plot_category_distribution(self):
        """Create and save research category distribution visualization."""
        plt.figure(figsize=(10, 8))
        
        # Create stacked bar chart of categories over time
        category_by_year = self.data.pivot_table(
            index=self.data['date'].dt.year,
            columns='research_category',
            aggfunc='size',
            fill_value=0
        )
        
        category_by_year.plot(kind='bar', stacked=True)
        plt.title('Research Categories Distribution Over Time')
        plt.xlabel('Year')
        plt.ylabel('Number of Abstracts')
        plt.legend(title='Research Category', bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        
        # Save plot
        plt.savefig(FIGURES_DIR / f'category_distribution.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
    
    def _plot_covid_impact(self):
        """Create and save COVID-19 impact visualization."""
        plt.figure(figsize=(12, 6))
        
        # Create timeline of COVID-related research
        covid_timeline = self.data.set_index('date')['contains_covid'].rolling('30D').mean()
        
        plt.plot(covid_timeline.index, covid_timeline.values)
        plt.axvline(x=self.covid_date, color='r', linestyle='--', label='COVID-19 Start')
        plt.title('Timeline of COVID-19 Related Research')
        plt.xlabel('Date')
        plt.ylabel('Proportion of COVID-related Abstracts (30-day moving average)')
        plt.legend()
        
        # Save plot
        plt.savefig(FIGURES_DIR / f'covid_impact.{FIGURE_FORMAT}', dpi=FIGURE_DPI)
        plt.close()
    
    def _plot_geographical_distribution(self):
        """Create and save geographical distribution visualization."""
        # Create world map visualization using plotly
        geo_counts = self.data['geography'].value_counts()
        
        fig = go.Figure(data=go.Choropleth(
            locations=geo_counts.index,
            z=geo_counts.values,
            locationmode='country names',
            colorscale='Viridis',
            colorbar_title='Number of Abstracts'
        ))
        
        fig.update_layout(
            title='Geographical Distribution of DDW Research',
            geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular'),
            width=1000,
            height=600
        )
        
        # Save plot
        fig.write_html(str(FIGURES_DIR / 'geographical_distribution.html'))
    
    def _create_interactive_dashboard(self):
        """Create an interactive dashboard using plotly."""
        # Create a combined dashboard
        fig = go.Figure()
        
        # 1. Time series of abstracts
        yearly_counts = self.data.groupby(self.data['date'].dt.year)['abstract'].count()
        fig.add_trace(go.Scatter(
            x=yearly_counts.index,
            y=yearly_counts.values,
            name='Total Abstracts',
            mode='lines+markers'
        ))
        
        # 2. COVID-related research
        covid_counts = self.data.groupby(self.data['date'].dt.year)['contains_covid'].sum()
        fig.add_trace(go.Scatter(
            x=covid_counts.index,
            y=covid_counts.values,
            name='COVID-related',
            mode='lines+markers'
        ))
        
        # Update layout
        fig.update_layout(
            title='DDW Research Trends Dashboard',
            xaxis_title='Year',
            yaxis_title='Number of Abstracts',
            hovermode='x unified',
            width=1200,
            height=800
        )
        
        # Save dashboard
        fig.write_html(str(FIGURES_DIR / 'interactive_dashboard.html'))
    
    def _compare_distributions(self, pre: pd.Series, post: pd.Series) -> Dict:
        """
        Compare two distributions using statistical tests.
        
        Args:
            pre (pd.Series): Pre-event distribution
            post (pd.Series): Post-event distribution
            
        Returns:
            Dict: Dictionary containing comparison results
        """
        # Calculate proportions
        pre_props = pre.value_counts(normalize=True)
        post_props = post.value_counts(normalize=True)
        
        # Perform chi-square test
        chi2, p_value = stats.chi2_contingency(
            pd.crosstab(pd.concat([pre, post]),
                       pd.concat([pd.Series(['pre']*len(pre)),
                                pd.Series(['post']*len(post))]))[:2]
        
        return {
            'pre_distribution': pre_props.to_dict(),
            'post_distribution': post_props.to_dict(),
            'chi2_statistic': chi2,
            'p_value': p_value,
            'significant_difference': p_value < STATISTICAL_SIGNIFICANCE_LEVEL
        } 
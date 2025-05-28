"""
Tests for the trend analyzer module.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from src.analysis.trend_analyzer import TrendAnalyzer
from src.config import COVID_START_DATE

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    dates = pd.date_range(start='2019-01-01', end='2021-12-31', freq='M')
    n_samples = len(dates)
    
    return pd.DataFrame({
        'date': dates,
        'presentation_date': dates.strftime('%Y-%m-%d'),
        'abstract': [f'Abstract {i}' for i in range(n_samples)],
        'contains_covid': [1 if d >= datetime.strptime(COVID_START_DATE, '%Y-%m-%d') else 0 
                         for d in dates],
        'research_category': np.random.choice(
            ['clinical_trial', 'observational', 'basic_science'],
            size=n_samples
        ),
        'geography': np.random.choice(
            ['USA', 'UK', 'China', 'Germany'],
            size=n_samples
        )
    })

@pytest.fixture
def analyzer(sample_data):
    """Create a TrendAnalyzer instance with sample data."""
    return TrendAnalyzer(sample_data)

def test_analyze_temporal_trends(analyzer):
    """Test temporal trends analysis."""
    trends = analyzer.analyze_temporal_trends()
    
    assert 'abstract' in trends
    assert 'contains_covid' in trends
    assert 'research_category' in trends
    assert 'geography' in trends
    assert 'yoy_change' in trends

def test_analyze_covid_impact(analyzer):
    """Test COVID-19 impact analysis."""
    impact = analyzer.analyze_covid_impact()
    
    assert 'pre_covid_count' in impact
    assert 'post_covid_count' in impact
    assert 'covid_related_percentage' in impact
    assert 'category_changes' in impact
    
    # Verify that pre and post counts sum to total
    total_count = len(analyzer.data)
    assert impact['pre_covid_count'] + impact['post_covid_count'] == total_count

def test_analyze_geographical_distribution(analyzer):
    """Test geographical distribution analysis."""
    geo_dist = analyzer.analyze_geographical_distribution()
    
    assert 'overall_distribution' in geo_dist
    assert 'temporal_changes' in geo_dist
    
    # Check if all countries are present in distribution
    countries = set(analyzer.data['geography'].unique())
    assert all(country in geo_dist['overall_distribution'] for country in countries)

def test_compare_distributions(analyzer):
    """Test distribution comparison functionality."""
    pre = pd.Series(['A', 'A', 'B', 'C'])
    post = pd.Series(['A', 'B', 'B', 'B'])
    
    comparison = analyzer._compare_distributions(pre, post)
    
    assert 'pre_distribution' in comparison
    assert 'post_distribution' in comparison
    assert 'chi2_statistic' in comparison
    assert 'p_value' in comparison
    assert 'significant_difference' in comparison
    
    # Check if proportions sum to 1
    assert abs(sum(comparison['pre_distribution'].values()) - 1.0) < 1e-10
    assert abs(sum(comparison['post_distribution'].values()) - 1.0) < 1e-10

def test_visualization_creation(analyzer, tmp_path):
    """Test visualization creation."""
    # Temporarily set the figures directory to a test directory
    import src.config as config
    original_figures_dir = config.FIGURES_DIR
    config.FIGURES_DIR = tmp_path
    
    try:
        analyzer.create_visualizations()
        
        # Check if visualization files were created
        expected_files = [
            'temporal_trends.png',
            'category_distribution.png',
            'covid_impact.png',
            'geographical_distribution.html',
            'interactive_dashboard.html'
        ]
        
        for file in expected_files:
            assert (tmp_path / file).exists()
    
    finally:
        # Restore original figures directory
        config.FIGURES_DIR = original_figures_dir 
"""
Data preprocessing module for DDW abstracts.
Handles data cleaning, formatting, and feature extraction.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Union, Tuple
import re
import logging
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import requests

from src.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    YEARS_TO_ANALYZE,
    DDW_BASE_URL
)

logger = logging.getLogger(__name__)

class DDWDataProcessor:
    def __init__(self):
        """Initialize the DDW data processor."""
        self.raw_data_dir = RAW_DATA_DIR
        self.processed_data_dir = PROCESSED_DATA_DIR
        
    def fetch_abstracts(self, year: int) -> pd.DataFrame:
        """
        Fetch abstracts from DDW website for a specific year.
        
        Args:
            year (int): Year to fetch abstracts for
            
        Returns:
            pd.DataFrame: DataFrame containing the fetched abstracts
        """
        logger.info(f"Fetching abstracts for year {year}")
        
        # Implement web scraping logic here
        # This is a placeholder - actual implementation would depend on DDW website structure
        url = f"{DDW_BASE_URL}/{year}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse the HTML and extract abstract information
            soup = BeautifulSoup(response.text, 'html.parser')
            abstracts = self._parse_abstracts(soup)
            
            # Convert to DataFrame
            df = pd.DataFrame(abstracts)
            
            # Save raw data
            raw_file = self.raw_data_dir / f"ddw_abstracts_{year}.csv"
            df.to_csv(raw_file, index=False)
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching abstracts for {year}: {str(e)}")
            return pd.DataFrame()
    
    def process_abstracts(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process raw abstract data.
        
        Args:
            df (pd.DataFrame): Raw abstract data
            
        Returns:
            pd.DataFrame: Processed abstract data
        """
        # Clean text
        df['clean_abstract'] = df['abstract'].apply(self._clean_text)
        
        # Extract features
        df['word_count'] = df['clean_abstract'].apply(lambda x: len(x.split()))
        df['contains_covid'] = df['clean_abstract'].apply(
            lambda x: 1 if re.search(r'covid|sars-cov-2|coronavirus', x.lower()) else 0
        )
        
        # Extract research categories
        df['research_category'] = df['clean_abstract'].apply(self._categorize_research)
        
        # Extract geographical information
        df['geography'] = df['author_affiliation'].apply(self._extract_geography)
        
        return df
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text data.
        
        Args:
            text (str): Raw text
            
        Returns:
            str: Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def _categorize_research(self, abstract: str) -> str:
        """
        Categorize research based on abstract content.
        
        Args:
            abstract (str): Abstract text
            
        Returns:
            str: Research category
        """
        # Implement logic to categorize research
        # This is a simple example - expand based on your needs
        categories = {
            'clinical_trial': r'trial|randomized|placebo',
            'observational': r'cohort|retrospective|prospective',
            'basic_science': r'vitro|vivo|molecular|cellular',
            'meta_analysis': r'meta-analysis|systematic review',
            'case_study': r'case report|case series'
        }
        
        for category, pattern in categories.items():
            if re.search(pattern, abstract.lower()):
                return category
                
        return 'other'
    
    def _extract_geography(self, affiliation: str) -> str:
        """
        Extract geographical information from author affiliation.
        
        Args:
            affiliation (str): Author affiliation text
            
        Returns:
            str: Extracted geography
        """
        # Implement geography extraction logic
        # This is a placeholder - expand based on your needs
        return affiliation.split(',')[-1].strip()
    
    def _parse_abstracts(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parse abstracts from HTML content.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            
        Returns:
            List[Dict]: List of abstract dictionaries
        """
        # Implement parsing logic based on DDW website structure
        # This is a placeholder - actual implementation would depend on site structure
        abstracts = []
        
        # Example structure - modify based on actual HTML structure
        abstract_elements = soup.find_all('div', class_='abstract')
        
        for element in abstract_elements:
            abstract = {
                'title': element.find('h2').text.strip(),
                'abstract': element.find('div', class_='content').text.strip(),
                'author': element.find('div', class_='author').text.strip(),
                'author_affiliation': element.find('div', class_='affiliation').text.strip(),
                'presentation_date': element.find('div', class_='date').text.strip()
            }
            abstracts.append(abstract)
            
        return abstracts
    
    def process_all_years(self) -> pd.DataFrame:
        """
        Process abstracts for all years in the analysis range.
        
        Returns:
            pd.DataFrame: Combined processed data for all years
        """
        all_data = []
        
        for year in YEARS_TO_ANALYZE:
            logger.info(f"Processing year {year}")
            
            # Check if processed file exists
            processed_file = self.processed_data_dir / f"processed_abstracts_{year}.csv"
            
            if processed_file.exists():
                df = pd.read_csv(processed_file)
            else:
                # Fetch and process new data
                raw_df = self.fetch_abstracts(year)
                df = self.process_abstracts(raw_df)
                
                # Save processed data
                df.to_csv(processed_file, index=False)
            
            all_data.append(df)
        
        # Combine all years
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Save combined dataset
        combined_file = self.processed_data_dir / "all_abstracts_processed.csv"
        combined_df.to_csv(combined_file, index=False)
        
        return combined_df 
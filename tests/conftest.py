"""
Pytest configuration file with common fixtures.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import shutil
import tempfile

@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="session")
def sample_raw_data():
    """Create sample raw data for testing."""
    return pd.DataFrame({
        'title': [
            'COVID-19 Study',
            'Endoscopy Techniques',
            'IBD Research'
        ],
        'abstract': [
            'Study about COVID-19 impact on GI procedures',
            'Novel endoscopic techniques for detection',
            'Investigation of IBD treatments'
        ],
        'author': [
            'John Smith',
            'Jane Doe',
            'Bob Johnson'
        ],
        'author_affiliation': [
            'Harvard University, USA',
            'Oxford University, UK',
            'Tokyo University, Japan'
        ],
        'presentation_date': [
            '2021-05-01',
            '2020-06-01',
            '2019-05-15'
        ]
    })

@pytest.fixture(scope="session")
def sample_processed_data(sample_raw_data):
    """Create sample processed data for testing."""
    df = sample_raw_data.copy()
    
    # Add processed columns
    df['clean_abstract'] = df['abstract'].str.lower()
    df['word_count'] = df['abstract'].str.split().str.len()
    df['contains_covid'] = df['abstract'].str.contains('covid', case=False).astype(int)
    df['research_category'] = ['clinical_trial', 'observational', 'basic_science']
    df['geography'] = df['author_affiliation'].str.split(',').str[-1].str.strip()
    
    return df

@pytest.fixture(scope="session")
def mock_config():
    """Create mock configuration for testing."""
    class MockConfig:
        STATISTICAL_SIGNIFICANCE_LEVEL = 0.05
        COVID_START_DATE = "2020-03-01"
        FIGURE_DPI = 100
        FIGURE_FORMAT = "png"
        COLOR_PALETTE = "viridis"
    
    return MockConfig()

@pytest.fixture(scope="function")
def temp_output_dir():
    """Create a temporary directory for test outputs."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="session")
def sample_trend_data():
    """Create sample trend data for testing."""
    np.random.seed(42)
    n_samples = 100
    
    return {
        'temporal_trends': {
            'year': list(range(2018, 2024)),
            'abstract_count': np.random.randint(100, 1000, 6).tolist(),
            'covid_related': [0, 0, 50, 200, 150, 100]
        },
        'covid_impact': {
            'pre_covid_count': 1500,
            'post_covid_count': 2000,
            'covid_related_percentage': 25.5
        },
        'geographical_distribution': {
            'USA': 500,
            'UK': 300,
            'China': 250,
            'Germany': 200,
            'Japan': 150
        }
    } 
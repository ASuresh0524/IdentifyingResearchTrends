"""
Tests for the DDW data processor module.
"""

import pytest
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from src.preprocessing.data_processor import DDWDataProcessor

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'title': ['Sample Abstract 1', 'Sample Abstract 2'],
        'abstract': [
            'A clinical trial study about COVID-19 treatment',
            'An observational study about patient outcomes'
        ],
        'author': ['John Doe', 'Jane Smith'],
        'author_affiliation': ['Stanford University, USA', 'Oxford University, UK'],
        'presentation_date': ['2020-05-01', '2019-06-01']
    })

@pytest.fixture
def processor():
    """Create a DDWDataProcessor instance."""
    return DDWDataProcessor()

def test_clean_text(processor):
    """Test text cleaning functionality."""
    text = "This is a TEST with special chars: @#$%"
    cleaned = processor._clean_text(text)
    assert cleaned == "this is a test with special chars"
    assert cleaned.islower()

def test_categorize_research(processor):
    """Test research categorization."""
    clinical_trial = "This is a randomized controlled trial"
    observational = "A retrospective cohort study"
    basic_science = "In vitro examination of cells"
    
    assert processor._categorize_research(clinical_trial) == "clinical_trial"
    assert processor._categorize_research(observational) == "observational"
    assert processor._categorize_research(basic_science) == "basic_science"

def test_extract_geography(processor):
    """Test geography extraction."""
    affiliation = "Department of Medicine, Stanford University, USA"
    assert processor._extract_geography(affiliation) == "USA"

def test_process_abstracts(processor, sample_data):
    """Test abstract processing pipeline."""
    processed_df = processor.process_abstracts(sample_data)
    
    # Check if all expected columns are present
    expected_columns = [
        'title', 'abstract', 'author', 'author_affiliation', 
        'presentation_date', 'clean_abstract', 'word_count',
        'contains_covid', 'research_category', 'geography'
    ]
    assert all(col in processed_df.columns for col in expected_columns)
    
    # Check COVID detection
    assert processed_df.loc[0, 'contains_covid'] == 1
    assert processed_df.loc[1, 'contains_covid'] == 0
    
    # Check word count calculation
    assert processed_df['word_count'].all() > 0

def test_parse_abstracts(processor):
    """Test HTML parsing functionality."""
    # Create a sample HTML structure
    html = """
    <div class="abstract">
        <h2>Sample Title</h2>
        <div class="content">Abstract content</div>
        <div class="author">Author Name</div>
        <div class="affiliation">University, Country</div>
        <div class="date">2023-01-01</div>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')
    abstracts = processor._parse_abstracts(soup)
    
    assert len(abstracts) == 1
    assert abstracts[0]['title'] == "Sample Title"
    assert abstracts[0]['abstract'] == "Abstract content" 
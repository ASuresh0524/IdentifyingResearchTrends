# Data Format Documentation

This document describes the format of the data files used in the DDW Research Trends Analysis project.

## Raw Data Format

The raw data is stored in CSV files in the `data/raw` directory, with one file per year (e.g., `sample_abstract_2023.csv`). Each file contains the following columns:

### Columns

1. **title** (string)
   - The title of the research abstract
   - Example: "Impact of COVID-19 on GI Procedures"

2. **abstract** (string)
   - The full text of the research abstract
   - Contains the main content, including background, methods, results, and conclusions
   - Example: "This study examines the impact of the COVID-19 pandemic..."

3. **author** (string)
   - Name of the primary author
   - Format: "First Last"
   - Example: "Sarah Johnson"

4. **author_affiliation** (string)
   - Institution and country of the primary author
   - Format: "Institution, Country"
   - Example: "Mayo Clinic, USA"

5. **presentation_date** (string)
   - Date of the presentation at DDW
   - Format: "YYYY-MM-DD"
   - Example: "2023-05-15"

## Processed Data Format

After processing, additional columns are added to the data:

1. **clean_abstract** (string)
   - Preprocessed version of the abstract text
   - Lowercase, special characters removed, standardized spacing

2. **word_count** (integer)
   - Number of words in the abstract

3. **contains_covid** (integer)
   - Binary flag (0/1) indicating if the abstract is COVID-19 related

4. **research_category** (string)
   - Categorization of the research type
   - Values: clinical_trial, observational, basic_science, meta_analysis, case_study, other

5. **geography** (string)
   - Extracted country from author affiliation

## Analysis Results Format

Analysis results are stored in JSON format with the following structure:

```json
{
    "temporal_trends": {
        "year": [...],
        "abstract_count": [...],
        "covid_related": [...],
        "categories": {...},
        "geography": {...}
    },
    "covid_impact": {
        "pre_covid_count": int,
        "post_covid_count": int,
        "covid_related_percentage": float,
        "category_changes": {...}
    },
    "geographical_distribution": {
        "overall_distribution": {...},
        "temporal_changes": {...}
    }
}
```

## File Naming Conventions

- Raw data files: `ddw_abstracts_YYYY.csv`
- Processed data files: `processed_abstracts_YYYY.csv`
- Combined processed data: `all_abstracts_processed.csv`
- Analysis results: `analysis_results_YYYYMMDD.json`

## Data Quality Guidelines

1. All dates should be in ISO format (YYYY-MM-DD)
2. No missing values allowed in required fields (title, abstract, author, affiliation, date)
3. Abstract text should be in English
4. Author affiliations should include both institution and country
5. Special characters in text should be properly encoded 
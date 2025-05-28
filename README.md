# Analyzing Research Trends in Digestive Disease Week Publications

## Project Overview
This research project analyzes gastrointestinal (GI) publications from Digestive Disease Week (DDW) conferences over the past 5-6 years. The study focuses on:
- Tracking changes in abstract publications
- Analyzing the impact of COVID-19 on research trends
- Utilizing GPC-4 Neural Network for data analysis
- Identifying patterns and trends in gastroenterology research

## Repository Structure
```
.
├── data/
│   ├── raw/                  # Original DDW abstract datasets
│   └── processed/            # Cleaned and processed datasets
├── src/
│   ├── preprocessing/        # Data cleaning and preparation scripts
│   ├── analysis/            # Statistical analysis scripts
│   ├── visualization/       # Data visualization code
│   └── models/              # GPC-4 Neural Network implementation
├── tests/                   # Unit tests and integration tests
├── docs/                    # Documentation and research notes
│   └── figures/            # Generated figures and visualizations
└── requirements/           # Project dependencies
```

## Setup Instructions
1. Clone the repository
```bash
git clone https://github.com/yourusername/IdentifyingResearchTrends.git
cd IdentifyingResearchTrends
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements/requirements.txt
```

## Data Collection
The project analyzes DDW publications from 2018-2023, focusing on:
- Abstract submissions
- Research categories
- Author demographics
- COVID-19 related research
- Geographic distribution

## Analysis Pipeline
1. Data Extraction: Automated scraping of DDW abstracts
2. Preprocessing: Cleaning and standardizing data
3. Neural Network Analysis: GPC-4 implementation for trend identification
4. Statistical Analysis: Multi-variable statistical analysis
5. Visualization: Generation of figures and trends.

## Authors
- Aakash Suresh 
- Dr. John Clarke 

## Acknowledgments
- Stanford University
- DDW Conference Organization
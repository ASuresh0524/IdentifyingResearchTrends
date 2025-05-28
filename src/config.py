"""
Configuration file for the DDW Research Trends Analysis project.
Contains paths, parameters, and settings used across the project.
"""

import os
from pathlib import Path

# Base paths
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = ROOT_DIR / "src" / "models"
FIGURES_DIR = ROOT_DIR / "docs" / "figures"

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, MODELS_DIR, FIGURES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Data collection parameters
YEARS_TO_ANALYZE = range(2018, 2024)
DDW_BASE_URL = "https://ddw.org/abstracts/"  # Example URL, replace with actual

# Model parameters
GPC4_CONFIG = {
    "model_name": "gpc4-research-assistant",
    "batch_size": 32,
    "learning_rate": 1e-4,
    "epochs": 100,
    "validation_split": 0.2,
}

# Analysis parameters
STATISTICAL_SIGNIFICANCE_LEVEL = 0.05
COVID_START_DATE = "2020-03-01"

# Visualization settings
FIGURE_DPI = 300
FIGURE_FORMAT = "png"
COLOR_PALETTE = "viridis"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" 
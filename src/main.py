"""
Main script for running the DDW research trends analysis pipeline.
"""

import logging
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

from src.preprocessing.data_processor import DDWDataProcessor
from src.models.gpc4_model import GPC4ResearchAssistant, load_pretrained_model
from src.analysis.trend_analyzer import TrendAnalyzer
from src.config import PROCESSED_DATA_DIR, MODELS_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('ddw_analysis.log')
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Run the complete analysis pipeline."""
    try:
        logger.info("Starting DDW research trends analysis pipeline")
        
        # Initialize data processor
        processor = DDWDataProcessor()
        
        # Process all years of data
        logger.info("Processing abstract data")
        processed_data = processor.process_all_years()
        
        # Load and apply GPC-4 model
        logger.info("Applying GPC-4 model for trend analysis")
        model = load_pretrained_model()
        
        # Analyze trends in batches
        abstracts = processed_data['clean_abstract'].tolist()
        trend_results = model.batch_analyze(abstracts)
        
        # Add model results to processed data
        processed_data['trend_analysis'] = trend_results
        
        # Perform statistical analysis
        logger.info("Performing statistical analysis")
        analyzer = TrendAnalyzer(processed_data)
        
        # Generate analysis results
        temporal_trends = analyzer.analyze_temporal_trends()
        covid_impact = analyzer.analyze_covid_impact()
        geo_distribution = analyzer.analyze_geographical_distribution()
        
        # Create visualizations
        logger.info("Generating visualizations")
        analyzer.create_visualizations()
        
        # Save analysis results
        results = {
            'temporal_trends': temporal_trends,
            'covid_impact': covid_impact,
            'geographical_distribution': geo_distribution
        }
        
        # Save results to JSON
        output_file = PROCESSED_DATA_DIR / f'analysis_results_{datetime.now().strftime("%Y%m%d")}.json'
        pd.DataFrame(results).to_json(output_file)
        
        logger.info(f"Analysis complete. Results saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Error in analysis pipeline: {str(e)}", exc_info=True)
        raise
    
if __name__ == "__main__":
    main() 
"""
Factory for creating TikTok data sources.

This module provides a factory for creating different types of data sources
based on configuration.
"""

from typing import Optional
from tiktok_analyzer.api.data_sources.base_data_source import BaseDataSource
from tiktok_analyzer.api.data_sources.tiktok_api_source import TikTokApiSource
from tiktok_analyzer.api.data_sources.csv_data_source import CSVDataSource
from tiktok_analyzer.api.data_sources.mock_data_source import MockDataSource
from tiktok_analyzer.utils.config import Config
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class DataSourceFactory:
    """Factory for creating TikTok data sources."""
    
    @staticmethod
    def create_data_source(data_source_type: Optional[str] = None) -> BaseDataSource:
        """
        Create a data source based on the specified type or configuration.
        
        Args:
            data_source_type: Type of data source to create ('api', 'csv', 'mock', or None)
                If None, the data source will be determined from the configuration.
                
        Returns:
            An instance of a data source
        """
        if data_source_type is None:
            config = Config.get_data_source_config()
            data_source_type = config.get('type', 'mock')
        
        logger.info(f"Creating data source of type: {data_source_type}")
        
        try:
            if data_source_type.lower() == "api":
                return TikTokApiSource()
            elif data_source_type.lower() == "csv":
                return CSVDataSource()
            elif data_source_type.lower() == "mock":
                return MockDataSource()
            else:
                logger.warning(f"Unknown data source type: {data_source_type}, falling back to mock data")
                return MockDataSource()
        except Exception as e:
            logger.error(f"Failed to create data source {data_source_type}: {str(e)}")
            logger.info("Falling back to mock data source")
            return MockDataSource()

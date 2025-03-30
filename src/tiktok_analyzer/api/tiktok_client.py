"""
TikTok client for accessing TikTok data.

This module provides a client for interacting with TikTok data sources
to retrieve data about users, videos, and trends.
"""

import os
from typing import List, Dict, Any, Optional
from tiktok_analyzer.api.data_sources.data_source_factory import DataSourceFactory
from tiktok_analyzer.utils.config import Config
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class TikTokClient:
    """
    Client for interacting with TikTok data sources.
    
    This client provides a unified interface for retrieving TikTok data
    from different sources, such as the TikTok API, CSV files, or mock data.
    """
    
    def __init__(self, data_source_type: Optional[str] = None):
        """
        Initialize the TikTok client.
        
        Args:
            data_source_type: Type of data source to use ('api', 'csv', 'mock', or None)
                If None, the data source will be determined from the configuration.
        """
        self.data_source = DataSourceFactory.create_data_source(data_source_type)
        logger.info(f"TikTok client initialized with data source: {type(self.data_source).__name__}")
    
    def get_trending_users(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        Get trending TikTok users.
        
        Args:
            count: Number of trending users to retrieve (default: 100)
            
        Returns:
            List of user dictionaries with standardized fields
        """
        try:
            users = self.data_source.get_trending_users(count)
            logger.info(f"Retrieved {len(users)} trending users")
            return users
        except Exception as e:
            logger.error(f"Error getting trending users: {str(e)}")
            return []
    
    def get_user_videos(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get videos from a specific user.
        
        Args:
            username: TikTok username
            limit: Maximum number of videos to retrieve (default: 10)
            
        Returns:
            List of video dictionaries with standardized fields
        """
        try:
            videos = self.data_source.get_user_videos(username, limit)
            logger.info(f"Retrieved {len(videos)} videos for user {username}")
            return videos
        except Exception as e:
            logger.error(f"Error getting user videos for {username}: {str(e)}")
            return []
    
    def get_video_download_url(self, video_id: str) -> Optional[str]:
        """
        Get the download URL for a video.
        
        Args:
            video_id: TikTok video ID
            
        Returns:
            Video download URL or None if not found
        """
        try:
            url = self.data_source.get_video_download_url(video_id)
            if url:
                logger.info(f"Retrieved download URL for video {video_id}")
            else:
                logger.warning(f"No download URL found for video {video_id}")
            return url
        except Exception as e:
            logger.error(f"Error getting video download URL for {video_id}: {str(e)}")
            return None

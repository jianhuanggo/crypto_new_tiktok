"""
Base data source for TikTok influencer identification.

This module defines the base interface for all data sources.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseDataSource(ABC):
    """
    Abstract base class for TikTok data sources.
    
    All data sources must implement these methods to provide
    a consistent interface for retrieving TikTok influencer data.
    """
    
    @abstractmethod
    def get_trending_users(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        Get trending TikTok users.
        
        Args:
            count: Number of trending users to retrieve (default: 100)
            
        Returns:
            List of user dictionaries with standardized fields
        """
        pass
    
    @abstractmethod
    def get_user_videos(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get videos from a specific user.
        
        Args:
            username: TikTok username
            limit: Maximum number of videos to retrieve (default: 10)
            
        Returns:
            List of video dictionaries with standardized fields
        """
        pass
    
    @abstractmethod
    def get_video_download_url(self, video_id: str) -> str:
        """
        Get the download URL for a video.
        
        Args:
            video_id: TikTok video ID
            
        Returns:
            Video download URL or None if not found
        """
        pass

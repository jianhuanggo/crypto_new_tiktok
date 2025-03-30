"""
CSV data source for TikTok influencer identification.

This module provides a data source that uses CSV files
to retrieve data about TikTok influencers.
"""

import os
import csv
import json
from typing import List, Dict, Any
from tiktok_analyzer.api.data_sources.base_data_source import BaseDataSource
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class CSVDataSource(BaseDataSource):
    """
    Data source that uses CSV files.
    """
    
    def __init__(self, users_file: str = None, videos_file: str = None):
        """
        Initialize the CSV data source.
        
        Args:
            users_file: Path to the CSV file containing user data
            videos_file: Path to the CSV file containing video data
        """
        self.users_file = users_file or os.path.join('data', 'tiktok_users.csv')
        self.videos_file = videos_file or os.path.join('data', 'tiktok_videos.csv')
        
        self.users = self._load_users()
        self.videos = self._load_videos()
    
    def _load_users(self) -> Dict[str, Dict[str, Any]]:
        """
        Load user data from CSV file.
        
        Returns:
            Dictionary mapping usernames to user data
        """
        users = {}
        
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        username = row.get('username')
                        if username:
                            for field in ['follower_count', 'following_count', 'heart_count', 'video_count']:
                                if field in row:
                                    try:
                                        row[field] = int(row[field])
                                    except (ValueError, TypeError):
                                        row[field] = 0
                            
                            if 'verified' in row:
                                row['verified'] = row['verified'].lower() in ['true', '1', 'yes']
                            
                            users[username] = row
                
                logger.info(f"Loaded {len(users)} users from {self.users_file}")
            else:
                logger.warning(f"Users file not found: {self.users_file}")
        
        except Exception as e:
            logger.error(f"Error loading users from CSV: {str(e)}")
        
        return users
    
    def _load_videos(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load video data from CSV file.
        
        Returns:
            Dictionary mapping usernames to lists of video data
        """
        videos = {}
        
        try:
            if os.path.exists(self.videos_file):
                with open(self.videos_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        username = row.get('username')
                        if username:
                            for field in ['create_time', 'likes', 'comments', 'shares', 'views']:
                                if field in row:
                                    try:
                                        row[field] = int(row[field])
                                    except (ValueError, TypeError):
                                        row[field] = 0
                            
                            if username not in videos:
                                videos[username] = []
                            
                            videos[username].append(row)
                
                logger.info(f"Loaded videos for {len(videos)} users from {self.videos_file}")
            else:
                logger.warning(f"Videos file not found: {self.videos_file}")
        
        except Exception as e:
            logger.error(f"Error loading videos from CSV: {str(e)}")
        
        return videos
    
    def get_trending_users(self, count: int = 100) -> List[Dict[str, Any]]:
        """
        Get trending TikTok users.
        
        Args:
            count: Number of trending users to retrieve (default: 100)
            
        Returns:
            List of user dictionaries with standardized fields
        """
        sorted_users = sorted(
            self.users.values(),
            key=lambda x: x.get('follower_count', 0),
            reverse=True
        )
        
        return sorted_users[:count]
    
    def get_user_videos(self, username: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get videos from a specific user.
        
        Args:
            username: TikTok username
            limit: Maximum number of videos to retrieve (default: 10)
            
        Returns:
            List of video dictionaries with standardized fields
        """
        if username not in self.videos:
            logger.warning(f"No videos found for user: {username}")
            return []
        
        sorted_videos = sorted(
            self.videos[username],
            key=lambda x: x.get('create_time', 0),
            reverse=True
        )
        
        return sorted_videos[:limit]
    
    def get_video_download_url(self, video_id: str) -> str:
        """
        Get the download URL for a video.
        
        Args:
            video_id: TikTok video ID
            
        Returns:
            Video download URL or None if not found
        """
        for username, user_videos in self.videos.items():
            for video in user_videos:
                if video.get('id') == video_id:
                    return video.get('video_url')
        
        logger.warning(f"Video not found: {video_id}")
        return None

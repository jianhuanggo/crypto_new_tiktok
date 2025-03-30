"""
Mock data source for TikTok influencer identification.

This module provides a mock data source for testing and development
without requiring actual TikTok API access.
"""

import os
import json
import random
from typing import List, Dict, Any
from datetime import datetime, timedelta
from tiktok_analyzer.api.data_sources.base_data_source import BaseDataSource
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class MockDataSource(BaseDataSource):
    """
    Mock data source for testing and development.
    """
    
    def __init__(self, user_count: int = 100, videos_per_user: int = 10):
        """
        Initialize the mock data source.
        
        Args:
            user_count: Number of mock users to generate (default: 100)
            videos_per_user: Number of mock videos per user (default: 10)
        """
        self.user_count = user_count
        self.videos_per_user = videos_per_user
        
        self.users = self._generate_users()
        self.videos = self._generate_videos()
    
    def _generate_users(self) -> Dict[str, Dict[str, Any]]:
        """
        Generate mock user data.
        
        Returns:
            Dictionary mapping usernames to user data
        """
        users = {}
        
        for i in range(1, self.user_count + 1):
            username = f"tiktok_user_{i}"
            follower_count = random.randint(1000, 10000000)
            
            users[username] = {
                'username': username,
                'display_name': f"TikTok User {i}",
                'follower_count': follower_count,
                'following_count': random.randint(10, 1000),
                'heart_count': follower_count * random.randint(1, 10),
                'video_count': random.randint(10, 500),
                'verified': random.random() > 0.9,  # 10% chance of being verified
                'signature': f"This is a mock TikTok user {i}",
                'user_id': f"user_{i}",
                'sec_uid': f"sec_uid_{i}",
                'avatar_url': f"https://example.com/avatar_{i}.jpg"
            }
        
        logger.info(f"Generated {len(users)} mock users")
        return users
    
    def _generate_videos(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate mock video data.
        
        Returns:
            Dictionary mapping usernames to lists of video data
        """
        videos = {}
        
        for username, user in self.users.items():
            videos[username] = []
            
            for i in range(1, self.videos_per_user + 1):
                video_id = f"{username}_video_{i}"
                views = random.randint(1000, 1000000)
                
                days_ago = random.randint(0, 30)
                create_time = int((datetime.now() - timedelta(days=days_ago)).timestamp())
                
                videos[username].append({
                    'id': video_id,
                    'desc': f"This is a mock TikTok video {i} by {username}",
                    'create_time': create_time,
                    'likes': int(views * random.uniform(0.1, 0.5)),
                    'comments': int(views * random.uniform(0.01, 0.1)),
                    'shares': int(views * random.uniform(0.01, 0.05)),
                    'views': views,
                    'video_url': f"https://example.com/videos/{video_id}.mp4",
                    'username': username
                })
        
        logger.info(f"Generated videos for {len(videos)} mock users")
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

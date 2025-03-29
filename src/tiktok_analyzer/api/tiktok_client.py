"""
TikTok API client for accessing TikTok data.

This module provides a client for interacting with the TikTok API
to retrieve data about users, videos, and trends.
"""

import os
import asyncio
from TikTokApi import TikTokApi
from tiktok_analyzer.utils.config import Config
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class TikTokClient:
    """
    Client for interacting with the TikTok API.
    """
    
    def __init__(self):
        """Initialize the TikTok API client."""
        self.ms_token = Config.get_tiktok_ms_token()
        self.api = None
        self._initialize_api()
    
    def _initialize_api(self):
        """Initialize the TikTok API client."""
        try:
            self.api = TikTokApi(ms_token=self.ms_token)
            logger.info("TikTok API client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TikTok API client: {str(e)}")
            raise
    
    def get_trending_users(self, count=100):
        """
        Get trending TikTok users.
        
        Args:
            count: Number of trending users to retrieve (default: 100)
            
        Returns:
            List of user dictionaries
        """
        try:
            trending_videos = asyncio.run(self._get_trending_videos(count))
            
            users = {}
            for video in trending_videos:
                author = video.get('author', {})
                username = author.get('uniqueId')
                if username and username not in users:
                    users[username] = {
                        'username': username,
                        'display_name': author.get('nickname'),
                        'follower_count': author.get('followerCount', 0),
                        'following_count': author.get('followingCount', 0),
                        'heart_count': author.get('heartCount', 0),
                        'video_count': author.get('videoCount', 0),
                        'verified': author.get('verified', False),
                        'signature': author.get('signature', ''),
                        'user_id': author.get('id'),
                        'sec_uid': author.get('secUid'),
                        'avatar_url': author.get('avatarMedium')
                    }
            
            return list(users.values())
        
        except Exception as e:
            logger.error(f"Error getting trending users: {str(e)}")
            return []
    
    async def _get_trending_videos(self, count=100):
        """
        Get trending TikTok videos.
        
        Args:
            count: Number of trending videos to retrieve (default: 100)
            
        Returns:
            List of video dictionaries
        """
        try:
            trending = self.api.trending.videos(count=count)
            videos = []
            
            async for video in trending:
                videos.append(video)
                if len(videos) >= count:
                    break
            
            return videos
        
        except Exception as e:
            logger.error(f"Error getting trending videos: {str(e)}")
            return []
    
    def get_user_videos(self, username, limit=10):
        """
        Get videos from a specific user.
        
        Args:
            username: TikTok username
            limit: Maximum number of videos to retrieve (default: 10)
            
        Returns:
            List of video dictionaries
        """
        try:
            user = asyncio.run(self._get_user_by_username(username))
            
            if not user:
                logger.warning(f"User not found: {username}")
                return []
            
            user_videos = asyncio.run(self._get_videos_by_user(user, limit))
            
            videos = []
            for video in user_videos:
                stats = video.get('stats', {})
                videos.append({
                    'id': video.get('id'),
                    'desc': video.get('desc', ''),
                    'create_time': video.get('createTime', 0),
                    'likes': stats.get('diggCount', 0),
                    'comments': stats.get('commentCount', 0),
                    'shares': stats.get('shareCount', 0),
                    'views': stats.get('playCount', 0),
                    'video_url': video.get('video', {}).get('downloadAddr', '')
                })
            
            return videos
        
        except Exception as e:
            logger.error(f"Error getting user videos for {username}: {str(e)}")
            return []
    
    async def _get_user_by_username(self, username):
        """
        Get user data by username.
        
        Args:
            username: TikTok username
            
        Returns:
            User dictionary or None if not found
        """
        try:
            user = await self.api.user(username).info()
            return user
        except Exception as e:
            logger.error(f"Error getting user by username {username}: {str(e)}")
            return None
    
    async def _get_videos_by_user(self, user, limit=10):
        """
        Get videos by user.
        
        Args:
            user: User dictionary
            limit: Maximum number of videos to retrieve (default: 10)
            
        Returns:
            List of video dictionaries
        """
        try:
            user_videos = self.api.user(user).videos(count=limit)
            videos = []
            
            async for video in user_videos:
                videos.append(video)
                if len(videos) >= limit:
                    break
            
            return videos
        except Exception as e:
            logger.error(f"Error getting videos by user: {str(e)}")
            return []
    
    def get_video_download_url(self, video_id):
        """
        Get the download URL for a video.
        
        Args:
            video_id: TikTok video ID
            
        Returns:
            Video download URL or None if not found
        """
        try:
            video = asyncio.run(self._get_video_by_id(video_id))
            if video:
                return video.get('video', {}).get('downloadAddr')
            return None
        except Exception as e:
            logger.error(f"Error getting video download URL for {video_id}: {str(e)}")
            return None
    
    async def _get_video_by_id(self, video_id):
        """
        Get video data by ID.
        
        Args:
            video_id: TikTok video ID
            
        Returns:
            Video dictionary or None if not found
        """
        try:
            video = await self.api.video(id=video_id).info()
            return video
        except Exception as e:
            logger.error(f"Error getting video by ID {video_id}: {str(e)}")
            return None

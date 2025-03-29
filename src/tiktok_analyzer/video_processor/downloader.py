"""
Video downloader module for TikTok videos.

This module is responsible for downloading videos from TikTok.
"""

import os
import requests
import time
from pathlib import Path
from tiktok_analyzer.api.tiktok_client import TikTokClient
from tiktok_analyzer.utils.config import Config
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class VideoDownloader:
    """
    Downloads videos from TikTok.
    """
    
    def __init__(self):
        """Initialize the video downloader."""
        self.tiktok_client = TikTokClient()
        self.storage_path = Config.get_video_storage_path()
        
        os.makedirs(self.storage_path, exist_ok=True)
    
    def download_latest_video(self, influencer):
        """
        Download the latest video from a TikTok influencer.
        
        Args:
            influencer: Influencer data dictionary
            
        Returns:
            Path to the downloaded video file or None if download failed
        """
        try:
            username = influencer['username']
            logger.info(f"Downloading latest video for {username}")
            
            videos = self.tiktok_client.get_user_videos(username, limit=1)
            
            if not videos:
                logger.warning(f"No videos found for {username}")
                return None
            
            latest_video = videos[0]
            video_id = latest_video['id']
            video_url = latest_video['video_url']
            
            if not video_url:
                video_url = self.tiktok_client.get_video_download_url(video_id)
                
                if not video_url:
                    logger.warning(f"Could not get download URL for video {video_id}")
                    return None
            
            return self._download_video(video_url, username, video_id)
            
        except Exception as e:
            logger.error(f"Error downloading latest video for {influencer['username']}: {str(e)}")
            return None
    
    def _download_video(self, url, username, video_id):
        """
        Download a video from a URL.
        
        Args:
            url: Video download URL
            username: TikTok username
            video_id: TikTok video ID
            
        Returns:
            Path to the downloaded video file or None if download failed
        """
        try:
            timestamp = int(time.time())
            filename = f"{username}_{video_id}_{timestamp}.mp4"
            file_path = os.path.join(self.storage_path, filename)
            
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Video downloaded successfully: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            return None
    
    def download_video_by_id(self, video_id):
        """
        Download a specific video by ID.
        
        Args:
            video_id: TikTok video ID
            
        Returns:
            Path to the downloaded video file or None if download failed
        """
        try:
            video_url = self.tiktok_client.get_video_download_url(video_id)
            
            if not video_url:
                logger.warning(f"Could not get download URL for video {video_id}")
                return None
            
            timestamp = int(time.time())
            filename = f"video_{video_id}_{timestamp}.mp4"
            file_path = os.path.join(self.storage_path, filename)
            
            response = requests.get(video_url, stream=True)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Video downloaded successfully: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error downloading video by ID {video_id}: {str(e)}")
            return None

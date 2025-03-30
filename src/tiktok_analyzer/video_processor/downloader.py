"""
Video downloader module for TikTok videos.

This module is responsible for downloading videos from TikTok influencers,
handling different video formats and access restrictions.
"""

import os
import requests
import time
import concurrent.futures
from typing import Dict, List, Optional, Any
from pathlib import Path
from tiktok_analyzer.api.tiktok_client import TikTokClient
from tiktok_analyzer.utils.config import Config
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class VideoDownloader:
    """
    Downloads videos from TikTok.
    
    This class provides functionality to download videos from TikTok influencers,
    either individually or in batch. It handles different video formats and
    access restrictions through robust error handling.
    """
    
    def __init__(self, data_source_type: Optional[str] = None):
        """
        Initialize the video downloader.
        
        Args:
            data_source_type: Type of data source to use ('api', 'csv', 'mock', or None)
                If None, the data source will be determined from the configuration.
        """
        self.tiktok_client = TikTokClient(data_source_type)
        self.storage_path = Config.get_video_storage_path()
        
        os.makedirs(self.storage_path, exist_ok=True)
        logger.info(f"Video storage path: {self.storage_path}")
    
    def download_latest_videos_for_influencers(self, influencers: List[Dict[str, Any]], max_workers: int = 5) -> Dict[str, str]:
        """
        Download the latest video for multiple influencers in parallel.
        
        Args:
            influencers: List of influencer data dictionaries
            max_workers: Maximum number of concurrent downloads (default: 5)
            
        Returns:
            Dictionary mapping influencer usernames to downloaded video paths
        """
        logger.info(f"Downloading latest videos for {len(influencers)} influencers")
        
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_influencer = {
                executor.submit(self.download_latest_video, influencer): influencer
                for influencer in influencers
            }
            
            for future in concurrent.futures.as_completed(future_to_influencer):
                influencer = future_to_influencer[future]
                username = influencer['username']
                
                try:
                    video_path = future.result()
                    if video_path:
                        results[username] = video_path
                        logger.info(f"Successfully downloaded video for {username}")
                    else:
                        logger.warning(f"Failed to download video for {username}")
                except Exception as e:
                    logger.error(f"Exception while downloading video for {username}: {str(e)}")
        
        logger.info(f"Downloaded {len(results)} videos out of {len(influencers)} influencers")
        return results
    
    def download_latest_video(self, influencer: Dict[str, Any]) -> Optional[str]:
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
            video_url = latest_video.get('video_url')
            
            if not video_url:
                video_url = self.tiktok_client.get_video_download_url(video_id)
                
                if not video_url:
                    logger.warning(f"Could not get download URL for video {video_id}")
                    return None
            
            video_path = self._download_video(video_url, username, video_id)
            
            if video_path:
                metadata_path = f"{video_path}.json"
                self._save_video_metadata(metadata_path, latest_video)
            
            return video_path
            
        except Exception as e:
            logger.error(f"Error downloading latest video for {influencer.get('username', 'unknown')}: {str(e)}")
            return None
    
    def _download_video(self, url: str, username: str, video_id: str) -> Optional[str]:
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
            
            logger.info(f"Downloading video from {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, stream=True, headers=headers, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 1024*1024 and downloaded % (1024*1024) < 8192:  # Log every ~1MB
                            progress = (downloaded / total_size) * 100 if total_size > 0 else 0
                            logger.debug(f"Download progress for {username}: {progress:.1f}%")
            
            if os.path.getsize(file_path) == 0:
                logger.error(f"Downloaded file is empty: {file_path}")
                os.remove(file_path)
                return None
            
            logger.info(f"Video downloaded successfully: {file_path} ({os.path.getsize(file_path) / 1024:.1f} KB)")
            return file_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error downloading video: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            return None
    
    def _save_video_metadata(self, metadata_path: str, video_data: Dict[str, Any]) -> None:
        """
        Save video metadata to a JSON file.
        
        Args:
            metadata_path: Path to save the metadata
            video_data: Video metadata dictionary
        """
        try:
            import json
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(video_data, f, ensure_ascii=False, indent=2)
            logger.debug(f"Saved video metadata to {metadata_path}")
        except Exception as e:
            logger.error(f"Error saving video metadata: {str(e)}")
    
    def download_video_by_id(self, video_id: str) -> Optional[str]:
        """
        Download a specific video by ID.
        
        Args:
            video_id: TikTok video ID
            
        Returns:
            Path to the downloaded video file or None if download failed
        """
        try:
            logger.info(f"Downloading video by ID: {video_id}")
            
            video_url = self.tiktok_client.get_video_download_url(video_id)
            
            if not video_url:
                logger.warning(f"Could not get download URL for video {video_id}")
                return None
            
            timestamp = int(time.time())
            filename = f"video_{video_id}_{timestamp}.mp4"
            file_path = os.path.join(self.storage_path, filename)
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(video_url, stream=True, headers=headers, timeout=30)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            if os.path.getsize(file_path) == 0:
                logger.error(f"Downloaded file is empty: {file_path}")
                os.remove(file_path)
                return None
            
            logger.info(f"Video downloaded successfully: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error downloading video by ID {video_id}: {str(e)}")
            return None

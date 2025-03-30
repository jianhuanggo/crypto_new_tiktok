"""
Configuration management for the TikTok Influencer Analysis Application.

This module handles loading and validating configuration from environment variables.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration manager for the application."""
    
    @staticmethod
    def get_tiktok_ms_token() -> str:
        """
        Get the TikTok MS token from environment variables.
        
        Returns:
            TikTok MS token string
            
        Raises:
            ValueError: If the token is not set and using the API data source
        """
        token = os.getenv("TIKTOK_MS_TOKEN", "")
        data_source = os.getenv("TIKTOK_DATA_SOURCE", "api").lower()
        
        if not token and data_source == "api":
            raise ValueError("TIKTOK_MS_TOKEN environment variable is not set")
        
        return token
    
    @staticmethod
    def get_openai_api_key() -> str:
        """
        Get the OpenAI API key from environment variables.
        
        Returns:
            OpenAI API key string
            
        Raises:
            ValueError: If the API key is not set
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        return api_key
    
    @staticmethod
    def get_email_config() -> Dict[str, Any]:
        """
        Get email configuration from environment variables.
        
        Returns:
            Dictionary containing email configuration
            
        Raises:
            ValueError: If required email configuration is not set
        """
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        smtp_server = os.getenv("EMAIL_SMTP_SERVER")
        smtp_port = os.getenv("EMAIL_SMTP_PORT")
        recipient = os.getenv("EMAIL_RECIPIENT")
        
        if not all([sender, password, smtp_server, smtp_port]):
            raise ValueError("Email configuration environment variables are not set")
        
        return {
            "sender": sender,
            "password": password,
            "smtp_server": smtp_server,
            "smtp_port": int(smtp_port),
            "recipient": recipient
        }
    
    @staticmethod
    def get_video_storage_path() -> str:
        """
        Get the path for storing downloaded videos.
        
        Returns:
            Path to the video storage directory
        """
        return os.getenv("VIDEO_STORAGE_PATH", os.path.join(os.getcwd(), "data", "videos"))
    
    @staticmethod
    def get_data_source_config() -> Dict[str, Any]:
        """
        Get data source configuration from environment variables.
        
        Returns:
            Dictionary containing data source configuration
        """
        data_source = os.getenv("TIKTOK_DATA_SOURCE", "api").lower()
        
        config = {
            "type": data_source,
            "users_file": os.getenv("TIKTOK_USERS_FILE", os.path.join("data", "tiktok_users.csv")),
            "videos_file": os.getenv("TIKTOK_VIDEOS_FILE", os.path.join("data", "tiktok_videos.csv")),
            "mock_user_count": int(os.getenv("TIKTOK_MOCK_USER_COUNT", "100")),
            "mock_videos_per_user": int(os.getenv("TIKTOK_MOCK_VIDEOS_PER_USER", "10"))
        }
        
        return config

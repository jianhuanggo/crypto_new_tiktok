"""
Configuration management for the TikTok Influencer Analysis Application.

This module handles loading and validating configuration from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration manager for the application."""
    
    @staticmethod
    def get_tiktok_ms_token():
        """Get the TikTok MS token from environment variables."""
        token = os.getenv("TIKTOK_MS_TOKEN")
        if not token:
            raise ValueError("TIKTOK_MS_TOKEN environment variable is not set")
        return token
    
    @staticmethod
    def get_openai_api_key():
        """Get the OpenAI API key from environment variables."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        return api_key
    
    @staticmethod
    def get_email_config():
        """Get email configuration from environment variables."""
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
    def get_video_storage_path():
        """Get the path for storing downloaded videos."""
        return os.getenv("VIDEO_STORAGE_PATH", os.path.join(os.getcwd(), "videos"))

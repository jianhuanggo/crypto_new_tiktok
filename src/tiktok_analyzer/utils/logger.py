"""
Logging utilities for the TikTok Influencer Analysis Application.
"""

import logging
import os
from datetime import datetime

def setup_logger(log_level=logging.INFO):
    """
    Set up and configure the application logger.
    
    Args:
        log_level: The logging level to use (default: INFO)
        
    Returns:
        A configured logger instance
    """
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"tiktok_analyzer_{timestamp}.log")
    
    logger = logging.getLogger("tiktok_analyzer")
    logger.setLevel(log_level)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

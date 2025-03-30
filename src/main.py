"""
Main entry point for the TikTok Influencer Analysis Application.

This script orchestrates the workflow of:
1. Identifying top TikTok influencers
2. Downloading their latest videos
3. Extracting and summarizing content
4. Sending email summaries

The application can be configured using environment variables or command-line arguments.
"""

import os
import sys
import argparse
import time
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from tiktok_analyzer.api.influencer_analyzer import InfluencerAnalyzer
from tiktok_analyzer.video_processor.downloader import VideoDownloader
from tiktok_analyzer.video_processor.content_analyzer import ContentAnalyzer
from tiktok_analyzer.emailer.email_manager import EmailManager
from tiktok_analyzer.utils.config import Config
from tiktok_analyzer.utils.logger import setup_logger

load_dotenv()

logger = setup_logger()

class WorkflowManager:
    """
    Manages the entire workflow from influencer identification to email sending.
    
    This class orchestrates the complete TikTok influencer analysis workflow:
    1. Identifying top TikTok influencers based on metrics like engagement and follower count
    2. Downloading their latest videos in parallel
    3. Extracting and summarizing the content of each video
    4. Sending an email with the summarized content
    """
    
    def __init__(self, data_source_type: Optional[str] = None, max_workers: int = 5):
        """
        Initialize the workflow components.
        
        Args:
            data_source_type: Type of data source to use ('api', 'csv', 'mock', or None)
                If None, the data source will be determined from the configuration.
            max_workers: Maximum number of concurrent downloads (default: 5)
        """
        self.data_source_type = data_source_type
        self.max_workers = max_workers
        
        self.influencer_analyzer = InfluencerAnalyzer(data_source_type)
        self.video_downloader = VideoDownloader(data_source_type)
        self.content_analyzer = ContentAnalyzer()
        self.email_manager = EmailManager()
        
        logger.info(f"Workflow manager initialized with data source type: {data_source_type or 'default'}")
        logger.info(f"Using max_workers: {max_workers} for parallel processing")
        
    def run(self, influencer_limit: int = 10, recipient: Optional[str] = None) -> bool:
        """
        Execute the complete workflow.
        
        Args:
            influencer_limit: Number of top influencers to analyze (default: 10)
            recipient: Email recipient (default: uses the configured recipient)
            
        Returns:
            True if the workflow completed successfully, False otherwise
        """
        start_time = time.time()
        
        try:
            logger.info(f"Identifying top {influencer_limit} TikTok influencers...")
            top_influencers = self.influencer_analyzer.get_top_influencers(limit=influencer_limit)
            
            if not top_influencers:
                logger.error("No influencers found. Workflow cannot continue.")
                return False
                
            logger.info(f"Found {len(top_influencers)} top influencers")
            
            logger.info(f"Downloading latest videos for {len(top_influencers)} influencers...")
            influencer_videos = self.video_downloader.download_latest_videos_for_influencers(
                top_influencers, 
                max_workers=self.max_workers
            )
            
            if not influencer_videos:
                logger.error("No videos downloaded. Workflow cannot continue.")
                return False
                
            logger.info(f"Downloaded {len(influencer_videos)} videos")
            
            logger.info("Analyzing video content (extracting and summarizing)...")
            analysis_results = self.content_analyzer.analyze_influencer_videos(influencer_videos)
            
            if not analysis_results:
                logger.error("No content analysis results. Workflow cannot continue.")
                return False
                
            logger.info(f"Analyzed content for {len(analysis_results)} videos")
            
            logger.info("Sending email with video summaries...")
            email_success = self.email_manager.send_influencer_summaries(
                analysis_results,
                top_influencers,
                recipient
            )
            
            if not email_success:
                logger.error("Failed to send email. Workflow completed with errors.")
                return False
            
            elapsed_time = time.time() - start_time
            logger.info(f"Workflow completed successfully in {elapsed_time:.2f} seconds")
            return True
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"Error in workflow after {elapsed_time:.2f} seconds: {str(e)}")
            return False

def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description='TikTok Influencer Analysis Application')
    
    parser.add_argument('--data-source', type=str, choices=['api', 'csv', 'mock'],
                        help='Data source type (api, csv, mock)')
    
    parser.add_argument('--limit', type=int, default=10,
                        help='Number of top influencers to analyze (default: 10)')
    
    parser.add_argument('--recipient', type=str,
                        help='Email recipient (default: uses the configured recipient)')
    
    parser.add_argument('--max-workers', type=int, default=5,
                        help='Maximum number of concurrent downloads (default: 5)')
    
    parser.add_argument('--test-email', action='store_true',
                        help='Send a test email to verify email configuration')
    
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    args = parse_arguments()
    
    workflow = WorkflowManager(
        data_source_type=args.data_source,
        max_workers=args.max_workers
    )
    
    if args.test_email:
        logger.info("Sending test email...")
        success = workflow.email_manager.send_test_email(args.recipient)
        
        if success:
            logger.info("Test email sent successfully")
        else:
            logger.error("Failed to send test email")
        
        return
    
    success = workflow.run(
        influencer_limit=args.limit,
        recipient=args.recipient
    )
    
    if success:
        logger.info("Application completed successfully")
        sys.exit(0)
    else:
        logger.error("Application failed to complete")
        sys.exit(1)

if __name__ == "__main__":
    main()

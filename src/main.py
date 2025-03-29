"""
Main entry point for the TikTok Influencer Analysis Application.

This script orchestrates the workflow of:
1. Identifying top TikTok influencers
2. Downloading their latest videos
3. Extracting and summarizing content
4. Sending email summaries
"""

import os
import logging
from dotenv import load_dotenv
from tiktok_analyzer.api.influencer_analyzer import InfluencerAnalyzer
from tiktok_analyzer.video_processor.downloader import VideoDownloader
from tiktok_analyzer.video_processor.content_extractor import ContentExtractor
from tiktok_analyzer.summarizer.text_summarizer import TextSummarizer
from tiktok_analyzer.emailer.email_composer import EmailComposer
from tiktok_analyzer.emailer.email_sender import EmailSender
from tiktok_analyzer.utils.logger import setup_logger

load_dotenv()

logger = setup_logger()

class WorkflowManager:
    """
    Manages the entire workflow from influencer identification to email sending.
    """
    
    def __init__(self):
        """Initialize the workflow components."""
        self.influencer_analyzer = InfluencerAnalyzer()
        self.video_downloader = VideoDownloader()
        self.content_extractor = ContentExtractor()
        self.text_summarizer = TextSummarizer()
        self.email_composer = EmailComposer()
        self.email_sender = EmailSender()
        
    def run(self):
        """Execute the complete workflow."""
        try:
            logger.info("Identifying top TikTok influencers...")
            top_influencers = self.influencer_analyzer.get_top_influencers(limit=10)
            logger.info(f"Found {len(top_influencers)} top influencers")
            
            logger.info("Downloading latest videos...")
            video_paths = {}
            for influencer in top_influencers:
                video_path = self.video_downloader.download_latest_video(influencer)
                video_paths[influencer['username']] = video_path
            
            logger.info("Extracting content from videos...")
            extracted_content = {}
            for username, video_path in video_paths.items():
                text_content = self.content_extractor.extract_content(video_path)
                extracted_content[username] = text_content
            
            logger.info("Summarizing content...")
            summaries = {}
            for username, content in extracted_content.items():
                summary = self.text_summarizer.summarize(content)
                summaries[username] = summary
            
            logger.info("Composing email...")
            email_content = self.email_composer.compose_email(summaries, top_influencers)
            
            logger.info("Sending email...")
            recipient = os.getenv("EMAIL_RECIPIENT")
            self.email_sender.send_email(recipient, "TikTok Influencer Video Summaries", email_content)
            
            logger.info("Workflow completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error in workflow: {str(e)}")
            return False

def main():
    """Main entry point for the application."""
    workflow = WorkflowManager()
    success = workflow.run()
    
    if success:
        logger.info("Application completed successfully")
    else:
        logger.error("Application failed to complete")

if __name__ == "__main__":
    main()

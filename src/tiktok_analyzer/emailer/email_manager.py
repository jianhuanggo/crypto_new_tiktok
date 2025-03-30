"""
Email management module.

This module provides a unified interface for composing and sending
emails with TikTok influencer video summaries.
"""

from typing import Dict, List, Optional, Any
from tiktok_analyzer.emailer.email_composer import EmailComposer
from tiktok_analyzer.emailer.email_sender import EmailSender
from tiktok_analyzer.utils.config import Config
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class EmailManager:
    """
    Manages the composition and sending of emails with TikTok influencer video summaries.
    
    This class integrates the EmailComposer and EmailSender to provide a complete
    solution for formatting and delivering email summaries of TikTok influencer videos.
    """
    
    def __init__(self):
        """Initialize the email manager with composer and sender."""
        self.email_composer = EmailComposer()
        self.email_sender = EmailSender()
        self.email_config = Config.get_email_config()
        logger.info("Email manager initialized")
    
    def send_influencer_summaries(self, 
                                  analysis_results: Dict[str, Dict[str, str]], 
                                  influencers: List[Dict[str, Any]],
                                  recipient: Optional[str] = None) -> bool:
        """
        Compose and send an email with summaries of influencer videos.
        
        Args:
            analysis_results: Dictionary mapping influencer usernames to analysis results
                Each analysis result should contain 'summary' and 'extracted_content' keys
            influencers: List of influencer data dictionaries
            recipient: Email recipient (default: uses the configured recipient)
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        try:
            logger.info(f"Preparing to send email with {len(analysis_results)} influencer summaries")
            
            summaries = {username: result.get('summary', 'No summary available.') 
                         for username, result in analysis_results.items()}
            
            email_content = self.email_composer.compose_email(summaries, influencers)
            
            if recipient is None:
                recipient = self.email_config.get('recipient')
                if not recipient:
                    logger.error("No recipient email address provided or configured")
                    return False
            
            current_date = self._get_formatted_date()
            subject = f"TikTok Influencer Video Summaries - {current_date}"
            
            success = self.email_sender.send_email(recipient, subject, email_content)
            
            if success:
                logger.info(f"Successfully sent influencer summaries email to {recipient}")
            else:
                logger.error(f"Failed to send influencer summaries email to {recipient}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending influencer summaries email: {str(e)}")
            self._send_error_notification(str(e), recipient)
            return False
    
    def send_batch_influencer_summaries(self, 
                                        analysis_results: Dict[str, Dict[str, str]], 
                                        influencers: List[Dict[str, Any]],
                                        recipients: List[str]) -> Dict[str, bool]:
        """
        Compose and send an email with summaries of influencer videos to multiple recipients.
        
        Args:
            analysis_results: Dictionary mapping influencer usernames to analysis results
                Each analysis result should contain 'summary' and 'extracted_content' keys
            influencers: List of influencer data dictionaries
            recipients: List of email recipients
            
        Returns:
            Dictionary mapping recipients to success status
        """
        try:
            logger.info(f"Preparing to send email to {len(recipients)} recipients")
            
            summaries = {username: result.get('summary', 'No summary available.') 
                         for username, result in analysis_results.items()}
            
            email_content = self.email_composer.compose_email(summaries, influencers)
            
            current_date = self._get_formatted_date()
            subject = f"TikTok Influencer Video Summaries - {current_date}"
            
            results = self.email_sender.send_batch_emails(recipients, subject, email_content)
            
            success_count = sum(1 for success in results.values() if success)
            logger.info(f"Successfully sent emails to {success_count} out of {len(recipients)} recipients")
            
            return results
            
        except Exception as e:
            logger.error(f"Error sending batch influencer summaries emails: {str(e)}")
            return {recipient: False for recipient in recipients}
    
    def _send_error_notification(self, error_message: str, recipient: Optional[str] = None) -> bool:
        """
        Send an error notification email.
        
        Args:
            error_message: Error message to include in the email
            recipient: Email recipient (default: uses the configured recipient)
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        try:
            error_email = self.email_composer._generate_error_email(error_message)
            
            if recipient is None:
                recipient = self.email_config.get('recipient')
                if not recipient:
                    logger.error("No recipient email address provided or configured for error notification")
                    return False
            
            current_date = self._get_formatted_date()
            subject = f"ERROR: TikTok Influencer Analysis - {current_date}"
            
            return self.email_sender.send_email(recipient, subject, error_email)
            
        except Exception as e:
            logger.error(f"Error sending error notification email: {str(e)}")
            return False
    
    def _get_formatted_date(self) -> str:
        """
        Get the current date formatted for email subjects.
        
        Returns:
            Formatted date string
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def send_test_email(self, recipient: Optional[str] = None) -> bool:
        """
        Send a test email to verify email configuration.
        
        Args:
            recipient: Email recipient (default: uses the configured recipient)
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        try:
            logger.info("Sending test email")
            
            if recipient is None:
                recipient = self.email_config.get('recipient')
                if not recipient:
                    logger.error("No recipient email address provided or configured for test email")
                    return False
            
            subject = "TikTok Analyzer - Test Email"
            content = """
            <html>
            <body>
                <h1>TikTok Analyzer - Test Email</h1>
                <p>This is a test email to verify that the email configuration is working correctly.</p>
                <p>If you received this email, the email configuration is working!</p>
            </body>
            </html>
            """
            
            success = self.email_sender.send_email(recipient, subject, content)
            
            if success:
                logger.info(f"Successfully sent test email to {recipient}")
            else:
                logger.error(f"Failed to send test email to {recipient}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error sending test email: {str(e)}")
            return False

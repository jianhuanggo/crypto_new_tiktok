"""
Email sending module.

This module is responsible for sending emails with video summaries.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tiktok_analyzer.utils.config import Config
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class EmailSender:
    """
    Sends emails with video summaries.
    """
    
    def __init__(self):
        """Initialize the email sender."""
        self.email_config = Config.get_email_config()
    
    def send_email(self, recipient, subject, content, content_type='html'):
        """
        Send an email with the provided content.
        
        Args:
            recipient: Email recipient
            subject: Email subject
            content: Email content
            content_type: Content type ('html' or 'plain', default: 'html')
            
        Returns:
            True if the email was sent successfully, False otherwise
        """
        try:
            logger.info(f"Sending email to {recipient}")
            
            message = MIMEMultipart()
            message['From'] = self.email_config['sender']
            message['To'] = recipient
            message['Subject'] = subject
            
            message.attach(MIMEText(content, content_type))
            
            with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
                server.starttls()
                
                server.login(self.email_config['sender'], self.email_config['password'])
                
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_batch_emails(self, recipients, subject, content, content_type='html'):
        """
        Send the same email to multiple recipients.
        
        Args:
            recipients: List of email recipients
            subject: Email subject
            content: Email content
            content_type: Content type ('html' or 'plain', default: 'html')
            
        Returns:
            Dictionary mapping recipients to success status
        """
        results = {}
        
        for recipient in recipients:
            success = self.send_email(recipient, subject, content, content_type)
            results[recipient] = success
        
        return results

"""
Text summarization module.

This module is responsible for summarizing text content using an LLM.
"""

import os
from openai import OpenAI
from tiktok_analyzer.utils.config import Config
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class TextSummarizer:
    """
    Summarizes text content using an LLM.
    """
    
    def __init__(self):
        """Initialize the text summarizer."""
        self.api_key = Config.get_openai_api_key()
        self.client = OpenAI(api_key=self.api_key)
    
    def summarize(self, text, max_tokens=150):
        """
        Summarize text content using OpenAI's API.
        
        Args:
            text: Text content to summarize
            max_tokens: Maximum number of tokens in the summary (default: 150)
            
        Returns:
            Summarized text
        """
        if not text:
            logger.warning("No text provided for summarization")
            return "No content available for summarization."
        
        try:
            logger.info(f"Summarizing text content: {len(text)} characters")
            
            prompt = f"Please provide a concise summary of the following TikTok video content:\n\n{text}\n\nSummary:"
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes TikTok video content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.5
            )
            
            summary = response.choices[0].message.content.strip()
            
            logger.info(f"Generated summary: {len(summary)} characters")
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing text: {str(e)}")
            return f"Error generating summary: {str(e)}"
    
    def batch_summarize(self, texts, max_tokens=150):
        """
        Summarize multiple text contents.
        
        Args:
            texts: List of text contents to summarize
            max_tokens: Maximum number of tokens in each summary (default: 150)
            
        Returns:
            List of summarized texts
        """
        summaries = []
        
        for text in texts:
            summary = self.summarize(text, max_tokens)
            summaries.append(summary)
        
        return summaries

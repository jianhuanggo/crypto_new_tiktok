"""
Content analysis module for TikTok videos.

This module combines content extraction and summarization to process
TikTok videos and generate concise summaries of their content.
"""

from typing import Dict, List, Optional, Any, Tuple
import os
from pathlib import Path
from tiktok_analyzer.video_processor.content_extractor import ContentExtractor
from tiktok_analyzer.summarizer.text_summarizer import TextSummarizer
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class ContentAnalyzer:
    """
    Analyzes TikTok video content by extracting text and generating summaries.
    
    This class combines the ContentExtractor and TextSummarizer to provide
    a complete solution for processing TikTok videos, extracting their textual
    content, and generating concise summaries using an LLM.
    """
    
    def __init__(self):
        """Initialize the content analyzer with extractors and summarizers."""
        self.content_extractor = ContentExtractor()
        self.text_summarizer = TextSummarizer()
        logger.info("Content analyzer initialized")
    
    def analyze_video(self, video_path: str, max_summary_tokens: int = 150) -> Dict[str, str]:
        """
        Analyze a video by extracting its content and generating a summary.
        
        Args:
            video_path: Path to the video file
            max_summary_tokens: Maximum number of tokens in the summary (default: 150)
            
        Returns:
            Dictionary containing extracted content and summary
        """
        if not video_path or not os.path.exists(video_path):
            logger.warning(f"Video file not found: {video_path}")
            return {
                "extracted_content": "",
                "summary": "No video content to analyze."
            }
        
        logger.info(f"Analyzing video content: {video_path}")
        
        extracted_content = self.content_extractor.extract_content(video_path)
        
        summary = self.text_summarizer.summarize(extracted_content, max_summary_tokens)
        
        return {
            "extracted_content": extracted_content,
            "summary": summary
        }
    
    def analyze_videos(self, video_paths: List[str], max_summary_tokens: int = 150) -> List[Dict[str, str]]:
        """
        Analyze multiple videos by extracting their content and generating summaries.
        
        Args:
            video_paths: List of paths to video files
            max_summary_tokens: Maximum number of tokens in each summary (default: 150)
            
        Returns:
            List of dictionaries containing extracted content and summaries
        """
        logger.info(f"Analyzing {len(video_paths)} videos")
        
        results = []
        
        for video_path in video_paths:
            result = self.analyze_video(video_path, max_summary_tokens)
            results.append(result)
        
        return results
    
    def analyze_influencer_videos(self, influencer_videos: Dict[str, str], max_summary_tokens: int = 150) -> Dict[str, Dict[str, str]]:
        """
        Analyze videos from multiple influencers.
        
        Args:
            influencer_videos: Dictionary mapping influencer usernames to video paths
            max_summary_tokens: Maximum number of tokens in each summary (default: 150)
            
        Returns:
            Dictionary mapping influencer usernames to analysis results
        """
        logger.info(f"Analyzing videos from {len(influencer_videos)} influencers")
        
        results = {}
        
        for username, video_path in influencer_videos.items():
            logger.info(f"Analyzing video for influencer: {username}")
            
            if not video_path or not os.path.exists(video_path):
                logger.warning(f"Video file not found for {username}: {video_path}")
                results[username] = {
                    "extracted_content": "",
                    "summary": f"No video content available for {username}."
                }
                continue
            
            result = self.analyze_video(video_path, max_summary_tokens)
            results[username] = result
        
        return results
    
    def extract_key_points(self, content: str, max_points: int = 5) -> List[str]:
        """
        Extract key points from content using the text summarizer.
        
        Args:
            content: Text content to extract key points from
            max_points: Maximum number of key points to extract (default: 5)
            
        Returns:
            List of key points
        """
        if not content:
            return []
        
        try:
            logger.info(f"Extracting key points from content: {len(content)} characters")
            
            prompt = f"Extract {max_points} key points from the following TikTok video content. Format each point as a separate line starting with '- ':\n\n{content}"
            
            response = self.text_summarizer.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts key points from TikTok video content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            key_points_text = response.choices[0].message.content.strip()
            
            key_points = [point.strip()[2:].strip() for point in key_points_text.split('\n') if point.strip().startswith('- ')]
            
            logger.info(f"Extracted {len(key_points)} key points")
            return key_points
            
        except Exception as e:
            logger.error(f"Error extracting key points: {str(e)}")
            return []
    
    def get_content_sentiment(self, content: str) -> Tuple[str, float]:
        """
        Analyze the sentiment of content using the text summarizer.
        
        Args:
            content: Text content to analyze sentiment for
            
        Returns:
            Tuple of (sentiment, confidence) where sentiment is one of 'positive', 'neutral', or 'negative'
        """
        if not content:
            return ("neutral", 0.5)
        
        try:
            logger.info(f"Analyzing sentiment of content: {len(content)} characters")
            
            prompt = f"Analyze the sentiment of the following TikTok video content. Respond with only one word: 'positive', 'neutral', or 'negative', followed by a confidence score between 0 and 1 (e.g., 'positive 0.8'):\n\n{content}"
            
            response = self.text_summarizer.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes sentiment of TikTok video content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.1
            )
            
            result = response.choices[0].message.content.strip().lower()
            
            parts = result.split()
            sentiment = parts[0] if parts and parts[0] in ['positive', 'neutral', 'negative'] else 'neutral'
            
            try:
                confidence = float(parts[1]) if len(parts) > 1 else 0.5
                confidence = max(0, min(1, confidence))  # Ensure confidence is between 0 and 1
            except (ValueError, IndexError):
                confidence = 0.5
            
            logger.info(f"Sentiment analysis result: {sentiment} (confidence: {confidence:.2f})")
            return (sentiment, confidence)
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return ("neutral", 0.5)

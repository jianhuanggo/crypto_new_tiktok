"""
TikTok influencer identification and analysis module.

This module is responsible for retrieving data about TikTok influencers
and identifying the top influencers based on metrics like engagement and follower count.
"""

from tiktok_analyzer.api.tiktok_client import TikTokClient
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class InfluencerAnalyzer:
    """
    Analyzes TikTok data to identify top influencers based on various metrics.
    """
    
    def __init__(self):
        """Initialize the influencer analyzer with a TikTok client."""
        self.tiktok_client = TikTokClient()
    
    def get_top_influencers(self, limit=10, metrics=None):
        """
        Retrieve the top TikTok influencers based on specified metrics.
        
        Args:
            limit: Number of top influencers to return (default: 10)
            metrics: List of metrics to consider for ranking (default: ['follower_count', 'engagement_rate'])
            
        Returns:
            List of dictionaries containing influencer data
        """
        if metrics is None:
            metrics = ['follower_count', 'engagement_rate']
        
        logger.info(f"Retrieving top {limit} influencers based on {metrics}")
        
        trending_users = self.tiktok_client.get_trending_users()
        
        if 'engagement_rate' in metrics:
            for user in trending_users:
                user['engagement_rate'] = self._calculate_engagement_rate(user)
        
        ranked_users = self._rank_users(trending_users, metrics)
        
        return ranked_users[:limit]
    
    def _calculate_engagement_rate(self, user):
        """
        Calculate the engagement rate for a user.
        
        Engagement rate = (likes + comments + shares) / views * 100
        
        Args:
            user: User data dictionary
            
        Returns:
            Engagement rate as a percentage
        """
        recent_videos = self.tiktok_client.get_user_videos(user['username'], limit=10)
        
        if not recent_videos:
            return 0
        
        total_engagement = 0
        total_views = 0
        
        for video in recent_videos:
            likes = video.get('likes', 0)
            comments = video.get('comments', 0)
            shares = video.get('shares', 0)
            views = video.get('views', 1)  # Avoid division by zero
            
            total_engagement += likes + comments + shares
            total_views += views
        
        if total_views == 0:
            return 0
        
        engagement_rate = (total_engagement / total_views) * 100
        return engagement_rate
    
    def _rank_users(self, users, metrics):
        """
        Rank users based on specified metrics.
        
        Args:
            users: List of user dictionaries
            metrics: List of metrics to consider for ranking
            
        Returns:
            List of users sorted by rank
        """
        ranked_users = users.copy()
        
        weights = {
            'follower_count': 0.6,
            'engagement_rate': 0.4,
        }
        
        for user in ranked_users:
            user['score'] = 0
            for metric in metrics:
                if metric in weights:
                    max_value = max(u.get(metric, 0) for u in users)
                    if max_value > 0:
                        normalized_value = user.get(metric, 0) / max_value
                        user['score'] += normalized_value * weights[metric]
        
        ranked_users.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return ranked_users

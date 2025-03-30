"""
TikTok influencer identification and analysis module.

This module is responsible for retrieving data about TikTok influencers
and identifying the top influencers based on metrics like engagement and follower count.
"""

from typing import List, Dict, Any, Optional
from tiktok_analyzer.api.tiktok_client import TikTokClient
from tiktok_analyzer.utils.logger import setup_logger

logger = setup_logger()

class InfluencerAnalyzer:
    """
    Analyzes TikTok data to identify top influencers based on various metrics.
    """
    
    def __init__(self, data_source_type: Optional[str] = None):
        """
        Initialize the influencer analyzer with a TikTok client.
        
        Args:
            data_source_type: Type of data source to use ('api', 'csv', 'mock', or None)
                If None, the data source will be determined from the configuration.
        """
        self.tiktok_client = TikTokClient(data_source_type)
        logger.info(f"Influencer analyzer initialized with data source type: {data_source_type or 'default'}")
    
    def get_top_influencers(self, limit: int = 10, metrics: Optional[List[str]] = None) -> List[Dict[str, Any]]:
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
        
        trending_users = self.tiktok_client.get_trending_users(count=100)
        
        if not trending_users:
            logger.warning("No trending users found")
            return []
        
        if 'engagement_rate' in metrics:
            logger.info("Calculating engagement rates for users")
            for user in trending_users:
                user['engagement_rate'] = self._calculate_engagement_rate(user)
        
        ranked_users = self._rank_users(trending_users, metrics)
        
        top_users = ranked_users[:limit]
        logger.info(f"Retrieved top {len(top_users)} influencers")
        
        return top_users
    
    def _calculate_engagement_rate(self, user: Dict[str, Any]) -> float:
        """
        Calculate the engagement rate for a user.
        
        Engagement rate = (likes + comments + shares) / views * 100
        
        Args:
            user: User data dictionary
            
        Returns:
            Engagement rate as a percentage
        """
        username = user['username']
        logger.debug(f"Calculating engagement rate for user: {username}")
        
        recent_videos = self.tiktok_client.get_user_videos(username, limit=10)
        
        if not recent_videos:
            logger.warning(f"No videos found for user {username}, engagement rate set to 0")
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
            logger.warning(f"No views for user {username}, engagement rate set to 0")
            return 0
        
        engagement_rate = (total_engagement / total_views) * 100
        logger.debug(f"Calculated engagement rate for {username}: {engagement_rate:.2f}%")
        return engagement_rate
    
    def _rank_users(self, users: List[Dict[str, Any]], metrics: List[str]) -> List[Dict[str, Any]]:
        """
        Rank users based on specified metrics.
        
        Args:
            users: List of user dictionaries
            metrics: List of metrics to consider for ranking
            
        Returns:
            List of users sorted by rank
        """
        if not users:
            logger.warning("No users to rank")
            return []
        
        ranked_users = users.copy()
        
        weights = {
            'follower_count': 0.6,
            'engagement_rate': 0.4,
            'heart_count': 0.2,
            'video_count': 0.1,
        }
        
        valid_metrics = [m for m in metrics if m in weights]
        
        if not valid_metrics:
            logger.warning(f"No valid metrics found in {metrics}, using follower_count as default")
            valid_metrics = ['follower_count']
        
        total_weight = sum(weights[m] for m in valid_metrics)
        normalized_weights = {m: weights[m] / total_weight for m in valid_metrics}
        
        logger.info(f"Ranking users with metrics: {valid_metrics}")
        
        for user in ranked_users:
            user['score'] = 0
            for metric in valid_metrics:
                max_value = max((u.get(metric, 0) for u in users), default=1)
                
                if max_value > 0:
                    user_value = user.get(metric, 0)
                    normalized_value = user_value / max_value
                    
                    user['score'] += normalized_value * normalized_weights[metric]
        
        ranked_users.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return ranked_users
    
    def get_influencer_details(self, username: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific influencer.
        
        Args:
            username: TikTok username
            
        Returns:
            Dictionary containing detailed influencer data
        """
        logger.info(f"Getting details for influencer: {username}")
        
        users = self.tiktok_client.get_trending_users(count=100)
        user_data = next((user for user in users if user['username'] == username), None)
        
        if not user_data:
            logger.warning(f"Influencer not found: {username}")
            return {}
        
        recent_videos = self.tiktok_client.get_user_videos(username, limit=5)
        
        engagement_rate = self._calculate_engagement_rate(user_data)
        
        user_data['engagement_rate'] = engagement_rate
        user_data['recent_videos'] = recent_videos
        
        return user_data

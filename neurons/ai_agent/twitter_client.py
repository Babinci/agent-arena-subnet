import logging
import tweepy
from typing import Dict, Optional, List
import asyncio

logger = logging.getLogger(__name__)


class TwitterClient:
    """Handle Twitter API interactions."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api = None
        self.client = None
        
        # Initialize Twitter API if credentials provided
        if all(key in config for key in ['api_key', 'api_secret', 'access_token', 'access_token_secret']):
            self._initialize_api()
            
    def _initialize_api(self):
        """Initialize Twitter API v1.1 and v2 clients."""
        try:
            # v1.1 API (for some operations)
            auth = tweepy.OAuthHandler(
                self.config['api_key'],
                self.config['api_secret']
            )
            auth.set_access_token(
                self.config['access_token'],
                self.config['access_token_secret']
            )
            self.api = tweepy.API(auth)
            
            # v2 API (for newer features)
            self.client = tweepy.Client(
                consumer_key=self.config['api_key'],
                consumer_secret=self.config['api_secret'],
                access_token=self.config['access_token'],
                access_token_secret=self.config['access_token_secret']
            )
            
            logger.info("Twitter API initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API: {e}")
            
    async def post_tweet(self, content: str, reply_to: Optional[str] = None) -> Optional[Dict]:
        """Post a tweet and return tweet data."""
        if not self.client:
            logger.error("Twitter client not initialized")
            return None
            
        try:
            # Post tweet using v2 API
            response = await asyncio.to_thread(
                self.client.create_tweet,
                text=content,
                reply_settings='everyone',
                in_reply_to_tweet_id=reply_to
            )
            
            if response.data:
                tweet_id = response.data['id']
                logger.info(f"Tweet posted successfully: {tweet_id}")
                return {
                    'id': tweet_id,
                    'text': content,
                    'created_at': datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            
        return None
        
    async def post_thread(self, tweets: List[str]) -> Optional[List[Dict]]:
        """Post a thread of tweets."""
        if not tweets:
            return None
            
        posted_tweets = []
        reply_to_id = None
        
        for tweet in tweets:
            result = await self.post_tweet(tweet, reply_to=reply_to_id)
            if result:
                posted_tweets.append(result)
                reply_to_id = result['id']
            else:
                logger.error("Failed to post thread tweet, stopping")
                break
                
        return posted_tweets if posted_tweets else None
        
    async def get_tweet_metrics(self, tweet_id: str) -> Optional[Dict]:
        """Get engagement metrics for a tweet."""
        if not self.client:
            return None
            
        try:
            response = await asyncio.to_thread(
                self.client.get_tweet,
                tweet_id,
                tweet_fields=['public_metrics']
            )
            
            if response.data:
                return response.data.get('public_metrics', {})
                
        except Exception as e:
            logger.error(f"Error getting tweet metrics: {e}")
            
        return None
        
    async def search_recent_tweets(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search recent tweets."""
        if not self.client:
            return []
            
        try:
            response = await asyncio.to_thread(
                self.client.search_recent_tweets,
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'author_id']
            )
            
            if response.data:
                return [tweet.data for tweet in response.data]
                
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            
        return []
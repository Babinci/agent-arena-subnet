import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional, List, Dict
import random

from .content_generator import ContentGenerator
from .twitter_client import TwitterClient
from .mcp_integrations import MCPManager

logger = logging.getLogger(__name__)


class AITechNewsAgent:
    """Main AI agent for generating and posting tech news content."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.twitter_client = TwitterClient(config.get('twitter', {}))
        self.content_generator = ContentGenerator(config.get('llm', {}))
        self.mcp_manager = MCPManager(config.get('mcp', {}))
        
        # Posting schedule configuration
        self.posts_per_day = config.get('posts_per_day', 15)
        self.peak_hours = config.get('peak_hours', [12, 13, 21, 22, 23])  # UTC
        self.min_interval_minutes = config.get('min_interval_minutes', 30)
        
        self.is_running = False
        self.last_post_time = None
        
    async def start(self):
        """Start the agent's posting loop."""
        self.is_running = True
        logger.info("Starting AI Tech News Agent")
        
        # Initialize MCP servers
        await self.mcp_manager.initialize()
        
        # Start posting loop
        await self.run_posting_loop()
        
    async def stop(self):
        """Stop the agent."""
        self.is_running = False
        await self.mcp_manager.shutdown()
        logger.info("AI Tech News Agent stopped")
        
    async def run_posting_loop(self):
        """Main posting loop."""
        while self.is_running:
            try:
                # Check if it's time to post
                if await self.should_post_now():
                    await self.create_and_post_content()
                    
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in posting loop: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
                
    async def should_post_now(self) -> bool:
        """Determine if we should post now based on schedule."""
        now = datetime.now(timezone.utc)
        
        # Check minimum interval
        if self.last_post_time:
            minutes_since_last = (now - self.last_post_time).total_seconds() / 60
            if minutes_since_last < self.min_interval_minutes:
                return False
                
        # Prefer peak hours but allow some posts outside
        current_hour = now.hour
        if current_hour in self.peak_hours:
            return random.random() < 0.8  # 80% chance during peak
        else:
            return random.random() < 0.2  # 20% chance off-peak
            
    async def create_and_post_content(self):
        """Generate and post content."""
        try:
            # Fetch latest content sources
            content_sources = await self.gather_content_sources()
            
            # Decide content type
            content_type = self.choose_content_type()
            
            # Generate content
            tweet_content = await self.content_generator.generate(
                content_type=content_type,
                sources=content_sources
            )
            
            # Post to Twitter
            if tweet_content:
                result = await self.twitter_client.post_tweet(tweet_content)
                if result:
                    self.last_post_time = datetime.now(timezone.utc)
                    logger.info(f"Posted tweet: {tweet_content[:50]}...")
                    
        except Exception as e:
            logger.error(f"Error creating/posting content: {e}")
            
    async def gather_content_sources(self) -> Dict:
        """Gather content from various sources."""
        sources = {}
        
        try:
            # Get latest papers from ArXiv
            sources['papers'] = await self.mcp_manager.fetch_latest_papers()
            
            # Get trending AI news
            sources['news'] = await self.mcp_manager.fetch_ai_news()
            
            # Get tweets from key AI accounts
            sources['tweets'] = await self.mcp_manager.fetch_influencer_tweets()
            
        except Exception as e:
            logger.error(f"Error gathering sources: {e}")
            
        return sources
        
    def choose_content_type(self) -> str:
        """Choose content type based on strategy."""
        weights = {
            'paper_summary': 0.4,
            'breaking_news': 0.3,
            'educational_thread': 0.2,
            'engagement_question': 0.1
        }
        
        return random.choices(
            list(weights.keys()),
            weights=list(weights.values())
        )[0]
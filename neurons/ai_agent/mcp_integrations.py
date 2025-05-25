import logging
import asyncio
from typing import Dict, List, Optional
import aiohttp
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MCPManager:
    """Manage MCP (Model Context Protocol) server integrations."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.arxiv_url = config.get('arxiv_url', 'http://localhost:3000/arxiv')
        self.brave_url = config.get('brave_url', 'http://localhost:3001/search')
        self.twitter_mcp_url = config.get('twitter_url', 'http://localhost:3002/twitter')
        self.session = None
        
    async def initialize(self):
        """Initialize MCP connections."""
        self.session = aiohttp.ClientSession()
        logger.info("MCP Manager initialized")
        
    async def shutdown(self):
        """Shutdown MCP connections."""
        if self.session:
            await self.session.close()
            
    async def fetch_latest_papers(self, categories: List[str] = None) -> List[Dict]:
        """Fetch latest AI papers from ArXiv MCP."""
        if not categories:
            categories = ['cs.AI', 'cs.LG', 'cs.CL', 'cs.CV']
            
        papers = []
        
        for category in categories:
            try:
                # Query ArXiv MCP for recent papers
                params = {
                    'category': category,
                    'max_results': 5,
                    'sort_by': 'submittedDate',
                    'sort_order': 'descending'
                }
                
                async with self.session.get(f"{self.arxiv_url}/search", params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        papers.extend(data.get('papers', []))
                        
            except Exception as e:
                logger.error(f"Error fetching papers from {category}: {e}")
                
        # Sort by date and return most recent
        papers.sort(key=lambda x: x.get('published', ''), reverse=True)
        return papers[:10]
        
    async def fetch_ai_news(self) -> List[Dict]:
        """Fetch trending AI news using Brave Search MCP."""
        queries = [
            "artificial intelligence breakthrough today",
            "new AI model released",
            "machine learning news",
            "OpenAI ChatGPT GPT Claude news"
        ]
        
        news_items = []
        
        for query in queries:
            try:
                params = {
                    'q': query,
                    'freshness': 'pd',  # Past day
                    'count': 5
                }
                
                async with self.session.get(f"{self.brave_url}/web", params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        results = data.get('web', {}).get('results', [])
                        
                        # Filter for relevance
                        for result in results:
                            if self._is_relevant_news(result):
                                news_items.append({
                                    'title': result.get('title'),
                                    'description': result.get('description'),
                                    'url': result.get('url'),
                                    'published': result.get('page_age', datetime.utcnow().isoformat())
                                })
                                
            except Exception as e:
                logger.error(f"Error fetching news for '{query}': {e}")
                
        # Deduplicate and sort by recency
        seen_urls = set()
        unique_news = []
        for item in news_items:
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])
                unique_news.append(item)
                
        return unique_news[:10]
        
    async def fetch_influencer_tweets(self) -> List[Dict]:
        """Fetch tweets from key AI influencers."""
        influencers = [
            'sama',  # Sam Altman
            'ylecun',  # Yann LeCun  
            'AndrewYNg',  # Andrew Ng
            'GaryMarcus',  # Gary Marcus
            'emollick',  # Ethan Mollick
            'svpino',  # Santiago
            'bindureddy',  # Bindu Reddy
        ]
        
        tweets = []
        
        for username in influencers:
            try:
                params = {
                    'username': username,
                    'count': 5,
                    'exclude_replies': True
                }
                
                async with self.session.get(f"{self.twitter_mcp_url}/user_tweets", params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        user_tweets = data.get('tweets', [])
                        
                        # Filter for AI-related content
                        for tweet in user_tweets:
                            if self._is_ai_related(tweet.get('text', '')):
                                tweets.append({
                                    'author': username,
                                    'text': tweet.get('text'),
                                    'created_at': tweet.get('created_at'),
                                    'metrics': tweet.get('public_metrics', {})
                                })
                                
            except Exception as e:
                logger.error(f"Error fetching tweets from {username}: {e}")
                
        # Sort by engagement
        tweets.sort(
            key=lambda x: x.get('metrics', {}).get('like_count', 0),
            reverse=True
        )
        
        return tweets[:20]
        
    def _is_relevant_news(self, result: Dict) -> bool:
        """Check if news item is relevant to AI."""
        keywords = [
            'ai', 'artificial intelligence', 'machine learning',
            'neural network', 'deep learning', 'gpt', 'llm',
            'chatgpt', 'claude', 'gemini', 'model', 'transformer'
        ]
        
        text = f"{result.get('title', '')} {result.get('description', '')}".lower()
        return any(keyword in text for keyword in keywords)
        
    def _is_ai_related(self, text: str) -> bool:
        """Check if tweet is AI-related."""
        keywords = [
            'ai', 'artificial intelligence', 'ml', 'machine learning',
            'neural', 'model', 'gpt', 'llm', 'agent', 'compute',
            'training', 'inference', 'dataset', 'benchmark'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
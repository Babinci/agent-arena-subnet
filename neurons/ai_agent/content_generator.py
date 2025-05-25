import logging
from typing import Dict, List, Optional
import openai
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generate engaging content using LLMs."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'gpt-4')
        self.temperature = config.get('temperature', 0.8)
        
        if self.api_key:
            openai.api_key = self.api_key
            
    async def generate(self, content_type: str, sources: Dict) -> Optional[str]:
        """Generate content based on type and sources."""
        try:
            if content_type == 'paper_summary':
                return await self.generate_paper_summary(sources.get('papers', []))
            elif content_type == 'breaking_news':
                return await self.generate_news_tweet(sources.get('news', []))
            elif content_type == 'educational_thread':
                return await self.generate_educational_thread(sources)
            elif content_type == 'engagement_question':
                return await self.generate_engagement_question(sources)
            else:
                logger.warning(f"Unknown content type: {content_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            return None
            
    async def generate_paper_summary(self, papers: List[Dict]) -> Optional[str]:
        """Generate engaging paper summary."""
        if not papers:
            return None
            
        paper = papers[0]  # Use most recent
        
        prompt = f"""
        Create an engaging tweet summarizing this AI research paper:
        Title: {paper.get('title')}
        Abstract: {paper.get('abstract', '')[:500]}
        
        Rules:
        - Make it exciting and accessible
        - Include key insight or breakthrough
        - Add relevant emojis
        - End with engagement hook (question or call to action)
        - Keep under 280 characters
        - Use clear, simple language
        """
        
        return await self._generate_with_llm(prompt)
        
    async def generate_news_tweet(self, news_items: List[Dict]) -> Optional[str]:
        """Generate tweet about AI news."""
        if not news_items:
            return None
            
        news = news_items[0]
        
        prompt = f"""
        Create an engaging tweet about this AI news:
        {news.get('title')}
        {news.get('description', '')[:300]}
        
        Rules:
        - Focus on why this matters
        - Add your perspective or hot take
        - Include 1-2 relevant hashtags
        - Use emojis strategically
        - Keep under 280 characters
        - Make it shareable
        """
        
        return await self._generate_with_llm(prompt)
        
    async def generate_educational_thread(self, sources: Dict) -> Optional[str]:
        """Generate educational thread starter."""
        prompt = """
        Create the first tweet of an educational thread about a current AI concept or trend.
        
        Rules:
        - Start with a hook that promises value
        - Make it about something trending in AI
        - Format: "🧵 [Hook statement]... Here's what you need to know:"
        - Under 280 characters
        - Make people want to read the thread
        """
        
        return await self._generate_with_llm(prompt)
        
    async def generate_engagement_question(self, sources: Dict) -> Optional[str]:
        """Generate thought-provoking question."""
        prompt = """
        Create a thought-provoking question about AI that will spark discussion.
        
        Rules:
        - Make it relevant to current AI developments
        - Controversial but respectful
        - Easy to have an opinion on
        - End with "What do you think? 👇"
        - Under 280 characters
        """
        
        return await self._generate_with_llm(prompt)
        
    async def _generate_with_llm(self, prompt: str) -> Optional[str]:
        """Generate content using OpenAI API."""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI tech news expert creating engaging Twitter content."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return None
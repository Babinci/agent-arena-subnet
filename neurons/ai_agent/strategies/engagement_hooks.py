import logging
from typing import Dict, List
import random

logger = logging.getLogger(__name__)


class EngagementHookStrategy:
    """Strategy for creating high-engagement content."""
    
    @staticmethod
    def create_thought_question(topic: str) -> str:
        """Create thought-provoking questions."""
        templates = [
            f"If {topic} becomes reality, what job would you want AI to do for you first?",
            f"Controversial: Is {topic} actually progress or are we solving the wrong problem?",
            f"Quick poll: Will {topic} be mainstream in 2 years or 10 years? 🤔",
            f"Honest question: Does {topic} excite you or concern you more? Why?",
            f"What's the most underrated aspect of {topic} that nobody talks about?"
        ]
        
        return random.choice(templates)
        
    @staticmethod
    def create_prediction(trend: Dict) -> str:
        """Create bold predictions."""
        templates = [
            f"Prediction: {trend.get('topic')} will make {trend.get('impact')} obsolete by 2026",
            f"Hot take: Everyone studying {trend.get('field')} should pivot to {trend.get('topic')} NOW",
            f"In 5 years, we'll look back at {trend.get('current')} the way we look at dial-up internet today",
            f"Mark my words: {trend.get('topic')} is the next trillion-dollar industry"
        ]
        
        return random.choice(templates)
        
    @staticmethod
    def create_comparison(item1: str, item2: str) -> str:
        """Create engaging comparisons."""
        templates = [
            f"{item1} vs {item2} - which will have more impact on AI? 🥊",
            f"Unpopular opinion: {item1} > {item2} for real-world applications",
            f"Thread: Why comparing {item1} to {item2} misses the point entirely",
            f"The {item1} vs {item2} debate is actually about something much deeper..."
        ]
        
        return random.choice(templates)
        
    @staticmethod
    def add_engagement_elements(base_tweet: str) -> str:
        """Add elements that boost engagement."""
        elements = {
            'emoji_hooks': ['🤯', '👀', '🔥', '💡', '🚀', '⚡'],
            'cta_endings': [
                "\n\nAgree or disagree? 👇",
                "\n\nWhat's your take?",
                "\n\nRT if you agree, reply if you don't",
                "\n\nDrop your thoughts below 💭",
                "\n\nWho else sees this coming?"
            ],
            'urgency_words': [
                "Breaking:", "Just in:", "HUGE:", "This changes everything:"
            ]
        }
        
        # Add emoji at start if not present
        if not any(emoji in base_tweet[:5] for emoji in elements['emoji_hooks']):
            base_tweet = f"{random.choice(elements['emoji_hooks'])} {base_tweet}"
            
        # Add CTA if not present
        if not any(cta in base_tweet for cta in ['?', '👇', 'thoughts']):
            base_tweet += random.choice(elements['cta_endings'])
            
        return base_tweet
        
    @staticmethod
    def optimize_for_algorithm() -> Dict:
        """Tips for algorithm optimization."""
        return {
            'best_practices': [
                'Ask questions to boost replies',
                'Use 1-2 emojis max for clarity',
                'Keep first line under 100 chars',
                'End with clear CTA',
                'Post threads for dwell time'
            ],
            'avoid': [
                'Too many hashtags (2 max)',
                'Links in first tweet',
                'Generic statements',
                'Complex jargon'
            ],
            'timing': {
                'reply_quickly': True,  # Reply to your own tweets
                'create_discussion': True,
                'quote_tweet': True  # Quote tweet popular posts
            }
        }
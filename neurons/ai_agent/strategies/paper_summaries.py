import logging
from typing import Dict, List, Optional
import re

logger = logging.getLogger(__name__)


class PaperSummaryStrategy:
    """Strategy for creating paper summary tweets."""
    
    @staticmethod
    def extract_key_insight(abstract: str) -> str:
        """Extract the key insight from paper abstract."""
        # Look for result sentences
        result_patterns = [
            r"we achieve[d]? (.*?)[\.]",
            r"our method (.*?)[\.]",
            r"results show[s]? (.*?)[\.]",
            r"we demonstrate[d]? (.*?)[\.]",
            r"improve[s]? (.*?)[\.]"
        ]
        
        for pattern in result_patterns:
            match = re.search(pattern, abstract.lower())
            if match:
                return match.group(1).strip()
                
        # Fallback to first interesting sentence
        sentences = abstract.split('.')
        for sent in sentences:
            if any(word in sent.lower() for word in ['achieve', 'improve', 'novel', 'new']):
                return sent.strip()
                
        return sentences[0].strip() if sentences else ""
        
    @staticmethod
    def create_paper_tweet(paper: Dict) -> Dict:
        """Create engaging paper summary tweet."""
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        authors = paper.get('authors', [])
        
        # Extract key insight
        key_insight = PaperSummaryStrategy.extract_key_insight(abstract)
        
        # Format for different styles
        formats = {
            'breakthrough': {
                'emoji': '🤯',
                'opener': f"Mind-blowing paper alert!",
                'focus': key_insight,
                'cta': "Paper link in comments 👇"
            },
            'educational': {
                'emoji': '📚',
                'opener': f"New research explains:",
                'focus': f"'{title}' - {key_insight}",
                'cta': "Thread explaining the key ideas ⬇️"
            },
            'discussion': {
                'emoji': '🔬',
                'opener': f"Interesting finding from {authors[0].split()[-1] if authors else 'researchers'}:",
                'focus': key_insight,
                'cta': "What are the implications? 🤔"
            }
        }
        
        return formats
        
    @staticmethod
    def create_paper_thread(paper: Dict) -> List[str]:
        """Create educational thread about paper."""
        tweets = []
        
        # Tweet 1: Hook
        tweets.append(
            f"🧵 New paper breakdown: \"{paper.get('title', '')}\"\n\n"
            f"This could change how we approach {PaperSummaryStrategy._extract_topic(paper)}\n\n"
            f"Here's what you need to know:"
        )
        
        # Tweet 2: Problem
        tweets.append(
            f"1/ The Problem:\n"
            f"{PaperSummaryStrategy._extract_problem(paper.get('abstract', ''))}"
        )
        
        # Tweet 3: Solution
        tweets.append(
            f"2/ The Solution:\n"
            f"{PaperSummaryStrategy._extract_solution(paper.get('abstract', ''))}"
        )
        
        # Tweet 4: Results
        tweets.append(
            f"3/ Key Results:\n"
            f"{PaperSummaryStrategy._extract_results(paper.get('abstract', ''))}"
        )
        
        # Tweet 5: Implications
        tweets.append(
            f"4/ Why This Matters:\n"
            f"• Potential applications\n"
            f"• Impact on the field\n"
            f"• What's next\n\n"
            f"Full paper: [link]"
        )
        
        return tweets
        
    @staticmethod
    def _extract_topic(paper: Dict) -> str:
        """Extract main topic from paper."""
        title = paper.get('title', '').lower()
        
        topics = {
            'language model': 'language models',
            'transformer': 'transformer architectures',
            'vision': 'computer vision',
            'reinforcement': 'reinforcement learning',
            'generation': 'generative AI',
            'optimization': 'model optimization'
        }
        
        for keyword, topic in topics.items():
            if keyword in title:
                return topic
                
        return "AI research"
        
    @staticmethod
    def _extract_problem(abstract: str) -> str:
        """Extract problem statement."""
        sentences = abstract.split('.')
        for sent in sentences[:3]:  # Usually in first few sentences
            if any(word in sent.lower() for word in ['however', 'but', 'problem', 'challenge']):
                return sent.strip()
        return "Addressing a key challenge in the field"
        
    @staticmethod
    def _extract_solution(abstract: str) -> str:
        """Extract solution approach."""
        patterns = [
            r"we propose[d]? (.*?)[\.]",
            r"our approach (.*?)[\.]",
            r"we introduce[d]? (.*?)[\.]"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, abstract.lower())
            if match:
                return match.group(1).strip().capitalize()
                
        return "A novel approach to the problem"
        
    @staticmethod
    def _extract_results(abstract: str) -> str:
        """Extract key results."""
        patterns = [
            r"(\d+\.?\d*%?) improvement",
            r"outperform[s]? (.*?) by (\d+\.?\d*%?)",
            r"achieve[s]? state-of-the-art"
        ]
        
        results = []
        for pattern in patterns:
            matches = re.findall(pattern, abstract.lower())
            if matches:
                results.extend(matches)
                
        if results:
            return f"• {results[0]} performance gain\n• State-of-the-art results"
        return "• Significant improvements over baselines"
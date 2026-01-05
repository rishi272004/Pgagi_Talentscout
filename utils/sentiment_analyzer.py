"""
Sentiment Analysis Module (Optional Enhancement)
Gauges candidate emotions during conversation
"""

from typing import Dict, Tuple
from textblob import TextBlob


class SentimentAnalyzer:
    """Analyzes sentiment in candidate responses"""

    @staticmethod
    def analyze_sentiment(text: str) -> Dict:
        """
        Analyze sentiment of given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment metrics
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'sentiment': SentimentAnalyzer._classify_sentiment(polarity),
                'confidence': abs(polarity)
            }
        except Exception as e:
            return {
                'polarity': 0,
                'subjectivity': 0,
                'sentiment': 'neutral',
                'confidence': 0,
                'error': str(e)
            }

    @staticmethod
    def _classify_sentiment(polarity: float) -> str:
        """
        Classify sentiment based on polarity score
        
        Args:
            polarity: Polarity score (-1 to 1)
            
        Returns:
            Sentiment classification
        """
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'

    @staticmethod
    def get_sentiment_indicator(sentiment: str) -> str:
        """Get emoji indicator for sentiment"""
        indicators = {
            'positive': '😊',
            'negative': '😟',
            'neutral': '😐'
        }
        return indicators.get(sentiment, '😐')


import re
from textblob import TextBlob


def analyze_sentiment(text):
    """Simple sentiment analysis with fallback"""
    try:
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    except:
        # Fallback: Count negative words
        negative_words = ['stress', 'overwhelm', 'burnout', 'quit', 'toxic']
        return -0.5 if any(word in text.lower() for word in negative_words) else 0


def extract_topics(text):
    """Extract key topics from text"""
    topics = []
    keyword_groups = {
        'workload': ['workload', 'busy', 'overwork', 'pressure'],
        'manager': ['manager', 'supervisor', 'boss', 'leadership'],
        'pay': ['salary', 'pay', 'compensation', 'bonus'],
        'tools': ['tool', 'software', 'system', 'equipment']
    }

    for topic, keywords in keyword_groups.items():
        if any(re.search(rf'\b{kw}\b', text, re.I) for kw in keywords):
            topics.append(topic)

    return topics
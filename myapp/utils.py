from textblob import TextBlob

from transformers import pipeline


def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def extract_topics(text):

    keywords = ["workload", "manager", "pay", "team", "tools"]
    found_topics = [word for word in keywords if word in text.lower()]
    return found_topics


def analyze_sentiment_advanced(text):
    classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
    return classifier(text)[0]['score'] * (1 if classifier(text)[0]['label'] == 'POSITIVE' else -1)
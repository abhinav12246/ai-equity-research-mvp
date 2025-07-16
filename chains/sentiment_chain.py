from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_sentiment(text):
    result = classifier(text[:512])[0]
    return result['label']

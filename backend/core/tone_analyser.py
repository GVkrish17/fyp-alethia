from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()

EMOTIONAL_KEYWORDS = [
    "sad", "tired", "anxious", "depressed", "don’t know", "don't know", "lost",
    "hurts", "hard", "overwhelmed", "cry", "upset", "sucks", "worthless", "empty"
]

def is_emotional_text(text: str) -> bool:
    text_lower = text.lower()
    for word in EMOTIONAL_KEYWORDS:
        if word in text_lower:
            return True
    return False

def analyze_tone(message: str) -> dict:
    """
    Basic tone analysis of a message using TextBlob and VADER.
    Returns sentiment scores and tone category.
    """

    # TextBlob sentiment
    blob = TextBlob(message)
    polarity = blob.sentiment.polarity # -1 to 1
    subjectivity = blob.sentiment.subjectivity # 0 to 1

    # VADER sentiment
    vader_scores = vader.polarity_scores(message)

    tone = "neutral"
    if is_emotional_text(message):
        tone = "emotional"

    elif vader_scores['compound'] >= 0.5:
        tone = "positive"

    elif vader_scores['compound'] <= -0.5:
        tone = "negative"

    elif subjectivity > 0.7 and polarity < 0:
        tone = "emotional"

    elif polarity < -0.3 and subjectivity > 0.5:
        tone = "emotional"

    return {
        "tone": tone,
        "vader": vader_scores,
        "polarity": polarity,
        "subjectivity": subjectivity,
    }

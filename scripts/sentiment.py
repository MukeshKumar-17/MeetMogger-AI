from textblob import TextBlob
from collections import defaultdict
import re

_POSITIVE_WORDS = {
    "good", "great", "excellent", "happy", "love", "wonderful", "amazing",
    "positive", "pleased", "satisfied", "fantastic", "nice", "awesome", "glad", "enjoy"
}
_NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "sad", "hate", "horrible", "negative", "angry",
    "upset", "disappointed", "poor", "worse", "worst", "unhappy", "annoyed"
}

def _build_highlight(sentence_text):
    """Return highlights and a markdown string with important words bolded."""
    if not sentence_text:
        return {"highlights": [], "highlighted_text": sentence_text}

    highlights = []
    def _collect(word_set, polarity_label):
        for w in word_set:
            for m in re.finditer(rf"\b{re.escape(w)}\b", sentence_text, flags=re.IGNORECASE):
                highlights.append({
                    "word": sentence_text[m.start():m.end()],
                    "polarity": polarity_label,
                    "start": m.start(),
                    "end": m.end(),
                })

    _collect(_POSITIVE_WORDS, "Positive")
    _collect(_NEGATIVE_WORDS, "Negative")

    if not highlights:
        return {"highlights": [], "highlighted_text": sentence_text}

    # Build bolded text without overlapping replacements
    highlights.sort(key=lambda h: h["start"])  # by start index
    pieces = []
    cursor = 0
    for h in highlights:
        if h["start"] < cursor:
            continue
        pieces.append(sentence_text[cursor:h["start"]])
        pieces.append(f"**{sentence_text[h['start']:h['end']]}**")
        cursor = h["end"]
    pieces.append(sentence_text[cursor:])
    return {"highlights": highlights, "highlighted_text": "".join(pieces)}

def analyze_sentiment(text):
    """Analyze sentiment of the given text safely.
    Handles empty or non-string inputs and iterates sentences robustly.
    """
    # Validate input type
    if text is None:
        return {
            "overall": "Neutral",
            "score": 0.0,
            "sentences": [],
            "error": "Transcript is None."
        }

    if not isinstance(text, str):
        return {
            "overall": "Neutral",
            "score": 0.0,
            "sentences": [],
            "error": f"Transcript must be a string, received {type(text).__name__}."
        }

    cleaned = text.strip()
    if not cleaned:
        return {
            "overall": "Neutral",
            "score": 0.0,
            "sentences": [],
            "error": "Transcript is empty."
        }

    blob = TextBlob(cleaned)
    sentiment_score = blob.sentiment.polarity

    if sentiment_score > 0.1:
        overall = "Positive"
    elif sentiment_score < -0.1:
        overall = "Negative"
    else:
        overall = "Neutral"

    # Build per-sentence analysis, falling back to whole text if sentence parsing yields none
    sentences = list(blob.sentences)
    if not sentences:
        sentences = [TextBlob(cleaned)]

    per_sentence = []
    for s in sentences:
        text_s = str(s)
        pol = float(s.sentiment.polarity)
        label = "Positive" if pol > 0 else ("Negative" if pol < 0 else "Neutral")
        hl = _build_highlight(text_s)
        per_sentence.append({
            "text": text_s,
            "sentiment": label,
            "polarity": pol,
            "highlights": hl["highlights"],
            "highlighted_text": hl["highlighted_text"],
            "is_important": abs(pol) >= 0.2 or bool(hl["highlights"]),
        })

    return {
        "overall": overall,
        "score": float(sentiment_score),
        "sentences": per_sentence,
    }
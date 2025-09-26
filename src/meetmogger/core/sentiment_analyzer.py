"""
Advanced sentiment analysis using VADER and TextBlob.

Provides comprehensive sentiment analysis with sentence-level insights
and professional visualization capabilities.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

from ..utils.logger import get_logger
from ..utils.validators import validate_transcript

logger = get_logger(__name__)


@dataclass
class SentimentResult:
    """Data class for sentiment analysis results."""
    overall: str
    score: float
    confidence: float
    sentences: List[Dict[str, Any]]
    summary: Dict[str, Any]


class SentimentAnalyzer:
    """
    Advanced sentiment analyzer using VADER and TextBlob.
    
    Provides comprehensive sentiment analysis with sentence-level insights,
    confidence scoring, and professional visualization capabilities.
    """
    
    def __init__(self, use_vader: bool = True, use_textblob: bool = True):
        """
        Initialize sentiment analyzer.
        
        Args:
            use_vader: Whether to use VADER sentiment analysis
            use_textblob: Whether to use TextBlob sentiment analysis
        """
        self.use_vader = use_vader
        self.use_textblob = use_textblob
        
        if use_vader:
            self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Sentiment word sets for highlighting
        self.positive_words = {
            "good", "great", "excellent", "happy", "love", "wonderful", "amazing",
            "positive", "pleased", "satisfied", "fantastic", "nice", "awesome", 
            "glad", "enjoy", "perfect", "outstanding", "brilliant", "superb",
            "delighted", "thrilled", "excited", "optimistic", "confident"
        }
        
        self.negative_words = {
            "bad", "terrible", "awful", "sad", "hate", "horrible", "negative", 
            "angry", "upset", "disappointed", "poor", "worse", "worst", 
            "unhappy", "annoyed", "frustrated", "concerned", "worried", 
            "disappointed", "frustrated", "angry", "upset", "terrible"
        }
        
        self.intensity_words = {
            "very", "extremely", "incredibly", "absolutely", "completely",
            "totally", "really", "quite", "rather", "somewhat", "slightly"
        }
    
    def analyze(self, text: str) -> SentimentResult:
        """
        Perform comprehensive sentiment analysis.
        
        Args:
            text: Input text to analyze
            
        Returns:
            SentimentResult object with analysis results
        """
        # Validate input
        validation = validate_transcript(text)
        if not validation["is_valid"]:
            logger.warning(f"Invalid transcript: {validation['error']}")
            return self._create_empty_result(validation["error"])
        
        cleaned_text = validation["transcript"]
        
        try:
            # Get sentence-level analysis
            sentences = self._extract_sentences(cleaned_text)
            sentence_results = []
            
            for sentence in sentences:
                sentence_analysis = self._analyze_sentence(sentence)
                sentence_results.append(sentence_analysis)
            
            # Calculate overall sentiment
            overall_sentiment = self._calculate_overall_sentiment(sentence_results)
            
            # Create summary statistics
            summary = self._create_summary(sentence_results)
            
            logger.info(f"Sentiment analysis completed: {overall_sentiment['overall']} "
                       f"(score: {overall_sentiment['score']:.3f})")
            
            return SentimentResult(
                overall=overall_sentiment["overall"],
                score=overall_sentiment["score"],
                confidence=overall_sentiment["confidence"],
                sentences=sentence_results,
                summary=summary
            )
            
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return self._create_empty_result(f"Analysis error: {str(e)}")
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text."""
        # Use TextBlob for sentence tokenization
        blob = TextBlob(text)
        sentences = [str(sentence).strip() for sentence in blob.sentences]
        
        # Filter out very short sentences
        return [s for s in sentences if len(s.split()) >= 3]
    
    def _analyze_sentence(self, sentence: str) -> Dict[str, Any]:
        """Analyze individual sentence sentiment."""
        result = {
            "text": sentence,
            "sentiment": "Neutral",
            "polarity": 0.0,
            "confidence": 0.0,
            "highlights": [],
            "highlighted_text": sentence,
            "is_important": False,
            "vader_scores": {},
            "textblob_scores": {}
        }
        
        try:
            # VADER analysis
            if self.use_vader:
                vader_scores = self.vader_analyzer.polarity_scores(sentence)
                result["vader_scores"] = vader_scores
                vader_compound = vader_scores["compound"]
            else:
                vader_compound = 0.0
            
            # TextBlob analysis
            if self.use_textblob:
                blob = TextBlob(sentence)
                textblob_polarity = blob.sentiment.polarity
                textblob_subjectivity = blob.sentiment.subjectivity
                result["textblob_scores"] = {
                    "polarity": textblob_polarity,
                    "subjectivity": textblob_subjectivity
                }
            else:
                textblob_polarity = 0.0
            
            # Combine scores (weighted average)
            if self.use_vader and self.use_textblob:
                # VADER is generally more accurate for social media text
                combined_score = (vader_compound * 0.7) + (textblob_polarity * 0.3)
            elif self.use_vader:
                combined_score = vader_compound
            else:
                combined_score = textblob_polarity
            
            # Determine sentiment label
            if combined_score >= 0.05:
                sentiment = "Positive"
            elif combined_score <= -0.05:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            
            # Calculate confidence
            confidence = abs(combined_score)
            
            # Generate highlights
            highlights = self._generate_highlights(sentence)
            
            # Determine if sentence is important
            is_important = (
                confidence >= 0.3 or 
                len(highlights) > 0 or 
                any(word in sentence.lower() for word in ["action", "next", "follow", "deadline", "urgent"])
            )
            
            result.update({
                "sentiment": sentiment,
                "polarity": combined_score,
                "confidence": confidence,
                "highlights": highlights,
                "highlighted_text": self._create_highlighted_text(sentence, highlights),
                "is_important": is_important
            })
            
        except Exception as e:
            logger.error(f"Error analyzing sentence: {e}")
            result["error"] = str(e)
        
        return result
    
    def _generate_highlights(self, text: str) -> List[Dict[str, Any]]:
        """Generate word highlights for sentiment analysis."""
        highlights = []
        text_lower = text.lower()
        
        # Find positive words
        for word in self.positive_words:
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                highlights.append({
                    "word": text[match.start():match.end()],
                    "polarity": "Positive",
                    "start": match.start(),
                    "end": match.end(),
                    "intensity": self._get_word_intensity(text, match.start(), match.end())
                })
        
        # Find negative words
        for word in self.negative_words:
            for match in re.finditer(rf'\b{re.escape(word)}\b', text_lower):
                highlights.append({
                    "word": text[match.start():match.end()],
                    "polarity": "Negative",
                    "start": match.start(),
                    "end": match.end(),
                    "intensity": self._get_word_intensity(text, match.start(), match.end())
                })
        
        # Sort by position
        highlights.sort(key=lambda x: x["start"])
        
        return highlights
    
    def _get_word_intensity(self, text: str, start: int, end: int) -> str:
        """Determine intensity of sentiment word."""
        # Check for intensity modifiers before the word
        before_text = text[max(0, start-20):start].lower()
        for intensity_word in self.intensity_words:
            if intensity_word in before_text:
                return "High"
        return "Medium"
    
    def _create_highlighted_text(self, text: str, highlights: List[Dict[str, Any]]) -> str:
        """Create highlighted text with bold formatting."""
        if not highlights:
            return text
        
        # Sort highlights by position and avoid overlaps
        highlights.sort(key=lambda x: x["start"])
        result_parts = []
        last_end = 0
        
        for highlight in highlights:
            if highlight["start"] < last_end:
                continue
            
            # Add text before highlight
            result_parts.append(text[last_end:highlight["start"]])
            
            # Add highlighted word
            word = highlight["word"]
            polarity = highlight["polarity"]
            intensity = highlight.get("intensity", "Medium")
            
            if intensity == "High":
                result_parts.append(f"**{word}**")
            else:
                result_parts.append(f"**{word}**")
            
            last_end = highlight["end"]
        
        # Add remaining text
        result_parts.append(text[last_end:])
        
        return "".join(result_parts)
    
    def _calculate_overall_sentiment(self, sentence_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall sentiment from sentence results."""
        if not sentence_results:
            return {"overall": "Neutral", "score": 0.0, "confidence": 0.0}
        
        # Weighted average by confidence
        total_weight = 0
        weighted_score = 0
        
        for result in sentence_results:
            if "polarity" in result and "confidence" in result:
                weight = result["confidence"]
                weighted_score += result["polarity"] * weight
                total_weight += weight
        
        if total_weight == 0:
            return {"overall": "Neutral", "score": 0.0, "confidence": 0.0}
        
        avg_score = weighted_score / total_weight
        avg_confidence = total_weight / len(sentence_results)
        
        if avg_score >= 0.05:
            overall = "Positive"
        elif avg_score <= -0.05:
            overall = "Negative"
        else:
            overall = "Neutral"
        
        return {
            "overall": overall,
            "score": avg_score,
            "confidence": min(avg_confidence, 1.0)
        }
    
    def _create_summary(self, sentence_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create summary statistics."""
        if not sentence_results:
            return {}
        
        sentiments = [r.get("sentiment", "Neutral") for r in sentence_results]
        polarities = [r.get("polarity", 0.0) for r in sentence_results]
        confidences = [r.get("confidence", 0.0) for r in sentence_results]
        
        # Count sentiments
        sentiment_counts = {
            "Positive": sentiments.count("Positive"),
            "Negative": sentiments.count("Negative"),
            "Neutral": sentiments.count("Neutral")
        }
        
        # Calculate statistics
        return {
            "total_sentences": len(sentence_results),
            "sentiment_distribution": sentiment_counts,
            "average_polarity": sum(polarities) / len(polarities),
            "average_confidence": sum(confidences) / len(confidences),
            "max_polarity": max(polarities),
            "min_polarity": min(polarities),
            "important_sentences": sum(1 for r in sentence_results if r.get("is_important", False))
        }
    
    def _create_empty_result(self, error: str) -> SentimentResult:
        """Create empty result for error cases."""
        return SentimentResult(
            overall="Neutral",
            score=0.0,
            confidence=0.0,
            sentences=[],
            summary={"error": error}
        )
    
    def get_sentiment_distribution_chart_data(self, result: SentimentResult) -> Dict[str, Any]:
        """Get data for sentiment distribution chart."""
        if not result.summary or "sentiment_distribution" not in result.summary:
            return {}
        
        distribution = result.summary["sentiment_distribution"]
        return {
            "labels": list(distribution.keys()),
            "values": list(distribution.values()),
            "colors": ["#28a745", "#dc3545", "#6c757d"]  # Green, Red, Gray
        }

"""
Unit tests for SentimentAnalyzer.

Tests the sentiment analysis functionality with various input scenarios.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from meetmogger.core.sentiment_analyzer import SentimentAnalyzer


class TestSentimentAnalyzer:
    """Test cases for SentimentAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = SentimentAnalyzer()
    
    def test_analyze_positive_text(self):
        """Test analysis of positive text."""
        text = "This is a great solution! I'm very happy with the results."
        result = self.analyzer.analyze(text)
        
        assert result.overall == "Positive"
        assert result.score > 0
        assert result.confidence > 0
        assert len(result.sentences) > 0
    
    def test_analyze_negative_text(self):
        """Test analysis of negative text."""
        text = "This is terrible! I'm very disappointed with the service."
        result = self.analyzer.analyze(text)
        
        assert result.overall == "Negative"
        assert result.score < 0
        assert result.confidence > 0
        assert len(result.sentences) > 0
    
    def test_analyze_neutral_text(self):
        """Test analysis of neutral text."""
        text = "The meeting was scheduled for tomorrow at 2 PM."
        result = self.analyzer.analyze(text)
        
        assert result.overall == "Neutral"
        assert abs(result.score) < 0.1
        assert len(result.sentences) > 0
    
    def test_analyze_empty_text(self):
        """Test analysis of empty text."""
        result = self.analyzer.analyze("")
        
        assert result.overall == "Neutral"
        assert result.score == 0.0
        assert result.confidence == 0.0
        assert len(result.sentences) == 0
    
    def test_analyze_none_input(self):
        """Test analysis of None input."""
        result = self.analyzer.analyze(None)
        
        assert result.overall == "Neutral"
        assert result.score == 0.0
        assert result.confidence == 0.0
        assert len(result.sentences) == 0
    
    def test_analyze_invalid_input(self):
        """Test analysis of invalid input type."""
        result = self.analyzer.analyze(123)
        
        assert result.overall == "Neutral"
        assert result.score == 0.0
        assert result.confidence == 0.0
        assert len(result.sentences) == 0
    
    def test_sentence_analysis(self):
        """Test sentence-level analysis."""
        text = "This is great! But there are some issues. Overall, it's okay."
        result = self.analyzer.analyze(text)
        
        assert len(result.sentences) >= 3
        assert any(s["sentiment"] == "Positive" for s in result.sentences)
        assert any(s["sentiment"] == "Negative" for s in result.sentences)
    
    def test_highlight_generation(self):
        """Test keyword highlighting."""
        text = "This is a great solution with excellent features!"
        result = self.analyzer.analyze(text)
        
        # Check that highlights are generated
        for sentence in result.sentences:
            if "great" in sentence["text"].lower() or "excellent" in sentence["text"].lower():
                assert len(sentence["highlights"]) > 0
                assert "**" in sentence["highlighted_text"]
    
    def test_confidence_calculation(self):
        """Test confidence score calculation."""
        text = "I absolutely love this amazing solution!"
        result = self.analyzer.analyze(text)
        
        assert result.confidence > 0
        assert result.confidence <= 1.0
    
    def test_summary_creation(self):
        """Test summary statistics creation."""
        text = "Great! This is wonderful. But there are some problems. Overall, it's good."
        result = self.analyzer.analyze(text)
        
        assert "sentiment_distribution" in result.summary
        assert "total_sentences" in result.summary
        assert "average_polarity" in result.summary

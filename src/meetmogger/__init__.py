"""
MeetMogger AI - Call Transcript Intelligence Platform

A production-ready solution for analyzing call transcripts with sentiment analysis,
insight extraction, and actionable intelligence.
"""

__version__ = "1.0.0"
__author__ = "MeetMogger AI Team"
__email__ = "contact@meetmogger.ai"

from .core.sentiment_analyzer import SentimentAnalyzer
from .core.insight_extractor import InsightExtractor
from .core.transcript_processor import TranscriptProcessor

__all__ = [
    "SentimentAnalyzer",
    "InsightExtractor", 
    "TranscriptProcessor",
]

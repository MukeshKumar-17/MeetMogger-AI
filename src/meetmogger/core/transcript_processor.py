"""
Transcript processing and preprocessing utilities.

Handles transcript cleaning, normalization, and preparation for analysis.
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from ..utils.logger import get_logger
from ..utils.validators import validate_transcript

logger = get_logger(__name__)


@dataclass
class ProcessedTranscript:
    """Data class for processed transcript."""
    original_text: str
    cleaned_text: str
    sentences: List[str]
    speakers: List[str]
    metadata: Dict[str, Any]


class TranscriptProcessor:
    """
    Advanced transcript processor with cleaning and normalization.
    
    Provides comprehensive transcript preprocessing including speaker
    identification, noise removal, and text normalization.
    """
    
    def __init__(self):
        """Initialize transcript processor."""
        self.speaker_patterns = [
            r'^([A-Z][a-zA-Z\s]+):\s*',  # "Speaker Name:"
            r'^([A-Z][A-Z\s]+):\s*',     # "SPEAKER NAME:"
            r'^([A-Z][a-z]+):\s*',       # "Speaker:"
            r'^([A-Z]+):\s*',            # "SPEAKER:"
        ]
        
        # Common noise patterns
        self.noise_patterns = [
            r'\[.*?\]',  # [background noise]
            r'\(.*?\)',  # (unclear)
            r'<.*?>',    # <inaudible>
            r'\.\.\.+',  # Multiple dots
            r'--+',      # Multiple dashes
            r'__+',      # Multiple underscores
        ]
    
    def process(self, text: str) -> ProcessedTranscript:
        """
        Process transcript with comprehensive cleaning and normalization.
        
        Args:
            text: Raw transcript text
            
        Returns:
            ProcessedTranscript object with cleaned data
        """
        # Validate input
        validation = validate_transcript(text)
        if not validation["is_valid"]:
            logger.warning(f"Invalid transcript: {validation['error']}")
            return self._create_empty_result(text, validation["error"])
        
        original_text = validation["transcript"]
        
        try:
            # Clean and normalize text
            cleaned_text = self._clean_text(original_text)
            
            # Extract sentences
            sentences = self._extract_sentences(cleaned_text)
            
            # Extract speakers
            speakers = self._extract_speakers(cleaned_text)
            
            # Create metadata
            metadata = self._create_metadata(original_text, cleaned_text, sentences, speakers)
            
            logger.info(f"Processed transcript: {len(sentences)} sentences, {len(speakers)} speakers")
            
            return ProcessedTranscript(
                original_text=original_text,
                cleaned_text=cleaned_text,
                sentences=sentences,
                speakers=speakers,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Transcript processing error: {e}")
            return self._create_empty_result(original_text, f"Processing error: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize transcript text."""
        # Remove noise patterns
        cleaned = text
        for pattern in self.noise_patterns:
            cleaned = re.sub(pattern, '', cleaned)
        
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove extra punctuation
        cleaned = re.sub(r'([.!?])\s*([.!?])+', r'\1', cleaned)
        
        # Fix common transcript issues
        cleaned = self._fix_common_issues(cleaned)
        
        return cleaned.strip()
    
    def _fix_common_issues(self, text: str) -> str:
        """Fix common transcript formatting issues."""
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.!?,:;])', r'\1', text)
        text = re.sub(r'([.!?,:;])([A-Z])', r'\1 \2', text)
        
        # Fix common word issues
        fixes = {
            r'\buh\b': '',
            r'\bum\b': '',
            r'\ber\b': '',
            r'\bwell\s+well\b': 'well',
            r'\byeah\s+yeah\b': 'yeah',
            r'\bokay\s+okay\b': 'okay',
        }
        
        for pattern, replacement in fixes.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from cleaned text."""
        # Split by sentence endings
        sentences = re.split(r'[.!?]+', text)
        
        # Clean and filter sentences
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Filter out very short fragments
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def _extract_speakers(self, text: str) -> List[str]:
        """Extract unique speakers from transcript."""
        speakers = set()
        lines = text.split('\n')
        
        for line in lines:
            for pattern in self.speaker_patterns:
                match = re.match(pattern, line)
                if match:
                    speaker = match.group(1).strip()
                    if len(speaker) > 1:  # Filter out single characters
                        speakers.add(speaker)
                    break
        
        return sorted(list(speakers))
    
    def _create_metadata(self, original: str, cleaned: str, sentences: List[str], speakers: List[str]) -> Dict[str, Any]:
        """Create metadata for processed transcript."""
        return {
            "original_length": len(original),
            "cleaned_length": len(cleaned),
            "sentence_count": len(sentences),
            "speaker_count": len(speakers),
            "average_sentence_length": sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0,
            "word_count": len(cleaned.split()),
            "speakers": speakers,
            "processing_timestamp": "2024-01-01T00:00:00Z"  # Would use actual timestamp in production
        }
    
    def _create_empty_result(self, original_text: str, error: str) -> ProcessedTranscript:
        """Create empty result for error cases."""
        return ProcessedTranscript(
            original_text=original_text,
            cleaned_text="",
            sentences=[],
            speakers=[],
            metadata={"error": error}
        )

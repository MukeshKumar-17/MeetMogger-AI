"""
Unit tests for TranscriptProcessor.

Tests the transcript processing and preprocessing functionality.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from meetmogger.core.transcript_processor import TranscriptProcessor


class TestTranscriptProcessor:
    """Test cases for TranscriptProcessor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = TranscriptProcessor()
    
    def test_process_valid_transcript(self):
        """Test processing of valid transcript."""
        text = "Speaker 1: Hello, how are you?\nSpeaker 2: I'm doing well, thank you!"
        result = self.processor.process(text)
        
        assert result.original_text == text
        assert len(result.cleaned_text) > 0
        assert len(result.sentences) > 0
        assert len(result.speakers) > 0
        assert "sentence_count" in result.metadata
    
    def test_process_empty_text(self):
        """Test processing of empty text."""
        result = self.processor.process("")
        
        assert result.original_text == ""
        assert result.cleaned_text == ""
        assert len(result.sentences) == 0
        assert len(result.speakers) == 0
        assert "error" in result.metadata
    
    def test_process_none_input(self):
        """Test processing of None input."""
        result = self.processor.process(None)
        
        assert result.original_text is None
        assert "error" in result.metadata
    
    def test_speaker_extraction(self):
        """Test speaker extraction from transcript."""
        text = """
        John: Hello everyone!
        Mary: Hi John, how are you?
        John: I'm doing great, thanks for asking.
        """
        result = self.processor.process(text)
        
        assert "John" in result.speakers
        assert "Mary" in result.speakers
        assert len(result.speakers) == 2
    
    def test_sentence_extraction(self):
        """Test sentence extraction from transcript."""
        text = "This is sentence one. This is sentence two! This is sentence three?"
        result = self.processor.process(text)
        
        assert len(result.sentences) == 3
        assert "This is sentence one" in result.sentences
        assert "This is sentence two" in result.sentences
        assert "This is sentence three" in result.sentences
    
    def test_noise_removal(self):
        """Test removal of noise patterns."""
        text = "Hello [background noise] how are you? (unclear) I'm fine."
        result = self.processor.process(text)
        
        assert "[background noise]" not in result.cleaned_text
        assert "(unclear)" not in result.cleaned_text
        assert "Hello how are you" in result.cleaned_text
    
    def test_whitespace_normalization(self):
        """Test normalization of whitespace."""
        text = "Hello    world!\n\nThis   is   a   test."
        result = self.processor.process(text)
        
        assert "   " not in result.cleaned_text
        assert "\n\n" not in result.cleaned_text
    
    def test_common_issues_fixing(self):
        """Test fixing of common transcript issues."""
        text = "Hello world ! This is a test ."
        result = self.processor.process(text)
        
        assert "world !" not in result.cleaned_text
        assert "test ." not in result.cleaned_text
    
    def test_metadata_creation(self):
        """Test metadata creation."""
        text = "Speaker 1: Hello world!\nSpeaker 2: Hi there!"
        result = self.processor.process(text)
        
        assert "original_length" in result.metadata
        assert "cleaned_length" in result.metadata
        assert "sentence_count" in result.metadata
        assert "speaker_count" in result.metadata
        assert "word_count" in result.metadata
        assert "speakers" in result.metadata
    
    def test_short_sentence_filtering(self):
        """Test filtering of very short sentences."""
        text = "Hi. This is a longer sentence. OK. Another long sentence here."
        result = self.processor.process(text)
        
        # Should filter out "Hi" and "OK" as they're too short
        assert "Hi" not in result.sentences
        assert "OK" not in result.sentences
        assert "This is a longer sentence" in result.sentences
    
    def test_error_handling(self):
        """Test error handling during processing."""
        # This would test various error conditions
        # For now, we'll test with a simple case
        text = "Normal text here."
        result = self.processor.process(text)
        
        # Should not have errors for normal text
        assert "error" not in result.metadata

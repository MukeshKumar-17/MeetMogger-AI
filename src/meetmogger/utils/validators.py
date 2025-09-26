"""
Validation utilities for MeetMogger AI.

Provides input validation and sanitization functions.
"""

import re
from typing import Any, Dict, List, Optional, Union


def validate_transcript(transcript: Any) -> Dict[str, Any]:
    """
    Validate and sanitize transcript input.
    
    Args:
        transcript: Input transcript (string, dict, or other)
        
    Returns:
        Dictionary with validation results and cleaned transcript
    """
    result = {
        "is_valid": False,
        "transcript": "",
        "error": None,
        "warnings": []
    }
    
    # Handle None input
    if transcript is None:
        result["error"] = "Transcript cannot be None"
        return result
    
    # Handle non-string types
    if not isinstance(transcript, str):
        if isinstance(transcript, dict) and "text" in transcript:
            transcript = transcript["text"]
        else:
            result["error"] = f"Transcript must be a string, received {type(transcript).__name__}"
            return result
    
    # Clean and validate string
    cleaned = transcript.strip()
    
    if not cleaned:
        result["error"] = "Transcript is empty"
        return result
    
    if len(cleaned) < 10:
        result["warnings"].append("Transcript is very short (less than 10 characters)")
    
    if len(cleaned) > 50000:
        result["warnings"].append("Transcript is very long (over 50,000 characters)")
    
    # Basic content validation
    if not re.search(r'[a-zA-Z]', cleaned):
        result["error"] = "Transcript contains no alphabetic characters"
        return result
    
    # Check for reasonable sentence structure
    sentences = re.split(r'[.!?]+', cleaned)
    if len(sentences) < 2:
        result["warnings"].append("Transcript appears to have no sentence breaks")
    
    result["is_valid"] = True
    result["transcript"] = cleaned
    
    return result


def validate_file_upload(file_content: bytes, file_type: str) -> Dict[str, Any]:
    """
    Validate uploaded file content and type.
    
    Args:
        file_content: Raw file content
        file_type: MIME type or file extension
        
    Returns:
        Dictionary with validation results
    """
    result = {
        "is_valid": False,
        "content": "",
        "error": None,
        "file_type": file_type
    }
    
    if not file_content:
        result["error"] = "File is empty"
        return result
    
    if len(file_content) > 10 * 1024 * 1024:  # 10MB limit
        result["error"] = "File too large (max 10MB)"
        return result
    
    # Validate file type
    allowed_types = {
        "text/plain": [".txt"],
        "application/pdf": [".pdf"],
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
        "text/csv": [".csv"]
    }
    
    if file_type not in allowed_types:
        result["error"] = f"Unsupported file type: {file_type}"
        return result
    
    result["is_valid"] = True
    return result


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing potentially harmful characters.
    
    Args:
        text: Input text to sanitize
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove control characters except newlines and tabs
    sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normalize whitespace
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    return sanitized.strip()


def validate_insight_data(insights: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Validate insight extraction results.
    
    Args:
        insights: Dictionary with problems, solutions, action_items
        
    Returns:
        Validation results
    """
    result = {
        "is_valid": True,
        "errors": [],
        "warnings": []
    }
    
    required_keys = ["problems", "solutions", "action_items"]
    
    for key in required_keys:
        if key not in insights:
            result["errors"].append(f"Missing required key: {key}")
            result["is_valid"] = False
        elif not isinstance(insights[key], list):
            result["errors"].append(f"Key '{key}' must be a list")
            result["is_valid"] = False
    
    if result["is_valid"]:
        total_insights = sum(len(insights[key]) for key in required_keys)
        if total_insights == 0:
            result["warnings"].append("No insights extracted from transcript")
    
    return result

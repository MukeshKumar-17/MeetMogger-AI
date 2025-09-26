"""
File handling utilities for MeetMogger AI.

Provides robust file upload, processing, and export functionality.
"""

import io
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd
from docx import Document
from PyPDF2 import PdfReader

from .logger import get_logger
from .validators import validate_file_upload

logger = get_logger(__name__)


class FileHandler:
    """Handles file operations for transcript processing."""
    
    def __init__(self, upload_dir: str = "uploads", output_dir: str = "outputs"):
        """
        Initialize file handler.
        
        Args:
            upload_dir: Directory for uploaded files
            output_dir: Directory for output files
        """
        self.upload_dir = Path(upload_dir)
        self.output_dir = Path(output_dir)
        self.upload_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    def process_uploaded_file(
        self, 
        file_content: bytes, 
        file_type: str,
        filename: str = "uploaded_file"
    ) -> Dict[str, Any]:
        """
        Process uploaded file and extract text content.
        
        Args:
            file_content: Raw file content
            file_type: MIME type or file extension
            filename: Original filename
            
        Returns:
            Dictionary with processing results
        """
        result = {
            "success": False,
            "content": "",
            "error": None,
            "file_type": file_type,
            "filename": filename
        }
        
        try:
            # Validate file
            validation = validate_file_upload(file_content, file_type)
            if not validation["is_valid"]:
                result["error"] = validation["error"]
                return result
            
            # Extract text based on file type
            if file_type == "text/plain" or filename.endswith(".txt"):
                content = self._extract_from_txt(file_content)
            elif file_type == "application/pdf" or filename.endswith(".pdf"):
                content = self._extract_from_pdf(file_content)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or filename.endswith(".docx"):
                content = self._extract_from_docx(file_content)
            else:
                result["error"] = f"Unsupported file type: {file_type}"
                return result
            
            if not content.strip():
                result["error"] = "No text content found in file"
                return result
            
            result["success"] = True
            result["content"] = content
            logger.info(f"Successfully processed file: {filename}")
            
        except Exception as e:
            result["error"] = f"Error processing file: {str(e)}"
            logger.error(f"File processing error: {e}")
        
        return result
    
    def _extract_from_txt(self, content: bytes) -> str:
        """Extract text from plain text file."""
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            return content.decode('utf-8', errors='ignore')
    
    def _extract_from_pdf(self, content: bytes) -> str:
        """Extract text from PDF file."""
        try:
            pdf_reader = PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return ""
    
    def _extract_from_docx(self, content: bytes) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(io.BytesIO(content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            logger.error(f"DOCX extraction error: {e}")
            return ""
    
    def save_transcript(self, transcript: str, filename: str = "transcript.json") -> bool:
        """
        Save transcript to JSON file.
        
        Args:
            transcript: Transcript text
            filename: Output filename
            
        Returns:
            Success status
        """
        try:
            file_path = self.output_dir / filename
            data = {
                "text": transcript,
                "metadata": {
                    "created_at": pd.Timestamp.now().isoformat(),
                    "length": len(transcript),
                    "word_count": len(transcript.split())
                }
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Transcript saved to: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving transcript: {e}")
            return False
    
    def load_transcript(self, filename: str = "transcript.json") -> Optional[str]:
        """
        Load transcript from JSON file.
        
        Args:
            filename: Input filename
            
        Returns:
            Transcript text or None if error
        """
        try:
            file_path = self.output_dir / filename
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return data.get("text", "")
            
        except Exception as e:
            logger.error(f"Error loading transcript: {e}")
            return None
    
    def export_to_csv(
        self, 
        data: List[Dict[str, Any]], 
        filename: str = "export.csv"
    ) -> Optional[bytes]:
        """
        Export data to CSV format.
        
        Args:
            data: List of dictionaries to export
            filename: Output filename
            
        Returns:
            CSV content as bytes or None if error
        """
        try:
            if not data:
                return None
            
            df = pd.DataFrame(data)
            csv_content = df.to_csv(index=False)
            return csv_content.encode('utf-8')
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            return None
    
    def export_to_json(
        self, 
        data: Dict[str, Any], 
        filename: str = "export.json"
    ) -> Optional[bytes]:
        """
        Export data to JSON format.
        
        Args:
            data: Dictionary to export
            filename: Output filename
            
        Returns:
            JSON content as bytes or None if error
        """
        try:
            json_content = json.dumps(data, indent=2, ensure_ascii=False)
            return json_content.encode('utf-8')
            
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            return None

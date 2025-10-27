"""
Response Parser
Parses and validates responses from custom LLM model
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ResponseParser:
    """
    Parses and validates LLM model responses
    """
    
    def parse_outline(self, response: str) -> Dict[str, Any]:
        """
        Parse book outline from model response
        
        Args:
            response: Raw model response
        
        Returns:
            Structured outline dict
        """
        try:
            # Extract title
            title_match = re.search(r'TITLE:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "Untitled Book"
            
            # Extract chapters
            chapters = []
            chapter_pattern = r'(\d+)\.\s*([^\n-]+?)(?:\s*-\s*([^\n]+))?(?:\n|$)'
            
            for match in re.finditer(chapter_pattern, response):
                chapter_num = match.group(1)
                chapter_title = match.group(2).strip()
                chapter_desc = match.group(3).strip() if match.group(3) else ""
                
                chapters.append({
                    "number": int(chapter_num),
                    "title": chapter_title,
                    "description": chapter_desc
                })
            
            # Validate we have chapters
            if not chapters:
                logger.warning("No chapters found in outline, using fallback structure")
                chapters = self._generate_fallback_outline()
            
            return {
                "title": title,
                "chapters": chapters,
                "total_chapters": len(chapters)
            }
            
        except Exception as e:
            logger.error(f"Outline parsing error: {str(e)}")
            return {
                "title": "Untitled Book",
                "chapters": self._generate_fallback_outline(),
                "total_chapters": 8
            }
    
    def parse_chapter(self, response: str) -> str:
        """
        Parse chapter content from model response
        
        Args:
            response: Raw model response
        
        Returns:
            Cleaned chapter content
        """
        try:
            # Remove any metadata or system messages
            content = response.strip()
            
            # Remove common prefixes
            prefixes_to_remove = [
                "Here is the chapter:",
                "Chapter content:",
                "Content:",
                "**Chapter**:",
            ]
            
            for prefix in prefixes_to_remove:
                if content.lower().startswith(prefix.lower()):
                    content = content[len(prefix):].strip()
            
            # Clean up excessive whitespace
            content = re.sub(r'\n{3,}', '\n\n', content)
            content = re.sub(r' {2,}', ' ', content)
            
            # Validate minimum length
            if len(content) < 100:
                logger.warning(f"Chapter content too short: {len(content)} characters")
                return self._generate_placeholder_content()
            
            return content
            
        except Exception as e:
            logger.error(f"Chapter parsing error: {str(e)}")
            return self._generate_placeholder_content()
    
    def parse_refinement(self, response: str) -> str:
        """
        Parse refined content from model response
        
        Args:
            response: Raw model response
        
        Returns:
            Cleaned refined content
        """
        try:
            content = response.strip()
            
            # Remove refinement metadata
            prefixes = [
                "Refined version:",
                "Improved content:",
                "Enhanced text:",
                "**Refined Version**:",
            ]
            
            for prefix in prefixes:
                if content.lower().startswith(prefix.lower()):
                    content = content[len(prefix):].strip()
            
            return content
            
        except Exception as e:
            logger.error(f"Refinement parsing error: {str(e)}")
            return response  # Return original if parsing fails
    
    def validate_outline(self, outline: Dict[str, Any]) -> bool:
        """
        Validate outline structure
        
        Args:
            outline: Parsed outline dict
        
        Returns:
            True if valid
        """
        required_keys = ['title', 'chapters', 'total_chapters']
        
        # Check required keys exist
        if not all(key in outline for key in required_keys):
            logger.warning("Outline missing required keys")
            return False
        
        # Validate chapters
        if not isinstance(outline['chapters'], list):
            logger.warning("Chapters is not a list")
            return False
        
        if len(outline['chapters']) < 5:
            logger.warning(f"Too few chapters: {len(outline['chapters'])}")
            return False
        
        # Validate each chapter has required fields
        for chapter in outline['chapters']:
            if not all(key in chapter for key in ['number', 'title']):
                logger.warning(f"Invalid chapter structure: {chapter}")
                return False
        
        return True
    
    def _generate_fallback_outline(self) -> List[Dict[str, Any]]:
        """Generate fallback outline if parsing fails"""
        return [
            {"number": 1, "title": "Introduction", "description": "Overview and context"},
            {"number": 2, "title": "Fundamentals", "description": "Core concepts and basics"},
            {"number": 3, "title": "Key Principles", "description": "Essential principles"},
            {"number": 4, "title": "Practical Applications", "description": "Real-world examples"},
            {"number": 5, "title": "Best Practices", "description": "Proven strategies"},
            {"number": 6, "title": "Common Challenges", "description": "Troubleshooting guide"},
            {"number": 7, "title": "Advanced Topics", "description": "In-depth exploration"},
            {"number": 8, "title": "Conclusion", "description": "Summary and next steps"}
        ]
    
    def _generate_placeholder_content(self) -> str:
        """Generate placeholder content if generation fails"""
        return """This chapter provides comprehensive coverage of the topic.

## Key Points

- Important concept 1
- Important concept 2
- Important concept 3

## Summary

This chapter covered essential information about the subject matter. The following chapters will build upon these foundations to provide deeper insights and practical applications."""

"""
Custom Model Service
Main interface for using custom-trained LLM model for book generation
"""

import logging
from typing import Dict, List, Optional, Any
from .cloudflare_client import CloudflareAIClient
from .prompt_templates import PromptTemplates
from .response_parser import ResponseParser

logger = logging.getLogger(__name__)


class CustomModelService:
    """
    Service for interacting with custom-trained LLM model
    Handles book outline, chapter generation, and content refinement
    """
    
    def __init__(self):
        self.client = CloudflareAIClient()
        self.prompts = PromptTemplates()
        self.parser = ResponseParser()
        self.model_id = self.client.custom_model_id
    
    def generate_book_outline(
        self,
        domain: str,
        niche: str,
        target_audience: str,
        page_count: int = 20,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate book outline using custom model
        
        Args:
            domain: Book domain/category
            niche: Specific niche within domain
            target_audience: Target audience level
            page_count: Desired number of pages
            **kwargs: Additional context
        
        Returns:
            Dict with outline structure
        """
        logger.info(f"Generating outline for {domain} / {niche}")
        
        # Build prompt from template
        prompt = self.prompts.outline_prompt(
            domain=domain,
            niche=niche,
            target_audience=target_audience,
            page_count=page_count,
            **kwargs
        )
        
        # Call model
        result = self.client.call_model(
            prompt=prompt,
            max_tokens=2000,
            temperature=0.7
        )
        
        if not result.get("success"):
            logger.error(f"Outline generation failed: {result.get('error')}")
            raise Exception(f"Model call failed: {result.get('error')}")
        
        # Parse response
        outline = self.parser.parse_outline(result.get("response", ""))
        
        return {
            "outline": outline,
            "chapters": len(outline.get("chapters", [])),
            "metadata": {
                "model": result.get("model"),
                "elapsed_time": result.get("elapsed_time"),
                "tokens": result.get("tokens")
            }
        }
    
    def generate_chapter_content(
        self,
        chapter_title: str,
        chapter_outline: str,
        book_context: Dict[str, Any],
        word_count: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate content for a specific chapter
        
        Args:
            chapter_title: Title of the chapter
            chapter_outline: Brief outline/description
            book_context: Overall book context (domain, niche, etc.)
            word_count: Target word count
            **kwargs: Additional parameters
        
        Returns:
            Dict with chapter content
        """
        logger.info(f"Generating chapter: {chapter_title}")
        
        # Build prompt
        prompt = self.prompts.chapter_prompt(
            title=chapter_title,
            outline=chapter_outline,
            context=book_context,
            word_count=word_count,
            **kwargs
        )
        
        # Call model
        result = self.client.call_model(
            prompt=prompt,
            max_tokens=2500,
            temperature=0.7
        )
        
        if not result.get("success"):
            logger.error(f"Chapter generation failed: {result.get('error')}")
            raise Exception(f"Model call failed: {result.get('error')}")
        
        # Parse and validate content
        content = self.parser.parse_chapter(result.get("response", ""))
        
        return {
            "content": content,
            "word_count": len(content.split()),
            "metadata": {
                "model": result.get("model"),
                "elapsed_time": result.get("elapsed_time"),
                "tokens": result.get("tokens")
            }
        }
    
    def refine_content(
        self,
        content: str,
        refinement_type: str = "grammar",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Refine/improve existing content
        
        Args:
            content: Content to refine
            refinement_type: Type of refinement (grammar, clarity, style, etc.)
            **kwargs: Additional parameters
        
        Returns:
            Dict with refined content
        """
        logger.info(f"Refining content ({refinement_type})")
        
        prompt = self.prompts.refinement_prompt(
            content=content,
            refinement_type=refinement_type,
            **kwargs
        )
        
        result = self.client.call_model(
            prompt=prompt,
            max_tokens=3000,
            temperature=0.5
        )
        
        if not result.get("success"):
            logger.warning(f"Refinement failed: {result.get('error')}")
            # Return original content if refinement fails
            return {"content": content}
        
        refined = self.parser.parse_refinement(result.get("response", ""))
        
        return {
            "content": refined,
            "metadata": {
                "model": result.get("model"),
                "elapsed_time": result.get("elapsed_time")
            }
        }
    
    def generate_cover_description(
        self,
        book_title: str,
        book_context: Dict[str, Any],
        **kwargs
    ) -> str:
        """
        Generate visual description for book cover
        
        Args:
            book_title: Title of the book
            book_context: Book context and metadata
            **kwargs: Additional parameters
        
        Returns:
            String description for cover image generation
        """
        logger.info(f"Generating cover description for: {book_title}")
        
        prompt = self.prompts.cover_description_prompt(
            title=book_title,
            context=book_context,
            **kwargs
        )
        
        result = self.client.call_model(
            prompt=prompt,
            max_tokens=300,
            temperature=0.8
        )
        
        if not result.get("success"):
            logger.warning(f"Cover description generation failed: {result.get('error')}")
            # Return fallback description
            return f"Professional book cover for {book_title}"
        
        description = result.get("response", "").strip()
        return description
    
    def test_model(self) -> Dict[str, Any]:
        """
        Test custom model with simple prompt
        
        Returns:
            Dict with test results
        """
        logger.info("Testing custom model...")
        
        test_prompt = "Write a short introduction (50 words) about the importance of continuous learning."
        
        result = self.client.call_model(
            prompt=test_prompt,
            max_tokens=100,
            temperature=0.7
        )
        
        return {
            "success": result.get("success"),
            "response": result.get("response"),
            "error": result.get("error"),
            "model": result.get("model"),
            "elapsed_time": result.get("elapsed_time")
        }

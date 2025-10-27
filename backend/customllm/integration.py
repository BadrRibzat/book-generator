"""
LLM Integration Selector
DEPRECATED: Use customllm.services.custom_book_generator.CustomBookGenerator directly
This file kept for backward compatibility only
"""

import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class LLMIntegration:
    """
    DEPRECATED: Use CustomBookGenerator directly
    This wrapper is no longer needed
    """
    
    def __init__(self):
        logger.warning(
            "⚠️ LLMIntegration is DEPRECATED!\n"
            "   Use: from customllm.services.custom_book_generator import CustomBookGenerator\n"
            "   This provides unlimited generation with no rate limits."
        )
        
        # Always use custom LLM now
        from customllm.services.model_service import CustomModelService
        self.custom_service = CustomModelService()
        self.custom_available = True
        self.openrouter_available = False
        
        logger.info("✓ Using Custom LLM (Cloudflare) - UNLIMITED")
    
    def _check_custom_model(self) -> bool:
        """Check if Cloudflare custom model is configured"""
        api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        
        if api_token and account_id and account_id != 'YOUR_ACCOUNT_ID_HERE':
            logger.info("Cloudflare credentials found")
            return True
        
        logger.warning("Cloudflare credentials not configured")
        return False
    
    def _check_openrouter(self) -> bool:
        """Check if OpenRouter is configured"""
        api_key = os.getenv('OPENROUTER_API_KEY')
        
        if api_key:
            logger.info("OpenRouter credentials found")
            return True
        
        logger.warning("OpenRouter credentials not configured")
        return False
    
    def generate_outline(self, book_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate book outline using best available service
        
        Args:
            book_context: Book metadata (domain, niche, audience, page_count, etc.)
        
        Returns:
            Dict with outline data
        """
        if self.custom_available:
            logger.info("📝 Generating outline with Custom LLM")
            return self.custom_service.generate_book_outline(
                domain=book_context.get('domain', 'General'),
                niche=book_context.get('niche', 'Professional Development'),
                target_audience=book_context.get('audience', 'professionals'),
                page_count=book_context.get('page_count', 30)
            )
        else:
            logger.info("📝 Generating outline with OpenRouter")
            outline_text = self.orchestrator.generate_outline(book_context)
            return {
                'outline': {'title': book_context.get('title', 'Untitled'), 'chapters': []},
                'raw_text': outline_text,
                'chapters': 8,  # Default estimate
                'metadata': {'model': 'openrouter', 'elapsed_time': 0}
            }
    
    def generate_chapter(
        self, 
        chapter_title: str,
        chapter_outline: str,
        book_context: Dict[str, Any],
        word_count: int = 500
    ) -> Dict[str, Any]:
        """
        Generate chapter content using best available service
        
        Args:
            chapter_title: Title of the chapter
            chapter_outline: Brief outline/summary
            book_context: Book metadata
            word_count: Target word count
        
        Returns:
            Dict with chapter content and metadata
        """
        if self.custom_available:
            logger.info(f"✍️ Generating chapter '{chapter_title}' with Custom LLM")
            return self.custom_service.generate_chapter_content(
                chapter_title=chapter_title,
                chapter_outline=chapter_outline,
                book_context=book_context,
                word_count=word_count
            )
        else:
            logger.info(f"✍️ Generating chapter '{chapter_title}' with OpenRouter")
            content = self.orchestrator.generate_chapter_content(
                chapter_title=chapter_title,
                chapter_outline=chapter_outline,
                book_context=book_context,
                target_length='medium'
            )
            return {
                'content': content.get('content', ''),
                'word_count': len(content.get('content', '').split()),
                'metadata': {'model': 'openrouter', 'elapsed_time': 0}
            }
    
    def refine_content(self, content: str, instructions: str = "") -> Dict[str, Any]:
        """
        Refine/improve existing content
        
        Args:
            content: Content to refine
            instructions: Specific refinement instructions
        
        Returns:
            Dict with refined content
        """
        if self.custom_available:
            logger.info("🔧 Refining content with Custom LLM")
            return self.custom_service.refine_content(content, instructions)
        else:
            logger.info("🔧 Refining content with OpenRouter")
            refined = self.orchestrator.review_and_improve_content(content, instructions)
            return {
                'refined_content': refined,
                'improvements_made': ['Grammar', 'Clarity', 'Flow'],
                'metadata': {'model': 'openrouter', 'elapsed_time': 0}
            }
    
    def generate_cover_description(self, book_context: Dict[str, Any]) -> str:
        """
        Generate cover image description/prompt
        
        Args:
            book_context: Book metadata
        
        Returns:
            Cover description string
        """
        if self.custom_available:
            logger.info("🎨 Generating cover description with Custom LLM")
            result = self.custom_service.generate_cover_description(book_context)
            return result.get('description', '')
        else:
            logger.info("🎨 Generating cover description with OpenRouter")
            return self.orchestrator.generate_cover_description(book_context)
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about active service"""
        if self.custom_available:
            return {
                'service': 'Custom LLM (Cloudflare)',
                'rate_limited': False,
                'cost_model': 'Fixed monthly (~$5-10)',
                'quality': 'Optimized for book generation',
                'status': '✅ ACTIVE'
            }
        elif self.openrouter_available:
            return {
                'service': 'OpenRouter',
                'rate_limited': True,
                'cost_model': 'Per-request or free tier (50/day)',
                'quality': 'Generic models',
                'status': '⚠️ FALLBACK'
            }
        else:
            return {
                'service': 'None',
                'status': '❌ NO SERVICE'
            }

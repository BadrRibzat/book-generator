"""
Custom Book Generator
Uses ONLY local trained LLM - No external API calls except Cloudflare for images
Unlimited generation capacity for the 3 trained domains
"""

import logging
from typing import Dict, Any, Optional
from customllm.services.local_llm_engine import LocalLLMEngine
from customllm.services.cloudflare_client import CloudflareAIClient
from backend.utils.mongodb import get_mongodb_db

logger = logging.getLogger(__name__)


class CustomBookGenerator:
    """
    Book generator using custom trained LLM
    - Text generation: Local LLM (unlimited, no API calls)
    - Images: Cloudflare AI (for covers only)
    - PDF: ReportLab (completely local)
    """
    
    def __init__(self):
        self.llm = LocalLLMEngine()
        self.cloudflare = CloudflareAIClient()
        self.supported_domains = [
            'AI & Automation',
            'Parenting',
            'Parenting: Pre-school Speech & Learning',
            'E-commerce & Digital Products',
            'E-commerce',
            # Expanded labels used by guided workflow
            'Sustainability & Green Tech',
            'Nutrition & Wellness',
            'Meditation & Mindfulness',
            'Home Workout & Fitness',
            'Language & Kids',
            'Technology & AI',
        ]
    
    def is_domain_supported(self, domain: str) -> bool:
        """Check if domain is supported by trained model"""
        return any(d.lower() in domain.lower() or domain.lower() in d.lower() for d in self.supported_domains)
    
    def generate_book_outline(self, book_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate book outline using local LLM
        No external API calls - instant and unlimited
        
        Args:
            book_context: Book metadata (domain, niche, audience, page_count)
        
        Returns:
            Dict with outline structure
        """
        try:
            logger.info(f"📝 Generating outline with Custom LLM for: {book_context.get('domain')}")
            
            domain = book_context.get('domain', 'AI & Automation')
            
            # No hard failure: LocalLLMEngine handles fallback when not trained
            if not self.is_domain_supported(domain):
                logger.warning("Domain %s not in trained set; using fallback outline generator", domain)
            
            # Generate outline using local LLM
            result = self.llm.generate_outline(
                domain=domain,
                niche=book_context.get('niche', 'General'),
                target_audience=book_context.get('audience', 'professionals'),
                page_count=book_context.get('page_count', 30)
            )
            
            logger.info(f"✅ Outline generated: {result.get('chapters', 0)} chapters")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Outline generation failed: {str(e)}")
            raise
    
    def generate_chapter(
        self,
        chapter_title: str,
        chapter_outline: str,
        book_context: Dict[str, Any],
        word_count: int = 500,
        subtopics: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate chapter content using local LLM
        No external API calls - instant and unlimited
        
        Args:
            chapter_title: Chapter title
            chapter_outline: Brief outline
            book_context: Book metadata
            word_count: Target word count
        
        Returns:
            Dict with chapter content
        """
        try:
            logger.info(f"✍️ Generating chapter '{chapter_title}' with Custom LLM")
            
            # Generate chapter using local LLM
            result = self.llm.generate_chapter_content(
                chapter_title=chapter_title,
                chapter_outline=chapter_outline,
                book_context=book_context,
                word_count=word_count,
                subtopics=subtopics
            )
            
            logger.info(f"✅ Chapter generated: {result.get('word_count', 0)} words")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Chapter generation failed: {str(e)}")
            raise
    
    def generate_cover_image(self, book_context: Dict[str, Any]) -> Optional[bytes]:
        """
        Generate cover image using Cloudflare AI
        This is the ONLY external API call in the entire process
        
        Args:
            book_context: Book metadata
        
        Returns:
            bytes: Image data or None
        """
        try:
            logger.info("🎨 Generating cover image with Cloudflare AI")
            
            # Create cover prompt
            domain = book_context.get('domain', 'Professional')
            niche = book_context.get('niche', 'Guide')
            title = book_context.get('title', 'Complete Guide')
            
            prompt = self._create_cover_prompt(domain, niche, title)
            
            # Generate image using Cloudflare
            image_data = self.cloudflare.generate_image(prompt)
            
            if image_data:
                logger.info("✅ Cover image generated")
            else:
                logger.warning("⚠️ Cover image generation failed, will use default")
            
            return image_data
            
        except Exception as e:
            logger.error(f"❌ Cover image generation failed: {str(e)}")
            return None
    
    def _create_cover_prompt(self, domain: str, niche: str, title: str) -> str:
        """Create cover image prompt based on domain"""
        
        prompts = {
            'ai': f"Professional book cover for '{title}'. Modern tech design, AI and automation theme, circuit patterns, neural network, blue purple gradient, clean typography, minimalist style, 4K quality",
            'parenting': f"Warm nurturing book cover for '{title}'. Soft pastel colors, parent child silhouette, playful educational elements, hearts, growth symbols, friendly professional design, 4K quality",
            'ecommerce': f"Dynamic business book cover for '{title}'. Bold colors, growth charts, shopping elements, digital commerce theme, modern typography, success imagery, professional style, 4K quality"
        }
        
        # Determine domain type
        domain_lower = domain.lower()
        if 'ai' in domain_lower or 'automation' in domain_lower:
            return prompts['ai']
        elif 'parent' in domain_lower or 'child' in domain_lower or 'speech' in domain_lower:
            return prompts['parenting']
        elif 'ecommerce' in domain_lower or 'commerce' in domain_lower or 'digital' in domain_lower:
            return prompts['ecommerce']
        
        return prompts['ai']  # Default
    
    def save_book_content(self, book_id: int, content_data: Dict[str, Any]) -> str:
        """
        Save book content to MongoDB
        
        Args:
            book_id: Book ID
            content_data: Content data dict
        
        Returns:
            MongoDB document ID
        """
        try:
            db = get_mongodb_db()
            collection = db['book_contents']
            
            document = {
                'book_id': book_id,
                'outline': content_data.get('outline', {}),
                'chapters': content_data.get('chapters', []),
                'metadata': content_data.get('metadata', {}),
                'generated_with': 'custom_local_llm',
                'api_calls_used': 1 if content_data.get('cover_image') else 0  # Only Cloudflare for image
            }
            
            result = collection.insert_one(document)
            logger.info(f"✅ Book content saved to MongoDB: {result.inserted_id}")
            
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to save book content: {str(e)}")
            raise
    
    def get_supported_domains(self) -> list:
        """Get list of supported trained domains"""
        return self.supported_domains
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Get training statistics"""
        from customllm.models import TrainingDomain, TrainingSample
        
        stats = {
            'domains': [],
            'total_samples': TrainingSample.objects.filter(is_active=True).count()
        }
        
        for domain in TrainingDomain.objects.filter(is_active=True):
            stats['domains'].append({
                'name': domain.name,
                'slug': domain.slug,
                'samples': domain.training_samples_count,
                'quality_score': domain.training_quality_score,
                'last_trained': domain.last_trained.isoformat() if domain.last_trained else None
            })
        
        return stats

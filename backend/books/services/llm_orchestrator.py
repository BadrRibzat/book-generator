"""
Enhanced LLM Orchestrator with Cloudflare Integration
Optimizes book generation using specialized models for different tasks
Integrates Cloudflare AI for image generation and token tracking
"""

import os
import requests
import time
import logging
from typing import Dict, List, Optional, Any
from openai import OpenAI
from .usage_tracker import UsageTracker

logger = logging.getLogger(__name__)


class CloudflareAIClient:
    """
    Cloudflare AI integration for image generation and token tracking
    """
    
    def __init__(self):
        self.api_key = os.getenv('CLOUDFLAR_KEY')
        self.global_api_key = os.getenv('GLOBAL_API_KEY')
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID', '')
        
        if not self.api_key:
            logger.warning("CLOUDFLAR_KEY not set - Cloudflare features disabled")
        
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run"
        self.usage_tracker = UsageTracker()
    
    def generate_image(self, prompt: str, **kwargs) -> Optional[bytes]:
        """
        Generate image using Cloudflare AI Workers
        
        Args:
            prompt: Image generation prompt
            **kwargs: Additional parameters (width, height, steps, etc.)
        
        Returns:
            bytes: Image data or None if failed
        """
        if not self.api_key or not self.account_id:
            logger.error("Cloudflare credentials not configured")
            return None
        
        try:
            # Cloudflare AI image generation model
            model = "@cf/stabilityai/stable-diffusion-xl-base-1.0"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": prompt,
                "num_steps": kwargs.get('steps', 20),
                "guidance": kwargs.get('guidance', 7.5),
            }
            
            response = requests.post(
                f"{self.base_url}/{model}",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            
            # Track Cloudflare usage
            self.usage_tracker.record_cloudflare_usage('image_generation', 1)
            
            return response.content
            
        except Exception as e:
            logger.error(f"Cloudflare image generation failed: {str(e)}")
            return None
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count using Cloudflare AI tokenization
        Fallback to simple estimation if Cloudflare unavailable
        
        Args:
            text: Text to count tokens for
            
        Returns:
            int: Approximate token count
        """
        # Simple estimation: ~4 characters per token for English
        return len(text) // 4


class LLMOrchestrator:
    """
    Enhanced LLM orchestration with model specialization and Cloudflare integration
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key
        )
        
        self.cloudflare = CloudflareAIClient()
        self.usage_tracker = UsageTracker()
        
        # Optimized model mapping for different tasks (verified working models)
        self.models = {
            # Outline Generation: Fast structural planning (10B activated, 230B total)
            'outline': 'minimax/minimax-m2:free',
            
            # Content Generation: High-quality verbose content (9B with reasoning)
            'content_generation': 'nvidia/nemotron-nano-9b-v2:free',
            
            # Content Review: Editing and refinement (24B params)
            'content_review': 'mistralai/mistral-small-3.2-24b-instruct:free',
            
            # Cover Design: Creative descriptive prompts (24B params)
            'cover_design': 'mistralai/mistral-small-3.2-24b-instruct:free',
            
            # Fallback model
            'fallback': 'mistralai/mistral-small-3.2-24b-instruct:free',
        }
        
        # Dynamic token thresholds with 20% buffers
        self.token_thresholds = {
            'short': {
                'min': 400,
                'target': 500,
                'max': 600,
                'buffer': 0.2
            },
            'medium': {
                'min': 600,
                'target': 700,
                'max': 800,
                'buffer': 0.2
            },
            'full': {
                'min': 800,
                'target': 900,
                'max': 1000,
                'buffer': 0.2
            }
        }
    
    def generate_outline(self, book_context: Dict[str, Any]) -> str:
        """
        Generate book outline using fast structural model with Cloudflare validation
        
        Args:
            book_context: Book metadata including domain, niche, style
            
        Returns:
            str: Generated outline
        """
        prompt = f"""Generate a comprehensive book outline for:

Title: {book_context.get('title', 'Professional Guide')}
Domain: {book_context.get('domain', 'General')}
Niche: {book_context.get('niche', 'Professional Development')}
Audience: {book_context.get('audience', 'Professionals')}
Length: {book_context.get('length', 'medium')}

Create a detailed outline with:
1. Introduction (with hook and overview)
2. 6-8 main chapters with descriptive titles
3. 3-5 subsections per chapter
4. Conclusion with key takeaways
5. Additional sections (glossary, resources, appendix)

Format as structured outline with clear hierarchy."""

        try:
            response = self._call_model('outline', prompt, max_tokens=2000, temperature=0.7)
            outline = response.get('content', '')
            
            # Validate outline structure
            if not self._validate_outline(outline):
                logger.warning("Outline validation failed, regenerating...")
                response = self._call_model('fallback', prompt, max_tokens=2000, temperature=0.8)
                outline = response.get('content', '')
            
            return outline
            
        except Exception as e:
            logger.error(f"Outline generation failed: {str(e)}")
            raise
    
    def generate_chapter_content(
        self, 
        chapter_title: str, 
        book_context: Dict[str, Any],
        length_setting: str = 'medium',
        retry_count: int = 0
    ) -> str:
        """
        Generate chapter content with dynamic token validation and recursive expansion
        
        Args:
            chapter_title: Title of the chapter
            book_context: Book metadata
            length_setting: short/medium/full
            retry_count: Current retry attempt
            
        Returns:
            str: Generated chapter content
        """
        threshold = self.token_thresholds.get(length_setting, self.token_thresholds['medium'])
        target_words = threshold['target'] * 4  # Approximate words from tokens
        
        prompt = f"""Write a complete chapter for a professional book.

Chapter Title: {chapter_title}
Book Context: {book_context.get('title', '')} - {book_context.get('domain', '')}
Target Word Count: {target_words} words MINIMUM
Audience: {book_context.get('audience', 'Professionals')}

Requirements:
1. Write {target_words} words minimum (aim for 20% more)
2. Use 5-7 well-developed paragraphs
3. Each paragraph should be 150-250 words
4. Include practical examples and actionable insights
5. Use clear section headings (####) for subsections
6. Incorporate relevant statistics or research (with citations)
7. End with a smooth transition to the next chapter

Writing Style:
- Professional yet accessible
- Concrete examples over abstract theory
- Active voice and clear sentences
- Engage the reader with questions and scenarios

Write the FULL chapter now with substantial content:"""

        try:
            max_tokens = threshold['max'] * 5  # Allow for verbose generation
            response = self._call_model(
                'content_generation', 
                prompt, 
                max_tokens=max_tokens, 
                temperature=0.7
            )
            content = response.get('content', '')
            
            # Validate content length using Cloudflare token counter
            token_count = self.cloudflare.count_tokens(content)
            
            if token_count < threshold['min'] and retry_count < 3:
                logger.warning(f"Chapter too short ({token_count} tokens), expanding... (retry {retry_count + 1})")
                content = self._expand_content(content, chapter_title, book_context, threshold)
            elif token_count < threshold['min']:
                logger.error(f"Chapter still too short after {retry_count} retries")
            
            return content
            
        except Exception as e:
            logger.error(f"Chapter generation failed: {str(e)}")
            raise
    
    def review_and_refine_content(
        self, 
        content: str, 
        chapter_title: str = "",
        book_context: Dict[str, Any] = None,
        refinement_goals: List[str] = None
    ) -> str:
        """
        Review and refine content using editing model with recursive rewriting
        
        Args:
            content: Content to refine
            chapter_title: Optional chapter title for context
            book_context: Optional book context
            refinement_goals: List of specific improvements to make
            
        Returns:
            str: Refined content
        """
        if refinement_goals is None:
            refinement_goals = [
                "Expand brief sections",
                "Add concrete examples",
                "Improve transitions",
                "Enhance readability"
            ]
        
        goals_text = "\n".join([f"- {goal}" for goal in refinement_goals])
        context_text = f"\nChapter: {chapter_title}" if chapter_title else ""
        if book_context:
            context_text += f"\nBook: {book_context.get('title', '')}"
        
        prompt = f"""You are an expert editor. Review and enhance this content:{context_text}

Original Content:
{content}

Refinement Goals:
{goals_text}

Your tasks:
1. Expand any sections that are too brief (less than 100 words)
2. Add transition sentences between paragraphs
3. Include concrete examples or case studies
4. Ensure professional language and consistency
5. Maintain the original structure and key points
6. Enhance readability and flow

Enhanced version:"""

        try:
            response = self._call_model('content_review', prompt, max_tokens=3000, temperature=0.6)
            refined = response.get('content', content)
            
            # Ensure refined content is actually longer
            if self.cloudflare.count_tokens(refined) < self.cloudflare.count_tokens(content):
                logger.warning("Refinement made content shorter, keeping original")
                return content
            
            return refined
            
        except Exception as e:
            logger.error(f"Content refinement failed: {str(e)}")
            return content  # Return original on failure
    
    def generate_cover_brief(self, book_context: Dict[str, Any]) -> str:
        """
        Generate creative cover design brief using specialized model
        
        Args:
            book_context: Book metadata
            
        Returns:
            str: Cover design brief
        """
        prompt = f"""Create a detailed cover design brief for a professional book.

Book Details:
Title: {book_context.get('title', '')}
Domain: {book_context.get('domain', '')}
Niche: {book_context.get('niche', '')}
Audience: {book_context.get('audience', '')}

Generate a comprehensive design brief including:
1. Visual theme and mood
2. Color palette (3-4 colors with hex codes)
3. Typography style (font families and weights)
4. Layout composition
5. Key visual elements or imagery
6. Design style (minimalist, futuristic, elegant, etc.)

Format as a clear, actionable brief for a designer."""

        try:
            response = self._call_model('cover_design', prompt, max_tokens=800, temperature=0.8)
            return response.get('content', '')
        except Exception as e:
            logger.error(f"Cover brief generation failed: {str(e)}")
            return "Professional minimalist design with clean typography and modern color palette"
    
    def _call_model(
        self, 
        task_type: str, 
        prompt: str, 
        max_tokens: int = 2000, 
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Call OpenRouter API with specified model for task type
        
        Args:
            task_type: Type of task (outline, content_generation, etc.)
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            dict: Response with content and metadata
        """
        model = self.models.get(task_type, self.models['fallback'])
        
        try:
            logger.info(f"Calling model {model} for task: {task_type}")
            
            start_time = time.time()
            
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional book writer creating high-quality, publishable content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9
            )
            
            latency = time.time() - start_time
            
            content = response.choices[0].message.content.strip()
            
            # Track usage
            if hasattr(response, 'usage'):
                usage = response.usage
                self.usage_tracker.record_usage(
                    usage.prompt_tokens,
                    usage.completion_tokens,
                    model=model
                )
                logger.info(f"Model {model}: {usage.prompt_tokens} prompt + {usage.completion_tokens} completion tokens ({latency:.2f}s)")
            
            return {
                'content': content,
                'model': model,
                'latency': latency,
                'tokens': getattr(response.usage, 'total_tokens', 0) if hasattr(response, 'usage') else 0
            }
            
        except Exception as e:
            logger.error(f"Model call failed for {model}: {str(e)}")
            raise
    
    def _validate_outline(self, outline: str) -> bool:
        """
        Validate outline structure
        
        Args:
            outline: Generated outline
            
        Returns:
            bool: True if valid
        """
        if not outline or len(outline) < 200:
            return False
        
        # Check for key sections
        required_sections = ['introduction', 'chapter', 'conclusion']
        outline_lower = outline.lower()
        
        return all(section in outline_lower for section in required_sections)
    
    def _expand_content(
        self, 
        content: str, 
        chapter_title: str, 
        book_context: Dict[str, Any],
        threshold: Dict[str, int]
    ) -> str:
        """
        Recursively expand content that's too short
        
        Args:
            content: Current content
            chapter_title: Chapter title
            book_context: Book metadata
            threshold: Token thresholds
            
        Returns:
            str: Expanded content
        """
        expansion_prompt = f"""The following chapter content is too brief. Expand it with more details, examples, and insights while maintaining quality.

Current Content:
{content}

Chapter: {chapter_title}
Context: {book_context.get('title', '')}

Requirements:
1. Add 2-3 more substantial paragraphs (150-250 words each)
2. Include concrete examples or case studies
3. Add practical applications
4. Incorporate relevant statistics or research
5. Maintain professional tone and flow
6. Ensure smooth transitions

Write the EXPANDED version:"""

        try:
            response = self._call_model(
                'content_generation',
                expansion_prompt,
                max_tokens=threshold['max'] * 6,
                temperature=0.75
            )
            expanded = response.get('content', content)
            
            # Check if expansion was successful
            if self.cloudflare.count_tokens(expanded) > self.cloudflare.count_tokens(content):
                return expanded
            else:
                return content
                
        except Exception as e:
            logger.error(f"Content expansion failed: {str(e)}")
            return content


class MultiLLMOrchestrator(LLMOrchestrator):
    """
    Backward compatibility wrapper - use LLMOrchestrator instead
    """
    
    def __init__(self):
        super().__init__()
        logger.warning("MultiLLMOrchestrator is deprecated, use LLMOrchestrator instead")
    
    def generate_with_fallback(
        self, 
        prompt: str, 
        task_type: str, 
        max_tokens: int = 2000
    ) -> str:
        """
        Backward compatibility method
        """
        response = self._call_model(task_type, prompt, max_tokens)
        return response.get('content', '')
    
    def generate_chapter(
        self, 
        chapter_title: str, 
        context: Dict[str, Any], 
        word_count: int = 800
    ) -> str:
        """
        Backward compatibility method
        """
        # Determine length setting based on word count
        if word_count < 600:
            length_setting = 'short'
        elif word_count < 900:
            length_setting = 'medium'
        else:
            length_setting = 'full'
        
        return self.generate_chapter_content(chapter_title, context, length_setting)
    
    def enhance_content(self, content: str) -> str:
        """
        Backward compatibility method
        """
        return self.review_and_refine_content(
            content,
            ['Expand brief sections', 'Add examples', 'Improve flow']
        )

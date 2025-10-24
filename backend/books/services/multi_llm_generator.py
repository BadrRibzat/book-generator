import os
from openai import OpenAI
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class MultiLLMOrchestrator:
    """
    Orchestrates multiple free LLMs for optimal book generation
    """

    def __init__(self):
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

        # Free LLM models optimized for different tasks (all with :free tags)
        self.models = {
            # Best for structured content & chapters
            'content_primary': 'deepseek/deepseek-chat:free',  # Free DeepSeek model
            
            # Best for creative introductions & conclusions
            'content_creative': 'meta-llama/llama-3.2-3b-instruct:free',
            
            # Best for technical accuracy & examples
            'content_technical': 'google/gemma-2-9b-it:free',
            
            # Best for copywriting & marketing text
            'content_marketing': 'mistralai/mistral-7b-instruct:free',
            
            # Best for editing & refinement
            'content_refiner': 'microsoft/phi-3-mini-128k-instruct:free',
            
            # Best for cover design descriptions
            'cover_designer': 'meta-llama/llama-3.2-3b-instruct:free'
        }

    def generate_with_fallback(self, prompt: str, task_type: str, max_tokens: int = 2000) -> str:
        """
        Generate content with automatic fallback to alternative models
        """
        primary_model = self.models.get(task_type, self.models['content_primary'])
        fallback_models = [m for m in self.models.values() if m != primary_model]

        models_to_try = [primary_model] + fallback_models[:2]  # Try 3 models max

        for model in models_to_try:
            try:
                logger.info(f"Attempting generation with {model} for task: {task_type}")
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
                    temperature=0.7,
                    top_p=0.9
                )

                content = response.choices[0].message.content.strip()

                # Validate content quality
                if self._validate_content(content):
                    logger.info(f"Successfully generated content with {model}")
                    return content
                else:
                    logger.warning(f"Content from {model} failed validation, trying fallback")

            except Exception as e:
                logger.error(f"Error with {model}: {str(e)}, trying next model")
                continue

        raise Exception("All models failed to generate acceptable content")

    def _validate_content(self, content: str) -> bool:
        """
        Validate that generated content meets minimum quality standards
        """
        if not content or len(content) < 100:
            return False

        # Check for minimum word count
        words = content.split()
        if len(words) < 50:
            return False

        # Check for paragraph structure
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        if len(paragraphs) < 1:
            return False

        # Ensure no single-line paragraphs dominate
        short_paragraphs = [p for p in paragraphs if len(p.split()) < 5]
        if len(short_paragraphs) > len(paragraphs) * 0.5:
            return False

        return True

    def generate_chapter(self, chapter_title: str, context: Dict, word_count: int = 800) -> str:
        """
        Generate a full chapter using optimized models
        """
        prompt = f"""Write a complete chapter for a professional book.

Chapter Title: {chapter_title}
Target Word Count: {word_count} words
Book Context: {context.get('book_title', '')}
Domain: {context.get('domain', '')}
Audience: {context.get('audience', '')}

Requirements:
1. Write {word_count} words minimum (aim for 1000-1200 words)
2. Use 4-6 well-developed paragraphs
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

Begin writing the chapter now:"""

        return self.generate_with_fallback(
            prompt=prompt,
            task_type='content_primary',
            max_tokens=2000  # Enough for ~1500 words
        )

    def enhance_content(self, content: str) -> str:
        """
        Use refinement model to enhance and expand content
        """
        prompt = f"""You are an expert editor. Review and enhance this book content:

Original Content:
{content}

Your tasks:
1. Expand any sections that are too brief (less than 100 words)
2. Add transition sentences between paragraphs
3. Include at least one concrete example or case study
4. Ensure professional language and consistency
5. Maintain the original structure and key points
6. Target output: 150% of original length

Enhanced version:"""

        return self.generate_with_fallback(
            prompt=prompt,
            task_type='content_refiner',
            max_tokens=2500
        )
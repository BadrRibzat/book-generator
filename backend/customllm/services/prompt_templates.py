"""
Prompt Templates
Optimized prompts for custom model book generation tasks
"""

from typing import Dict, Any


class PromptTemplates:
    """
    Collection of prompt templates optimized for book generation
    """
    
    def outline_prompt(
        self,
        domain: str,
        niche: str,
        target_audience: str,
        page_count: int,
        **kwargs
    ) -> str:
        """
        Generate prompt for book outline creation
        """
        key_topics = kwargs.get('key_topics', [])
        writing_style = kwargs.get('writing_preferences', 'professional')
        
        topics_text = ", ".join(key_topics) if key_topics else "comprehensive coverage"
        
        prompt = f"""Create a detailed book outline for the following:

**Domain**: {domain}
**Niche**: {niche}
**Target Audience**: {target_audience}
**Target Length**: {page_count} pages
**Writing Style**: {writing_style}
**Key Topics**: {topics_text}

Generate a professional book outline with:
1. A compelling book title
2. 8-10 chapter titles with brief descriptions
3. Logical flow and progression
4. Appropriate depth for {target_audience} readers

Format your response as:
TITLE: [Book Title]

CHAPTERS:
1. [Chapter Title] - [Brief description]
2. [Chapter Title] - [Brief description]
...

Make the outline engaging, practical, and tailored to the {niche} niche."""

        return prompt
    
    def chapter_prompt(
        self,
        title: str,
        outline: str,
        context: Dict[str, Any],
        word_count: int,
        **kwargs
    ) -> str:
        """
        Generate prompt for chapter content creation
        """
        domain = context.get('domain', '')
        niche = context.get('niche', '')
        audience = context.get('target_audience', 'general')
        style = context.get('writing_preferences', 'professional')
        
        prompt = f"""Write a complete chapter for a book about {niche} in the {domain} domain.

**Chapter Title**: {title}
**Chapter Outline**: {outline}
**Target Audience**: {audience}
**Writing Style**: {style}
**Target Length**: {word_count} words

Requirements:
1. Start with an engaging introduction
2. Include practical examples and actionable insights
3. Use clear, {audience}-appropriate language
4. Add subheadings for better readability
5. End with a brief summary or key takeaways
6. Write in a {style} tone

Write the complete chapter content now (aim for {word_count} words):"""

        return prompt
    
    def refinement_prompt(
        self,
        content: str,
        refinement_type: str,
        **kwargs
    ) -> str:
        """
        Generate prompt for content refinement
        """
        refinement_instructions = {
            'grammar': "Fix grammar, spelling, and punctuation errors while preserving the original meaning and style.",
            'clarity': "Improve clarity and readability. Make complex concepts easier to understand without oversimplifying.",
            'style': "Enhance writing style and flow. Make the text more engaging while maintaining professionalism.",
            'expansion': "Expand the content with more details, examples, and explanations. Add depth without being repetitive.",
            'condensing': "Make the content more concise. Remove redundancy while keeping all key points."
        }
        
        instruction = refinement_instructions.get(refinement_type, refinement_instructions['grammar'])
        
        prompt = f"""Refine the following content:

{instruction}

**Original Content**:
{content}

**Refined Version**:"""

        return prompt
    
    def cover_description_prompt(
        self,
        title: str,
        context: Dict[str, Any],
        **kwargs
    ) -> str:
        """
        Generate prompt for cover image description
        """
        domain = context.get('domain', '')
        niche = context.get('niche', '')
        style = kwargs.get('cover_style', 'professional')
        
        prompt = f"""Create a detailed visual description for a book cover design.

**Book Title**: {title}
**Domain**: {domain}
**Niche**: {niche}
**Cover Style**: {style}

Generate a vivid, detailed description (100-150 words) for an AI image generator to create this book cover. Include:
1. Main visual elements and composition
2. Color scheme appropriate for the {niche} niche
3. Typography style for the title
4. Overall mood and atmosphere
5. Professional design elements

Focus on creating a cover that would appeal to readers interested in {niche}.

Visual Description:"""

        return prompt
    
    def summarization_prompt(
        self,
        content: str,
        max_words: int = 100
    ) -> str:
        """
        Generate prompt for content summarization
        """
        prompt = f"""Summarize the following content in approximately {max_words} words. Focus on the key points and main ideas.

**Content**:
{content}

**Summary** ({max_words} words):"""

        return prompt
    
    def title_generation_prompt(
        self,
        outline: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Generate prompt for book title creation
        """
        domain = context.get('domain', '')
        niche = context.get('niche', '')
        
        prompt = f"""Based on this book outline, generate 5 compelling book titles.

**Domain**: {domain}
**Niche**: {niche}

**Outline**:
{outline}

Generate 5 professional, engaging titles that:
1. Clearly indicate the book's subject
2. Appeal to the target audience
3. Are memorable and marketable
4. Are concise (3-7 words preferred)

**Titles**:
1. 
2. 
3. 
4. 
5. """

        return prompt

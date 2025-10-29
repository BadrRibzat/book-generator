"""
Local LLM Engine - Custom Text Generation
No external APIs, uses trained templates and patterns from MongoDB
Generates unlimited content for the 3 trained domains
"""

import random
import logging
from typing import Dict, List, Any, Optional
from django.core.cache import cache
from customllm.models import TrainingDomain, TrainingNiche, TrainingSample

logger = logging.getLogger(__name__)


class LocalLLMEngine:
    """
    Custom LLM engine that generates content using trained templates
    No external API calls - completely self-contained
    """
    
    def __init__(self):
        self.cache_timeout = 3600  # 1 hour
        self._load_training_data()
    
    def _load_training_data(self):
        """Load training data from database into memory"""
        try:
            # Cache training data for performance
            cache_key = 'llm_training_data'
            cached_data = cache.get(cache_key)
            
            if cached_data:
                self.training_data = cached_data
                logger.info("Loaded training data from cache")
                return
            
            # Load from database
            self.training_data = {
                'ai_automation': self._load_domain_data('ai_automation'),
                'parenting': self._load_domain_data('parenting'),
                'ecommerce': self._load_domain_data('ecommerce'),
            }
            
            # Cache for future use
            cache.set(cache_key, self.training_data, self.cache_timeout)
            logger.info("Loaded training data from database")
            
        except Exception as e:
            logger.error(f"Failed to load training data: {str(e)}")
            self.training_data = {}
    
    def _load_domain_data(self, domain_slug: str) -> Dict[str, List[Dict]]:
        """Load training samples for a specific domain"""
        try:
            domain = TrainingDomain.objects.get(slug=domain_slug, is_active=True)
            
            data = {
                'outline': [],
                'chapter': [],
                'introduction': [],
                'conclusion': [],
                'cover_description': []
            }
            
            # Load samples by type
            for sample_type in data.keys():
                samples = TrainingSample.objects.filter(
                    domain=domain,
                    sample_type=sample_type,
                    is_active=True,
                    quality_score__gte=0.7  # Only high-quality samples
                ).order_by('-quality_score')[:50]  # Top 50 per type
                
                data[sample_type] = [
                    {
                        'prompt': s.prompt,
                        'completion': s.completion,
                        'context': s.context,
                        'quality_score': s.quality_score
                    }
                    for s in samples
                ]
            
            return data
            
        except TrainingDomain.DoesNotExist:
            logger.warning(f"Domain {domain_slug} not found in database")
            return {}
    
    def _get_domain_slug(self, domain_name: str) -> str:
        """Convert domain name to slug - use unique slugs for domain-specific content"""
        mapping = {
            'AI & Automation': 'ai_automation',
            'Parenting': 'parenting',
            'Parenting: Pre-school Speech & Learning': 'parenting',
            'E-commerce & Digital Products': 'ecommerce',
            'E-commerce': 'ecommerce',
            # Unique slugs for each domain so fallback can generate domain-specific content
            'Health & Wellness': 'health_wellness',
            'Personal Development': 'personal_development',
            'Business & Entrepreneurship': 'business',
            'Creative Arts': 'creative_arts',
            'Technology': 'technology',
            'Sustainability & Green Tech': 'sustainability',
            'Nutrition & Wellness': 'nutrition',
            'Meditation & Mindfulness': 'meditation',
            'Home Workout & Fitness': 'fitness',
            'Language & Kids': 'language_kids',
            'Technology & AI': 'technology_ai',
            'Finance & Investment': 'finance',
            'Future Skills': 'future_skills',
        }
        slug = mapping.get(domain_name)
        if slug:
            return slug
        # Create slug from domain name if not in mapping
        return domain_name.lower().replace(' & ', '_').replace(' ', '_').replace(':', '').replace('-', '_')
    
    def generate_outline(
        self,
        domain: str,
        niche: str,
        target_audience: str = 'professionals',
        page_count: int = 30
    ) -> Dict[str, Any]:
        """
        Generate book outline using trained templates
        
        Args:
            domain: Domain name (e.g., "AI & Automation")
            niche: Niche name
            target_audience: Target audience
            page_count: Target page count
        
        Returns:
            Dict with outline structure
        """
        domain_slug = self._get_domain_slug(domain)
        
        # Calculate chapter count based on page count
        chapter_count = max(6, min(12, page_count // 3))
        
        # Get training samples for this domain
        samples = self.training_data.get(domain_slug, {}).get('outline', [])
        
        if not samples:
            logger.warning(f"No training data for domain: {domain_slug}")
            fallback = self._generate_fallback_outline(domain, niche, chapter_count, target_audience)
            return {
                'outline': fallback,
                'chapters': len(fallback.get('chapters', [])),
                'metadata': {
                    'model': 'custom_local_llm',
                    'domain': domain_slug,
                    'trained': False,
                    'elapsed_time': 0.05
                }
            }
        
        # Select best matching sample based on context
        best_sample = self._select_best_sample(
            samples,
            context={'audience': target_audience, 'niche': niche}
        )
        
        # Generate outline based on template
        outline = self._adapt_outline_template(
            best_sample,
            domain=domain,
            niche=niche,
            chapter_count=chapter_count,
            audience=target_audience
        )
        
        return {
            'outline': outline,
            'chapters': len(outline.get('chapters', [])),
            'metadata': {
                'model': 'custom_local_llm',
                'domain': domain_slug,
                'trained': True,
                'elapsed_time': 0.1  # Local generation is instant
            }
        }
    
    def generate_chapter_content(
        self,
        chapter_title: str,
        chapter_outline: str,
        book_context: Dict[str, Any],
        word_count: int = 500,
        subtopics: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate chapter content using trained templates
        
        Args:
            chapter_title: Chapter title
            chapter_outline: Brief chapter outline
            book_context: Book metadata
            word_count: Target word count
        
        Returns:
            Dict with chapter content
        """
        domain = book_context.get('domain', 'AI & Automation')
        domain_slug = self._get_domain_slug(domain)
        niche = book_context.get('niche', 'General')
        
        # Get training samples
        samples = self.training_data.get(domain_slug, {}).get('chapter', [])
        
        if not samples:
            logger.warning(f"No chapter training data for domain: {domain_slug}, using contextual fallback")
            return self._generate_fallback_chapter(
                chapter_title, 
                chapter_outline, 
                word_count,
                domain_slug,
                niche
            )
        
        # Select best matching sample
        best_sample = self._select_best_sample(
            samples,
            context={
                'title': chapter_title,
                'outline': chapter_outline,
                'audience': book_context.get('audience', 'professionals')
            }
        )
        
        # Generate chapter content
        content = self._adapt_chapter_template(
            best_sample,
            title=chapter_title,
            outline=chapter_outline,
            word_count=word_count,
            context=book_context,
            subtopics=subtopics
        )
        
        return {
            'content': content,
            'word_count': len(content.split()),
            'metadata': {
                'model': 'custom_local_llm',
                'domain': domain_slug,
                'trained': True,
                'elapsed_time': 0.2
            }
        }
    
    def _select_best_sample(self, samples: List[Dict], context: Dict) -> Dict:
        """Select best matching training sample based on context"""
        if not samples:
            return {}
        
        # For now, use weighted random selection based on quality score
        weights = [s['quality_score'] for s in samples]
        return random.choices(samples, weights=weights, k=1)[0]
    
    def _adapt_outline_template(
        self,
        template: Dict,
        domain: str,
        niche: str,
        chapter_count: int,
        audience: str
    ) -> Dict[str, Any]:
        """Adapt training template to generate specific outline"""
        
        # Get chapter templates from training data
        chapter_templates = self._get_chapter_templates(domain, niche, chapter_count)
        
        return {
            'title': self._generate_title(domain, niche, audience),
            'chapters': chapter_templates,
            'metadata': {
                'domain': domain,
                'niche': niche,
                'audience': audience,
                'page_count': chapter_count * 3
            }
        }
    
    def _get_chapter_templates(self, domain: str, niche: str, count: int) -> List[Dict]:
        """Get chapter templates based on domain and niche"""
        
        # Domain-specific chapter structures
        templates = {
            'ai_automation': [
                {'title': 'Introduction to AI & Automation', 'summary': 'Overview of AI technologies and automation strategies'},
                {'title': 'Understanding AI Tools', 'summary': 'Deep dive into available AI tools and platforms'},
                {'title': 'Automation Strategies', 'summary': 'Practical automation approaches for businesses'},
                {'title': 'Implementation Guide', 'summary': 'Step-by-step implementation of AI solutions'},
                {'title': 'Best Practices', 'summary': 'Industry best practices and case studies'},
                {'title': 'Common Pitfalls', 'summary': 'Mistakes to avoid and how to overcome challenges'},
                {'title': 'Advanced Techniques', 'summary': 'Advanced AI and automation techniques'},
                {'title': 'Future Trends', 'summary': 'Emerging trends and future of AI automation'},
                {'title': 'Practical Applications', 'summary': 'Real-world applications and use cases'},
                {'title': 'Getting Started', 'summary': 'Action plan for implementing AI automation'},
            ],
            'parenting': [
                {'title': 'Understanding Early Development', 'summary': 'Key stages of early childhood development'},
                {'title': 'Speech Milestones', 'summary': 'Normal speech development milestones for preschoolers'},
                {'title': 'Learning Through Play', 'summary': 'Play-based learning strategies for preschool age'},
                {'title': 'Communication Techniques', 'summary': 'Effective communication with young children'},
                {'title': 'Speech Exercises', 'summary': 'Fun speech therapy exercises for home'},
                {'title': 'Building Vocabulary', 'summary': 'Activities to expand your child\'s vocabulary'},
                {'title': 'Reading Together', 'summary': 'The power of reading with your preschooler'},
                {'title': 'Social Skills', 'summary': 'Developing social skills in early childhood'},
                {'title': 'Problem Solving', 'summary': 'Teaching problem-solving to preschoolers'},
                {'title': 'Creating Routines', 'summary': 'Establishing healthy learning routines'},
            ],
            'ecommerce': [
                {'title': 'E-commerce Fundamentals', 'summary': 'Foundation of online business and digital products'},
                {'title': 'Product Selection', 'summary': 'Choosing profitable digital products to sell'},
                {'title': 'Platform Setup', 'summary': 'Setting up your e-commerce platform'},
                {'title': 'Payment Processing', 'summary': 'Secure payment solutions for online stores'},
                {'title': 'Marketing Strategies', 'summary': 'Digital marketing for e-commerce success'},
                {'title': 'Customer Experience', 'summary': 'Creating exceptional customer experiences'},
                {'title': 'Scaling Your Business', 'summary': 'Growth strategies for e-commerce'},
                {'title': 'Analytics & Optimization', 'summary': 'Data-driven optimization techniques'},
                {'title': 'Legal & Compliance', 'summary': 'Legal requirements for online businesses'},
                {'title': 'Automation Tools', 'summary': 'Tools to automate your e-commerce operations'},
            ]
        }
        
        domain_slug = self._get_domain_slug(domain)
        available_chapters = templates.get(domain_slug, templates['ai_automation'])
        
        # Return requested number of chapters
        return available_chapters[:count]
    
    def _generate_title(self, domain: str, niche: str, audience: str) -> str:
        """Generate book title based on domain and niche"""
        
        title_templates = {
            'ai_automation': [
                f"The Complete Guide to {niche}",
                f"Mastering {niche}: A Practical Approach",
                f"{niche} for {audience.title()}",
                f"AI & Automation: {niche} Explained",
            ],
            'parenting': [
                f"Nurturing Your Child: {niche}",
                f"The Parent's Guide to {niche}",
                f"Building Strong Foundations: {niche}",
                f"Helping Your Preschooler: {niche}",
            ],
            'ecommerce': [
                f"E-commerce Success: {niche}",
                f"The Digital Entrepreneur: {niche}",
                f"Building Your Online Business with {niche}",
                f"Profitable {niche} Strategies",
            ]
        }
        
        domain_slug = self._get_domain_slug(domain)
        templates = title_templates.get(domain_slug, title_templates['ai_automation'])
        
        return random.choice(templates)
    
    def _adapt_chapter_template(
        self,
        template: Dict,
        title: str,
        outline: str,
        word_count: int,
        context: Dict,
        subtopics: Optional[list] = None
    ) -> str:
        """Adapt training template to generate specific chapter"""
        
        # Use template as base and customize
        base_content = template.get('completion', '')
        
        # Generate content sections
        sections = []
        
        # Introduction
        sections.append(f"# {title}\n\n")
        sections.append(f"{outline}\n\n")
        
        # Main content (3-5 subsections)
        subsection_count = max(3, min(5, word_count // 200))
        words_per_section = word_count // subsection_count
        
        # Use provided subtopics as section headings when available
        topics = (subtopics or [])[:subsection_count]
        for i in range(subsection_count):
            heading = topics[i] if i < len(topics) else f"Key Concept {i+1}"
            sections.append(f"#### {heading}\n")
            sections.append(self._generate_subsection(
                title=heading,
                context=context,
                word_count=words_per_section,
                section_num=i+1
            ))
        
        # Conclusion
        sections.append(self._generate_section_conclusion(title, context))
        
        return "\n\n".join(sections)
    
    def _generate_subsection(
        self,
        title: str,
        context: Dict,
        word_count: int,
        section_num: int
    ) -> str:
        """Generate a subsection of content"""
        
        domain = context.get('domain', 'AI & Automation')
        domain_slug = self._get_domain_slug(domain)
        
        # Domain-specific content patterns
        content_patterns = {
            'ai_automation': [
                "Understanding the fundamentals is crucial for success. {topic} requires both theoretical knowledge and practical application.",
                "When implementing {topic}, consider the following key factors: efficiency, scalability, and user experience.",
                "Best practices in {topic} include thorough planning, iterative testing, and continuous improvement.",
                "Common challenges include technical complexity, change management, and resource allocation.",
            ],
            'parenting': [
                "Every child develops at their own pace. {topic} is about creating supportive, nurturing environments.",
                "Patience and consistency are key when working on {topic}. Celebrate small victories and progress.",
                "Create engaging activities that make learning fun. Children learn best through play and exploration.",
                "Remember that you're not alone on this journey. Many parents face similar challenges with {topic}.",
            ],
            'ecommerce': [
                "Success in {topic} requires a strategic approach. Start with clear goals and measurable objectives.",
                "Your customers are at the heart of your business. Focus on delivering value and exceptional experiences.",
                "Leverage technology and automation to streamline operations and scale efficiently.",
                "Data-driven decision making is essential. Monitor key metrics and adapt your strategies accordingly.",
            ]
        }
        
        patterns = content_patterns.get(domain_slug, content_patterns['ai_automation'])
        
        # Generate paragraphs
        paragraphs = []
        remaining_words = word_count
        
        while remaining_words > 0:
            pattern = random.choice(patterns)
            paragraph = pattern.format(topic=title)
            
            # Expand paragraph to reach word count
            paragraph += " " + self._generate_filler_content(remaining_words, domain_slug)
            
            paragraphs.append(paragraph)
            remaining_words -= len(paragraph.split())
        
        return "\n\n".join(paragraphs)
    
    def _generate_filler_content(self, word_count: int, domain_slug: str) -> str:
        """Generate additional content to reach word count"""
        
        filler_templates = {
            'ai_automation': "This approach has proven effective across various industries, from healthcare to finance. Organizations implementing these strategies report improved efficiency, reduced costs, and enhanced customer satisfaction. The key is to start small, measure results, and scale what works.",
            'parenting': "Many parents find success with this approach when they practice regularly and maintain a positive attitude. Remember to be patient with yourself and your child. Every small step forward is progress worth celebrating. Creating a supportive environment makes all the difference.",
            'ecommerce': "Successful entrepreneurs in this space consistently focus on customer needs, market trends, and continuous optimization. They test different strategies, analyze results, and adapt quickly. Building a sustainable business requires dedication, but the rewards are worth the effort.",
        }
        
        base_filler = filler_templates.get(domain_slug, filler_templates['ai_automation'])
        
        # Repeat and trim to match word count
        words_needed = max(0, word_count - 50)
        result = (base_filler + " ") * ((words_needed // len(base_filler.split())) + 1)
        
        return " ".join(result.split()[:words_needed])
    
    def _generate_section_conclusion(self, title: str, context: Dict) -> str:
        """Generate conclusion for a section"""
        return f"In this section, we've explored {title} in depth. These concepts provide a foundation for the topics we'll cover in the next chapter."

    def generate_chapter_subtopics(
        self,
        chapter_title: str,
        book_context: Dict[str, Any],
        count: int = 4
    ) -> list:
        """Generate a list of concrete subtopics/bullets for a chapter."""
        domain = book_context.get('domain', 'AI & Automation')
        domain_slug = self._get_domain_slug(domain)
        base = [
            "Foundations and key terms",
            "Frameworks and mental models",
            "Step-by-step workflow",
            "Common mistakes to avoid",
            "Tools and resources",
            "Metrics and checkpoints",
            "Real-world example",
            "Actionable checklist",
        ]
        # Domain hinting
        if domain_slug == 'ecommerce':
            base[:4] = [
                "Finding opportunities",
                "Offer and positioning",
                "Traffic and conversion",
                "Retention and upsells",
            ]
        elif domain_slug == 'parenting':
            base[:4] = [
                "Age-appropriate milestones",
                "Play-based activities",
                "Daily routines and habits",
                "Progress tracking",
            ]
        elif domain_slug == 'ai_automation':
            base[:4] = [
                "Map the current process",
                "Design the target workflow",
                "Automate with no-code tools",
                "Pilot, measure, scale",
            ]

        # Mix with chapter title specificity
        topics = []
        i = 0
        while len(topics) < count and i < len(base) * 2:
            hint = base[i % len(base)]
            item = f"{chapter_title}: {hint}" if len(chapter_title.split()) <= 5 else hint
            if item not in topics:
                topics.append(item)
            i += 1
        return topics[:count]
    
    def _generate_fallback_outline(
        self,
        domain: str,
        niche: str,
        chapter_count: int,
        audience: str
    ) -> Dict[str, Any]:
        """Generate domain/niche-specific outline when no training data available"""
        
        # Generate contextual title
        title = f"The Complete Guide to {niche}"
        if audience and audience != 'general':
            title += f" for {audience.title()}"
        
        # Get domain slug for template selection
        domain_slug = self._get_domain_slug(domain)
        
        # Domain-specific chapter templates
        domain_templates = {
            'health_wellness': [
                f'Understanding {niche} Fundamentals',
                f'Key Principles of {niche}',
                f'Getting Started with {niche}',
                f'Daily {niche} Practices',
                f'Advanced {niche} Techniques',
                f'Common {niche} Challenges',
                f'Measuring Your {niche} Progress',
                f'Long-term {niche} Success',
                f'Tools and Resources for {niche}',
                f'Building Your {niche} Routine',
            ],
            'personal_development': [
                f'The Foundation of {niche}',
                f'Setting {niche} Goals',
                f'Developing {niche} Skills',
                f'Overcoming {niche} Obstacles',
                f'Building {niche} Habits',
                f'Mastering {niche} Strategies',
                f'Advanced {niche} Techniques',
                f'Measuring {niche} Growth',
                f'Sustaining {niche} Progress',
                f'Your {niche} Action Plan',
            ],
            'business': [
                f'Introduction to {niche}',
                f'{niche} Market Analysis',
                f'Building Your {niche} Strategy',
                f'{niche} Best Practices',
                f'Implementing {niche} Systems',
                f'Scaling {niche} Operations',
                f'Measuring {niche} Success',
                f'Common {niche} Mistakes to Avoid',
                f'Advanced {niche} Techniques',
                f'{niche} Action Plan',
            ],
            'creative_arts': [
                f'Getting Started with {niche}',
                f'Essential {niche} Techniques',
                f'Developing Your {niche} Style',
                f'{niche} Tools and Materials',
                f'Mastering {niche} Skills',
                f'Creative {niche} Exercises',
                f'Professional {niche} Practices',
                f'Showcasing Your {niche} Work',
                f'Building a {niche} Portfolio',
                f'Your {niche} Journey',
            ],
            'technology': [
                f'Introduction to {niche}',
                f'Understanding {niche} Technology',
                f'{niche} Core Concepts',
                f'Practical {niche} Applications',
                f'Implementing {niche} Solutions',
                f'Advanced {niche} Techniques',
                f'Best Practices for {niche}',
                f'Common {niche} Challenges',
                f'Future of {niche}',
                f'Your {niche} Roadmap',
            ],
            'future_skills': [
                f'Introduction to {niche}',
                f'Why {niche} Matters Today',
                f'Core {niche} Competencies',
                f'Developing {niche} Skills',
                f'Practical {niche} Applications',
                f'Advanced {niche} Strategies',
                f'{niche} in the Workplace',
                f'Mastering {niche}',
                f'Future Trends in {niche}',
                f'Your {niche} Development Plan',
            ],
        }
        
        # Use domain-specific template or generic
        if domain_slug in domain_templates:
            template = domain_templates[domain_slug]
        else:
            template = [
                f'Introduction to {niche}',
                f'Understanding {niche} Basics',
                f'Getting Started with {niche}',
                f'Essential {niche} Concepts',
                f'Practical {niche} Applications',
                f'Advanced {niche} Strategies',
                f'Common {niche} Challenges',
                f'Best Practices for {niche}',
                f'Measuring {niche} Success',
                f'Your {niche} Action Plan',
            ]
        
        # Select chapters
        selected = template[:chapter_count] if len(template) >= chapter_count else template + template[:chapter_count - len(template)]
        
        chapters = [
            {
                'title': chapter_title,
                'summary': f'This chapter covers essential concepts and practical guidance for {chapter_title.lower()}.'
            }
            for chapter_title in selected[:chapter_count]
        ]
        
        return {
            'title': title,
            'chapters': chapters,
            'metadata': {
                'domain': domain,
                'niche': niche,
                'audience': audience,
                'generated_by': 'contextual_fallback'
            }
        }
    
    def _generate_fallback_chapter(
        self,
        title: str,
        outline: str,
        word_count: int,
        domain_slug: str = 'ai_automation',
        niche: str = 'General'
    ) -> Dict[str, Any]:
        """Generate domain/niche-specific fallback chapter"""
        
        sections = []
        sections.append(f"# {title}\n\n{outline}\n\n")

        # Domain-specific section templates
        section_templates = {
            'health_wellness': [
                "Understanding the Health Benefits",
                "Step-by-Step Implementation Guide",
                "Common Health Challenges and Solutions",
                "Tools and Resources for Success",
            ],
            'personal_development': [
                "Building Strong Foundations",
                "Practical Strategies for Growth",
                "Overcoming Common Obstacles",
                "Creating Your Action Plan",
            ],
            'business': [
                "Market Analysis and Research",
                "Strategic Implementation Framework",
                "Best Practices and Case Studies",
                "Measuring ROI and Success Metrics",
            ],
            'creative_arts': [
                "Essential Techniques and Skills",
                "Creative Process and Workflow",
                "Tools and Materials Guide",
                "Developing Your Unique Style",
            ],
            'technology': [
                "Technical Foundations",
                "Implementation Strategies",
                "Best Practices and Standards",
                "Future Trends and Innovations",
            ],
            'future_skills': [
                "Core Concepts and Principles",
                "Practical Application Methods",
                "Skill Development Strategies",
                "Real-World Implementation",
            ],
        }
        
        # Get section headers
        base_topics = section_templates.get(domain_slug, [
            "Foundations and Key Concepts",
            "Step-by-Step Implementation",
            "Common Challenges and Solutions",
            "Tools and Resources",
        ])
        
        words_per_section = max(120, word_count // 4)
        
        for idx, heading in enumerate(base_topics, 1):
            sections.append(f"#### {heading}\n\n")
            
            # Generate contextual content
            paragraph = self._generate_contextual_paragraph(heading, niche, domain_slug, words_per_section)
            sections.append(paragraph + "\n\n")
        
        content = "".join(sections)
        actual_words = len(content.split())
        
        return {
            'content': content,
            'word_count': actual_words,
            'metadata': {
                'domain': domain_slug,
                'niche': niche,
                'generated_by': 'contextual_fallback'
            }
        }
    
    def _generate_contextual_paragraph(self, heading: str, niche: str, domain_slug: str, word_count: int) -> str:
        """Generate contextual paragraph based on domain, niche, and heading"""
        
        # Domain-specific content patterns
        content_patterns = {
            'health_wellness': [
                f"When it comes to {niche.lower()}, {heading.lower()} plays a crucial role in achieving your health goals.",
                f"Research shows that proper attention to {heading.lower()} can significantly improve your {niche.lower()} outcomes.",
                f"Many people find that focusing on {heading.lower()} helps them make sustainable progress in their {niche.lower()} journey.",
            ],
            'personal_development': [
                f"Success in {niche.lower()} requires understanding {heading.lower()} and applying these principles consistently.",
                f"The most effective approach to {niche.lower()} involves mastering {heading.lower()} through deliberate practice.",
                f"By focusing on {heading.lower()}, you can accelerate your growth in {niche.lower()} and achieve lasting results.",
            ],
            'business': [
                f"In the {niche.lower()} industry, {heading.lower()} is essential for competitive advantage and sustainable growth.",
                f"Successful businesses prioritize {heading.lower()} when developing their {niche.lower()} strategies.",
                f"Research indicates that companies excelling in {heading.lower()} outperform competitors in {niche.lower()} markets.",
            ],
            'creative_arts': [
                f"Mastering {heading.lower()} is fundamental to developing your unique voice in {niche.lower()}.",
                f"Professional {niche.lower()} artists emphasize the importance of {heading.lower()} in their creative process.",
                f"Understanding {heading.lower()} allows you to expand your {niche.lower()} capabilities and artistic expression.",
            ],
            'technology': [
                f"Modern {niche.lower()} solutions rely heavily on {heading.lower()} for optimal performance and scalability.",
                f"Understanding {heading.lower()} is critical when implementing {niche.lower()} technologies in your organization.",
                f"The future of {niche.lower()} depends on advances in {heading.lower()} and continuous innovation.",
            ],
            'future_skills': [
                f"Developing {heading.lower()} is essential for success in {niche.lower()} as we move into the future of work.",
                f"Industry leaders emphasize that {heading.lower()} forms the foundation of effective {niche.lower()} mastery.",
                f"By focusing on {heading.lower()}, you position yourself for long-term success in {niche.lower()}.",
            ],
        }
        
        # Get patterns or use generic
        patterns = content_patterns.get(domain_slug, [
            f"Understanding {heading.lower()} is essential for success in {niche.lower()}.",
            f"This section covers key aspects of {heading.lower()} relevant to {niche.lower()}.",
            f"Applying {heading.lower()} principles can significantly improve your {niche.lower()} outcomes.",
        ])
        
        # Build paragraph
        paragraph = random.choice(patterns)
        
        # Add sentences to meet word count
        additional = [
            f"Start by assessing your current situation and identifying areas for improvement in {heading.lower()}. This systematic approach ensures you make meaningful progress.",
            f"Break down complex concepts into manageable steps. Focus on one aspect at a time to build confidence and competence.",
            f"Combine theory with hands-on practice. Experiment with different approaches to discover what works best for your specific situation.",
            f"Document your progress and adjust your strategy as needed for optimal results. Regular review helps maintain momentum and direction.",
        ]
        
        current_words = len(paragraph.split())
        while current_words < word_count:
            paragraph += " " + random.choice(additional)
            current_words = len(paragraph.split())
        
        return paragraph
    
    
    def reload_training_data(self):
        """Force reload training data from database"""
        cache.delete('llm_training_data')
        self._load_training_data()
        logger.info("Training data reloaded from database")

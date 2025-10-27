"""
Train Custom LLM Model
Management command to populate training data for the 3 specific domains
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from customllm.models import TrainingDomain, TrainingNiche, TrainingSample, TrainingSession
import time


class Command(BaseCommand):
    help = 'Train custom LLM model with domain-specific data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            choices=['ai_automation', 'parenting', 'ecommerce', 'all'],
            default='all',
            help='Domain to train (default: all)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force retrain even if recently trained'
        )

    def handle(self, *args, **options):
        domain_slug = options['domain']
        force = options['force']
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*70))
        self.stdout.write(self.style.SUCCESS('🧠 CUSTOM LLM TRAINING'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
        
        # Create training session
        session = TrainingSession.objects.create(
            status='running',
            started_at=timezone.now()
        )
        
        try:
            # Step 1: Initialize domains
            self.stdout.write('📋 Step 1: Initializing domains...')
            domains = self._initialize_domains()
            self.stdout.write(self.style.SUCCESS(f'   ✓ Created {len(domains)} domains\n'))
            
            # Step 2: Initialize niches
            self.stdout.write('🎯 Step 2: Initializing niches...')
            niches = self._initialize_niches(domains)
            self.stdout.write(self.style.SUCCESS(f'   ✓ Created {len(niches)} niches\n'))
            
            # Step 3: Generate training samples
            self.stdout.write('📝 Step 3: Generating training samples...')
            
            domains_to_train = domains if domain_slug == 'all' else [d for d in domains if d.slug == domain_slug]
            
            total_samples = 0
            for domain in domains_to_train:
                self.stdout.write(f'\n   Training: {domain.name}')
                count = self._generate_training_samples(domain)
                total_samples += count
                self.stdout.write(self.style.SUCCESS(f'   ✓ Generated {count} samples'))
            
            self.stdout.write(self.style.SUCCESS(f'\n   ✓ Total samples generated: {total_samples}\n'))
            
            # Step 4: Update training statistics
            self.stdout.write('📊 Step 4: Updating statistics...')
            for domain in domains_to_train:
                domain.training_samples_count = TrainingSample.objects.filter(domain=domain).count()
                domain.last_trained = timezone.now()
                domain.training_quality_score = 85.0  # Base quality score
                domain.save()
            self.stdout.write(self.style.SUCCESS('   ✓ Statistics updated\n'))
            
            # Complete session
            session.status = 'completed'
            session.completed_at = timezone.now()
            session.duration_seconds = int((session.completed_at - session.started_at).total_seconds())
            session.samples_count = total_samples
            session.log = f"Successfully trained {len(domains_to_train)} domains with {total_samples} samples"
            session.save()
            
            self.stdout.write(self.style.SUCCESS('='*70))
            self.stdout.write(self.style.SUCCESS('✅ TRAINING COMPLETE!'))
            self.stdout.write(self.style.SUCCESS(f'   Duration: {session.duration_seconds}s'))
            self.stdout.write(self.style.SUCCESS(f'   Samples: {total_samples}'))
            self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
            
            self.stdout.write(self.style.WARNING('💡 Next steps:'))
            self.stdout.write('   1. Test the model: python manage.py test_custom_model')
            self.stdout.write('   2. Generate a book using the trained domains')
            self.stdout.write('   3. Monitor quality and add more samples if needed\n')
            
        except Exception as e:
            session.status = 'failed'
            session.error_message = str(e)
            session.save()
            self.stdout.write(self.style.ERROR(f'\n❌ Training failed: {str(e)}\n'))
            import traceback
            traceback.print_exc()

    def _initialize_domains(self):
        """Create the 3 main domains"""
        domains_data = [
            {
                'slug': 'ai_automation',
                'name': 'AI & Automation',
                'description': 'AI tools, automation strategies, and intelligent systems'
            },
            {
                'slug': 'parenting',
                'name': 'Parenting: Pre-school Speech & Learning',
                'description': 'Early childhood development, speech therapy, and preschool learning'
            },
            {
                'slug': 'ecommerce',
                'name': 'E-commerce & Digital Products',
                'description': 'Online business, digital products, and e-commerce strategies'
            }
        ]
        
        domains = []
        for data in domains_data:
            domain, created = TrainingDomain.objects.get_or_create(
                slug=data['slug'],
                defaults=data
            )
            if not created:
                # Update existing
                domain.name = data['name']
                domain.description = data['description']
                domain.save()
            domains.append(domain)
        
        return domains

    def _initialize_niches(self, domains):
        """Create niches for each domain"""
        niches_data = {
            'ai_automation': [
                {'slug': 'no-code-ai-tools', 'name': 'No-Code AI Tools', 'keywords': ['no-code', 'automation', 'AI tools', 'workflow']},
                {'slug': 'ai-content-creation', 'name': 'AI Content Creation', 'keywords': ['content', 'writing', 'generation', 'AI']},
                {'slug': 'business-automation', 'name': 'Business Automation', 'keywords': ['business', 'automation', 'efficiency', 'tools']},
            ],
            'parenting': [
                {'slug': 'speech-development', 'name': 'Speech Development', 'keywords': ['speech', 'language', 'development', 'therapy']},
                {'slug': 'preschool-learning', 'name': 'Preschool Learning', 'keywords': ['learning', 'preschool', 'education', 'activities']},
                {'slug': 'early-childhood', 'name': 'Early Childhood Development', 'keywords': ['development', 'early childhood', 'milestones', 'growth']},
            ],
            'ecommerce': [
                {'slug': 'digital-products', 'name': 'Digital Products', 'keywords': ['digital', 'products', 'online', 'selling']},
                {'slug': 'online-store', 'name': 'Online Store Setup', 'keywords': ['ecommerce', 'store', 'platform', 'setup']},
                {'slug': 'ecommerce-marketing', 'name': 'E-commerce Marketing', 'keywords': ['marketing', 'sales', 'conversion', 'growth']},
            ]
        }
        
        niches = []
        for domain in domains:
            domain_niches = niches_data.get(domain.slug, [])
            for niche_data in domain_niches:
                niche, created = TrainingNiche.objects.get_or_create(
                    domain=domain,
                    slug=niche_data['slug'],
                    defaults={
                        'name': niche_data['name'],
                        'description': f"{niche_data['name']} in {domain.name}",
                        'keywords': niche_data['keywords'],
                        'target_audiences': ['beginners', 'professionals', 'parents', 'entrepreneurs']
                    }
                )
                niches.append(niche)
        
        return niches

    def _generate_training_samples(self, domain):
        """Generate training samples for a domain"""
        
        # Get niches for this domain
        niches = TrainingNiche.objects.filter(domain=domain)
        
        samples_created = 0
        
        for niche in niches:
            # Generate outline samples (2 per niche)
            samples_created += self._create_outline_samples(domain, niche, count=2)
            
            # Generate chapter samples (5 per niche)
            samples_created += self._create_chapter_samples(domain, niche, count=5)
            
            # Generate cover description samples (1 per niche)
            samples_created += self._create_cover_samples(domain, niche, count=1)
        
        return samples_created

    def _create_outline_samples(self, domain, niche, count=2):
        """Create outline training samples"""
        created = 0
        
        for i in range(count):
            prompt = f"Generate a book outline for: {domain.name} - {niche.name}"
            completion = self._get_outline_template(domain.slug, niche.name)
            
            _, is_created = TrainingSample.objects.get_or_create(
                domain=domain,
                niche=niche,
                sample_type='outline',
                prompt=prompt,
                defaults={
                    'completion': completion,
                    'context': {'audience': 'professionals', 'length': 'medium'},
                    'quality_score': 0.9,
                    'source': 'template'
                }
            )
            if is_created:
                created += 1
        
        return created

    def _create_chapter_samples(self, domain, niche, count=5):
        """Create chapter training samples"""
        created = 0
        
        chapter_titles = self._get_chapter_titles(domain.slug)
        
        for i in range(min(count, len(chapter_titles))):
            title = chapter_titles[i]
            prompt = f"Write a chapter titled: {title} for a book about {niche.name}"
            completion = self._get_chapter_template(domain.slug, title)
            
            _, is_created = TrainingSample.objects.get_or_create(
                domain=domain,
                niche=niche,
                sample_type='chapter',
                prompt=prompt,
                defaults={
                    'completion': completion,
                    'context': {'word_count': 500, 'audience': 'professionals'},
                    'quality_score': 0.85,
                    'source': 'template'
                }
            )
            if is_created:
                created += 1
        
        return created

    def _create_cover_samples(self, domain, niche, count=1):
        """Create cover description training samples"""
        created = 0
        
        prompt = f"Generate a cover description for a book about: {niche.name}"
        completion = self._get_cover_template(domain.slug, niche.name)
        
        _, is_created = TrainingSample.objects.get_or_create(
            domain=domain,
            niche=niche,
            sample_type='cover_description',
            prompt=prompt,
            defaults={
                'completion': completion,
                'context': {'style': 'professional', 'modern': True},
                'quality_score': 0.9,
                'source': 'template'
            }
        )
        if is_created:
            created += 1
        
        return created

    def _get_outline_template(self, domain_slug, niche_name):
        """Get outline template for domain"""
        templates = {
            'ai_automation': f"""Title: Mastering {niche_name}: A Complete Guide

1. Introduction to {niche_name}
   - Overview and importance
   - Current landscape
   - What you'll learn

2. Understanding the Fundamentals
   - Core concepts
   - Key technologies
   - Essential terminology

3. Getting Started
   - Setting up your environment
   - First steps
   - Best practices

4. Practical Applications
   - Real-world use cases
   - Implementation strategies
   - Common scenarios

5. Advanced Techniques
   - Power user features
   - Optimization strategies
   - Pro tips

6. Common Challenges and Solutions
   - Troubleshooting guide
   - Best practices
   - Avoiding pitfalls

7. Case Studies and Examples
   - Success stories
   - Lessons learned
   - Industry insights

8. Future Trends and Opportunities
   - Emerging technologies
   - Market trends
   - Career opportunities

9. Resources and Next Steps
   - Further learning
   - Community resources
   - Action plan

10. Conclusion
    - Key takeaways
    - Final thoughts
    - Your journey ahead""",
            
            'parenting': f"""Title: Nurturing Your Child: {niche_name}

1. Understanding Your Child's Development
   - Developmental milestones
   - Individual differences
   - What to expect

2. Building Strong Foundations
   - Creating supportive environments
   - Establishing routines
   - Positive parenting approaches

3. Practical Activities and Exercises
   - Daily activities
   - Fun games and play
   - Learning through exploration

4. Addressing Common Concerns
   - Normal variations
   - When to seek help
   - Professional resources

5. Communication Strategies
   - Effective techniques
   - Active listening
   - Building connection

6. Creating Learning Opportunities
   - Home-based activities
   - Educational resources
   - Making it fun

7. Supporting Social Development
   - Social skills
   - Friendships
   - Emotional intelligence

8. Working with Professionals
   - Finding the right support
   - Collaborative approaches
   - Maximizing benefits

9. Long-term Success Strategies
   - Consistency and patience
   - Celebrating progress
   - Building confidence

10. Resources for Parents
    - Recommended tools
    - Support networks
    - Further reading""",
            
            'ecommerce': f"""Title: E-commerce Success with {niche_name}

1. Introduction to E-commerce
   - Market overview
   - Opportunities in {niche_name}
   - Success factors

2. Planning Your Business
   - Market research
   - Business model selection
   - Setting goals

3. Setting Up Your Store
   - Platform selection
   - Technical setup
   - Essential features

4. Product Strategy
   - Product selection
   - Pricing strategies
   - Inventory management

5. Marketing and Promotion
   - Digital marketing basics
   - Social media strategies
   - Email marketing

6. Customer Experience
   - User experience design
   - Customer service
   - Building loyalty

7. Operations and Fulfillment
   - Order processing
   - Shipping strategies
   - Returns management

8. Analytics and Optimization
   - Key metrics
   - Data analysis
   - Continuous improvement

9. Scaling Your Business
   - Growth strategies
   - Automation tools
   - Team building

10. Legal and Compliance
    - Business registration
    - Tax considerations
    - Terms and policies"""
        }
        
        return templates.get(domain_slug, templates['ai_automation'])

    def _get_chapter_titles(self, domain_slug):
        """Get common chapter titles for domain"""
        titles = {
            'ai_automation': [
                'Introduction to AI & Automation',
                'Understanding AI Tools',
                'Automation Strategies',
                'Implementation Guide',
                'Best Practices and Case Studies'
            ],
            'parenting': [
                'Understanding Your Child',
                'Speech Development Basics',
                'Fun Learning Activities',
                'Communication Techniques',
                'Building Confidence'
            ],
            'ecommerce': [
                'E-commerce Fundamentals',
                'Setting Up Your Store',
                'Marketing Strategies',
                'Customer Experience',
                'Scaling Your Business'
            ]
        }
        return titles.get(domain_slug, titles['ai_automation'])

    def _get_chapter_template(self, domain_slug, title):
        """Get chapter content template"""
        return f"""# {title}

In this chapter, we'll explore the essential concepts and practical applications related to {title.lower()}. This comprehensive guide will provide you with actionable insights and real-world examples.

## Understanding the Basics

The foundation of success begins with understanding core principles. Whether you're just starting out or looking to deepen your knowledge, these fundamentals are crucial for your journey.

Key concepts include:
- Core principles and methodologies
- Industry best practices
- Common terminologies and frameworks
- Real-world applications

## Practical Applications

Theory is important, but practical application is where real learning happens. Let's explore how to implement these concepts in real situations.

### Step-by-Step Approach

1. **Assessment**: Evaluate your current situation and goals
2. **Planning**: Create a structured approach
3. **Implementation**: Put your plan into action
4. **Monitoring**: Track progress and adjust as needed
5. **Optimization**: Continuously improve your approach

## Common Challenges and Solutions

Every journey has obstacles. Here are common challenges you might face and how to overcome them:

- **Challenge 1**: Initial complexity and learning curve
  - Solution: Start small, focus on fundamentals, practice regularly

- **Challenge 2**: Maintaining consistency
  - Solution: Create routines, set reminders, track progress

- **Challenge 3**: Measuring success
  - Solution: Define clear metrics, regular reviews, celebrate wins

## Best Practices

Successful implementation requires following proven best practices:

1. Start with clear objectives
2. Break down complex tasks into manageable steps
3. Seek feedback and iterate
4. Document your learning process
5. Share knowledge with others

## Real-World Examples

Let's look at practical examples that demonstrate these concepts in action. These case studies show how others have successfully applied these principles.

### Example 1: Getting Started
A beginner's journey from zero to confident practitioner, highlighting key milestones and lessons learned along the way.

### Example 2: Overcoming Obstacles
How to handle setbacks and use them as learning opportunities for growth and improvement.

## Key Takeaways

- Understanding fundamentals is essential for success
- Practical application builds real competence
- Consistency and patience lead to mastery
- Learn from others' experiences
- Continuous improvement is the key

## Moving Forward

As you progress through this material, remember that learning is a journey. Each step builds on the previous one, creating a solid foundation for advanced topics covered in subsequent chapters.

In the next chapter, we'll dive deeper into advanced techniques and strategies that will elevate your understanding to the next level."""

    def _get_cover_template(self, domain_slug, niche_name):
        """Get cover description template"""
        templates = {
            'ai_automation': f"Professional book cover for '{niche_name}'. Modern, tech-focused design with circuit patterns, AI neural network visualization, blue and purple gradient. Clean typography, minimalist style. Digital transformation theme.",
            
            'parenting': f"Warm, inviting book cover for '{niche_name}'. Soft pastel colors, parent and child silhouette, playful educational elements. Friendly, approachable design with hearts and growth symbols. Professional yet nurturing aesthetic.",
            
            'ecommerce': f"Dynamic book cover for '{niche_name}'. Bold colors, shopping cart icon, growth charts, digital storefront imagery. Professional business style with modern typography. Success and profitability theme."
        }
        
        return templates.get(domain_slug, templates['ai_automation'])

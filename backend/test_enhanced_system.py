"""
Comprehensive Test Suite for Enhanced Multi-LLM Architecture
Tests all generation paths with Cloudflare integration
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.models import Book, Domain, Niche, BookStyle, FontTheme
from books.services.llm_orchestrator import LLMOrchestrator, CloudflareAIClient
from books.services.pdf_generator_pro import ProfessionalPDFGenerator
from django.contrib.auth.models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComprehensiveTestSuite:
    """
    Test all book generation paths with new architecture
    """
    
    def __init__(self):
        self.test_user = self._get_or_create_test_user()
        self.llm = LLMOrchestrator()
        self.cloudflare = CloudflareAIClient()
        self.results = []
    
    def _get_or_create_test_user(self):
        """Get or create test user"""
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('testpass123')
            user.save()
        return user
    
    def test_1_llm_orchestrator_outline(self):
        """Test LLM Orchestrator outline generation"""
        logger.info("\n===  TEST 1: LLM Orchestrator Outline Generation ===")
        
        try:
            book_context = {
                'title': 'The Complete Guide to Digital Products',
                'domain': 'E-commerce & Digital Products',
                'niche': 'Digital Product Creation',
                'audience': 'Content creators and course makers',
                'length': 'medium'
            }
            
            outline = self.llm.generate_outline(book_context)
            
            assert outline, "Outline generation failed"
            assert len(outline) > 200, "Outline too short"
            assert 'introduction' in outline.lower() or 'chapter' in outline.lower(), "Outline missing key sections"
            
            logger.info(f"✓ Outline generated successfully ({len(outline)} chars)")
            logger.info(f"Preview: {outline[:200]}...")
            self.results.append(("LLM Outline Generation", "PASS"))
            return True
            
        except Exception as e:
            logger.error(f"✗ Outline generation failed: {str(e)}")
            self.results.append(("LLM Outline Generation", f"FAIL: {str(e)}"))
            return False
    
    def test_2_llm_chapter_generation(self):
        """Test chapter generation with length validation"""
        logger.info("\n=== TEST 2: LLM Chapter Generation with Token Validation ===")
        
        try:
            book_context = {
                'title': 'AI Automation Handbook',
                'domain': 'AI & Automation',
                'audience': 'Business professionals',
                'niche': 'Workflow Automation'
            }
            
            chapter_title = "Understanding Automation Fundamentals"
            
            # Test with different length settings
            for length in ['short', 'medium', 'full']:
                logger.info(f"\nTesting {length} length setting...")
                content = self.llm.generate_chapter_content(
                    chapter_title, 
                    book_context,
                    length_setting=length
                )
                
                token_count = self.cloudflare.count_tokens(content)
                threshold = self.llm.token_thresholds[length]
                
                logger.info(f"Generated {token_count} tokens (threshold: {threshold['min']}-{threshold['max']})")
                
                assert content, f"Chapter generation failed for {length}"
                assert token_count >= threshold['min'] * 0.8, f"Chapter too short for {length}: {token_count} < {threshold['min']}"
                
                logger.info(f"✓ {length.capitalize()} chapter generated successfully")
            
            self.results.append(("LLM Chapter Generation", "PASS"))
            return True
            
        except Exception as e:
            logger.error(f"✗ Chapter generation failed: {str(e)}")
            self.results.append(("LLM Chapter Generation", f"FAIL: {str(e)}"))
            return False
    
    def test_3_content_review_refinement(self):
        """Test content review and recursive rewriting"""
        logger.info("\n=== TEST 3: Content Review & Refinement ===")
        
        try:
            sample_content = """
            This is a brief introduction to automation. Automation helps businesses save time.
            It can reduce manual work. Many companies use automation today.
            """
            
            refinement_goals = [
                "Expand to at least 200 words",
                "Add concrete examples",
                "Include statistics",
                "Improve professional tone"
            ]
            
            refined = self.llm.review_and_refine_content(sample_content, refinement_goals)
            
            assert refined, "Content refinement failed"
            assert len(refined) > len(sample_content), "Refined content not expanded"
            
            original_tokens = self.cloudflare.count_tokens(sample_content)
            refined_tokens = self.cloudflare.count_tokens(refined)
            
            logger.info(f"✓ Content refined: {original_tokens} → {refined_tokens} tokens ({refined_tokens/original_tokens:.1f}x expansion)")
            self.results.append(("Content Review & Refinement", "PASS"))
            return True
            
        except Exception as e:
            logger.error(f"✗ Content refinement failed: {str(e)}")
            self.results.append(("Content Review & Refinement", f"FAIL: {str(e)}"))
            return False
    
    def test_4_font_theme_selection(self):
        """Test FontTheme AI-based selection"""
        logger.info("\n=== TEST 4: Font Theme Selection ===")
        
        try:
            # Test different cover briefs
            test_cases = [
                ("Modern minimal design with clean typography and tech-forward aesthetic", "Tech Modern"),
                ("Playful friendly design for kids with warm colors", "Friendly Rounded"),
                ("Elegant sophisticated design with classic serif fonts", "Elegant Serif"),
            ]
            
            for brief, expected_category in test_cases:
                # Get e-commerce domain for testing
                domain = Domain.objects.filter(slug='ecommerce_digital_products').first()
                
                theme = FontTheme.select_font_theme_from_brief(brief, domain)
                
                assert theme, f"Font theme selection failed for: {brief[:50]}"
                logger.info(f"✓ Selected theme: {theme.name} (category: {theme.category})")
            
            self.results.append(("Font Theme Selection", "PASS"))
            return True
            
        except Exception as e:
            logger.error(f"✗ Font theme selection failed: {str(e)}")
            self.results.append(("Font Theme Selection", f"FAIL: {str(e)}"))
            return False
    
    def test_5_pdf_generation_with_fonts(self):
        """Test PDF generation with dynamic font selection"""
        logger.info("\n=== TEST 5: PDF Generation with Dynamic Fonts ===")
        
        try:
            # Create test book
            domain = Domain.objects.filter(slug='ecommerce_digital_products').first()
            niche = Niche.objects.filter(domain=domain).first()
            book_style = BookStyle.objects.first()
            
            book = Book.objects.create(
                user=self.test_user,
                title="Test Book: Digital Product Mastery",
                domain=domain,
                niche=niche,
                book_style=book_style,
                status='draft'
            )
            
            # Test cover brief
            cover_brief = "Professional modern design with clean typography for e-commerce"
            
            # Create PDF generator with font theme
            pdf_gen = ProfessionalPDFGenerator.create_with_book_context(book, cover_brief)
            
            assert pdf_gen.font_theme, "Font theme not selected"
            assert pdf_gen.header_font, "Header font not set"
            assert pdf_gen.body_font, "Body font not set"
            
            logger.info(f"✓ PDF Generator created with theme: {pdf_gen.font_theme.name}")
            logger.info(f"  Header font: {pdf_gen.header_font}")
            logger.info(f"  Body font: {pdf_gen.body_font}")
            
            # Clean up
            book.delete()
            
            self.results.append(("PDF Generation with Fonts", "PASS"))
            return True
            
        except Exception as e:
            logger.error(f"✗ PDF generation with fonts failed: {str(e)}")
            self.results.append(("PDF Generation with Fonts", f"FAIL: {str(e)}"))
            return False
    
    def test_6_cloudflare_integration(self):
        """Test Cloudflare AI integration"""
        logger.info("\n=== TEST 6: Cloudflare AI Integration ===")
        
        try:
            # Test token counting
            test_text = "This is a test of the Cloudflare token counting system. " * 10
            token_count = self.cloudflare.count_tokens(test_text)
            
            assert token_count > 0, "Token counting failed"
            logger.info(f"✓ Token counting works: {token_count} tokens for test text")
            
            # Test Cloudflare API availability
            if self.cloudflare.api_key:
                logger.info("✓ Cloudflare API key configured")
                
                # Test image generation (only if API key exists)
                # prompt = "Professional book cover design, modern minimal style"
                # image_data = self.cloudflare.generate_image(prompt)
                
                # if image_data:
                #     logger.info("✓ Cloudflare image generation successful")
                # else:
                #     logger.warning("⚠ Cloudflare image generation returned no data (may be rate limited)")
            else:
                logger.warning("⚠ Cloudflare API key not configured - skipping image generation test")
            
            self.results.append(("Cloudflare Integration", "PASS"))
            return True
            
        except Exception as e:
            logger.error(f"✗ Cloudflare integration test failed: {str(e)}")
            self.results.append(("Cloudflare Integration", f"FAIL: {str(e)}"))
            return False
    
    def test_7_new_domains_and_niches(self):
        """Test new domains and micro-workflows"""
        logger.info("\n=== TEST 7: New Domains & Micro-workflows ===")
        
        try:
            new_domains = [
                'ecommerce_digital_products',
                'parenting_preschool_learning',
                'ai_automation'
            ]
            
            for domain_slug in new_domains:
                domain = Domain.objects.filter(slug=domain_slug).first()
                assert domain, f"Domain {domain_slug} not found"
                
                niches = Niche.objects.filter(domain=domain)
                assert niches.count() >= 5, f"Domain {domain.name} has insufficient micro-workflows: {niches.count()}"
                
                logger.info(f"✓ Domain: {domain.name} ({niches.count()} micro-workflows)")
                for niche in niches[:3]:
                    logger.info(f"  - {niche.name}")
            
            self.results.append(("New Domains & Niches", "PASS"))
            return True
            
        except Exception as e:
            logger.error(f"✗ Domain/niche test failed: {str(e)}")
            self.results.append(("New Domains & Niches", f"FAIL: {str(e)}"))
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        logger.info("\n" + "="*70)
        logger.info("COMPREHENSIVE TEST SUITE - Multi-LLM Architecture with Cloudflare")
        logger.info("="*70 + "\n")
        
        tests = [
            self.test_1_llm_orchestrator_outline,
            self.test_2_llm_chapter_generation,
            self.test_3_content_review_refinement,
            self.test_4_font_theme_selection,
            self.test_5_pdf_generation_with_fonts,
            self.test_6_cloudflare_integration,
            self.test_7_new_domains_and_niches,
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Test execution error: {str(e)}")
                failed += 1
        
        # Print summary
        logger.info("\n" + "="*70)
        logger.info("TEST SUMMARY")
        logger.info("="*70)
        logger.info(f"\nTotal Tests: {len(tests)}")
        logger.info(f"Passed: {passed} ✓")
        logger.info(f"Failed: {failed} ✗")
        logger.info(f"Success Rate: {(passed/len(tests)*100):.1f}%\n")
        
        logger.info("Detailed Results:")
        logger.info("-" * 70)
        for test_name, result in self.results:
            status_icon = "✓" if result == "PASS" else "✗"
            logger.info(f"{status_icon} {test_name}: {result}")
        
        logger.info("\n" + "="*70 + "\n")
        
        return passed, failed


if __name__ == "__main__":
    suite = ComprehensiveTestSuite()
    passed, failed = suite.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)

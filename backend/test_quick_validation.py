#!/usr/bin/env python
"""
Quick Validation Test - LLM Orchestrator with Working Models
Tests all 4 core functions quickly
"""

import os
import sys
import django
import logging

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.services.llm_orchestrator import LLMOrchestrator
from books.models import Domain, FontTheme

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_quick():
    """Quick validation of all components"""
    
    print("\n" + "="*70)
    print("QUICK VALIDATION TEST - Multi-LLM Orchestrator")
    print("="*70 + "\n")
    
    llm = LLMOrchestrator()
    results = {"passed": 0, "failed": 0}
    
    # Test 1: Outline Generation (MiniMax M2)
    print("1️⃣  Testing Outline Generation (minimax/minimax-m2:free)...")
    try:
        outline = llm.generate_outline({
            'title': 'Quick Test Guide',
            'domain': 'E-commerce',
            'niche': 'Dropshipping',
            'audience': 'Entrepreneurs',
            'length': 'short'
        })
        if outline and len(outline) > 100:
            print(f"   ✅ PASS - Generated {len(outline)} chars")
            print(f"   Preview: {outline[:150]}...")
            results["passed"] += 1
        else:
            print(f"   ❌ FAIL - Output too short: {len(outline)} chars")
            results["failed"] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)[:100]}")
        results["failed"] += 1
    
    # Test 2: Short Chapter Generation (NVIDIA Nemotron) with strict max_tokens
    print("\n2️⃣  Testing Chapter Generation (nvidia/nemotron-nano-9b-v2:free)...")
    try:
        # Override max_tokens to get quick response
        chapter = llm.generate_chapter_content(
            chapter_title="Introduction to Digital Products",
            book_context={
                'title': 'Quick Test',
                'domain': 'E-commerce',
                'outline': 'Test outline'
            },
            length_setting='short'
        )
        if chapter and len(chapter) > 100:
            word_count = len(chapter.split())
            print(f"   ✅ PASS - Generated {word_count} words ({len(chapter)} chars)")
            print(f"   Preview: {chapter[:150]}...")
            results["passed"] += 1
        else:
            print(f"   ❌ FAIL - Output too short")
            results["failed"] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)[:100]}")
        results["failed"] += 1
    
    # Test 3: Content Review (Mistral Small)
    print("\n3️⃣  Testing Content Review (mistralai/mistral-small-3.2-24b-instruct:free)...")
    try:
        test_content = "Digital products are items sold online. They include ebooks and courses."
        refined = llm.review_and_refine_content(
            content=test_content,
            chapter_title="Introduction",
            book_context={'title': 'Test Book'}
        )
        if refined and len(refined) > len(test_content):
            print(f"   ✅ PASS - Expanded {len(test_content)} → {len(refined)} chars")
            print(f"   Preview: {refined[:150]}...")
            results["passed"] += 1
        else:
            print(f"   ❌ FAIL - Not expanded properly")
            results["failed"] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)[:100]}")
        results["failed"] += 1
    
    # Test 4: Cover Brief Generation (Google Gemma)
    print("\n4️⃣  Testing Cover Brief (google/gemma-3n-e2b-it:free)...")
    try:
        brief = llm.generate_cover_brief({
            'title': 'Digital Products Mastery',
            'domain': 'E-commerce',
            'niche': 'Digital Products',
            'style': 'Professional Modern'
        })
        if brief and len(brief) > 50:
            print(f"   ✅ PASS - Generated {len(brief)} chars")
            print(f"   Preview: {brief[:150]}...")
            results["passed"] += 1
        else:
            print(f"   ❌ FAIL - Output too short")
            results["failed"] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)[:100]}")
        results["failed"] += 1
    
    # Test 5: Font Theme Selection (Infrastructure)
    print("\n5️⃣  Testing Font Theme Selection...")
    try:
        domain = Domain.objects.get(slug='ecommerce_digital_products')
        theme = FontTheme.select_font_theme_from_brief(
            "Bold modern e-commerce design",
            domain
        )
        if theme:
            print(f"   ✅ PASS - Selected: {theme.name}")
            print(f"   Fonts: {theme.header_font} + {theme.body_font}")
            results["passed"] += 1
        else:
            print(f"   ❌ FAIL - No theme selected")
            results["failed"] += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)}")
        results["failed"] += 1
    
    # Summary
    total = results["passed"] + results["failed"]
    success_rate = (results["passed"] / total * 100) if total > 0 else 0
    
    print("\n" + "="*70)
    print("RESULTS SUMMARY")
    print("="*70)
    print(f"✅ Passed: {results['passed']}/{total}")
    print(f"❌ Failed: {results['failed']}/{total}")
    print(f"📊 Success Rate: {success_rate:.1f}%")
    print("="*70 + "\n")
    
    return results["failed"] == 0

if __name__ == '__main__':
    success = test_quick()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Workflow Fix Validation Script
Validates that domain-niche relationships are correctly set up
Run: python validate_workflow_fixes.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, '/home/badr/book-generator/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from books.models import Domain, Niche, BookStyle, CoverStyle
from django.db.models import Count


def validate_domain_niche_relationships():
    """Validate that each domain has its own unique niches"""
    print("\n" + "="*80)
    print("DOMAIN-NICHE RELATIONSHIP VALIDATION")
    print("="*80)
    
    domains = Domain.objects.filter(is_active=True)
    
    if domains.count() == 0:
        print("❌ ERROR: No active domains found!")
        return False
    
    print(f"\n✅ Found {domains.count()} active domains\n")
    
    all_valid = True
    niche_ids_seen = set()
    
    for domain in domains:
        niches = domain.niches.filter(is_active=True)
        niche_count = niches.count()
        
        print(f"📁 {domain.name} ({domain.slug})")
        print(f"   Niches: {niche_count}")
        
        if niche_count == 0:
            print(f"   ⚠️  WARNING: Domain has no niches!")
            all_valid = False
        
        # Check for duplicate niches across domains
        for niche in niches:
            if niche.id in niche_ids_seen:
                print(f"   ❌ ERROR: Niche '{niche.name}' appears in multiple domains!")
                all_valid = False
            niche_ids_seen.add(niche.id)
            print(f"   - {niche.name}")
        
        print()
    
    return all_valid


def validate_cover_styles():
    """Validate cover styles exist and are active"""
    print("\n" + "="*80)
    print("COVER STYLE VALIDATION")
    print("="*80)
    
    cover_styles = CoverStyle.objects.filter(is_active=True)
    
    if cover_styles.count() == 0:
        print("❌ ERROR: No active cover styles found!")
        return False
    
    print(f"\n✅ Found {cover_styles.count()} active cover styles\n")
    
    expected_styles = ['minimalist', 'futuristic', 'playful', 'elegant', 'corporate', 'artistic']
    found_styles = set(cover_styles.values_list('style', flat=True))
    
    for style in expected_styles:
        if style in found_styles:
            style_obj = cover_styles.filter(style=style).first()
            print(f"✅ {style.title():15} - {style_obj.name}")
        else:
            print(f"⚠️  {style.title():15} - NOT FOUND")
    
    print()
    return True


def validate_book_styles():
    """Validate book styles exist"""
    print("\n" + "="*80)
    print("BOOK STYLE VALIDATION")
    print("="*80)
    
    book_styles = BookStyle.objects.filter(is_active=True)
    
    if book_styles.count() == 0:
        print("❌ ERROR: No active book styles found!")
        return False
    
    print(f"\n✅ Found {book_styles.count()} active book styles\n")
    
    for style in book_styles:
        print(f"📖 {style.name}")
        print(f"   Tone: {style.tone}")
        print(f"   Audience: {style.target_audience}")
        print(f"   Length: {style.length}")
        print()
    
    return True


def test_niche_filtering():
    """Test that niche filtering by domain works"""
    print("\n" + "="*80)
    print("NICHE FILTERING TEST")
    print("="*80)
    
    domains = Domain.objects.filter(is_active=True)[:3]  # Test first 3 domains
    
    for domain in domains:
        print(f"\n🔍 Testing filter for domain: {domain.name} (slug={domain.slug})")
        
        # Test by ID
        niches_by_id = Niche.objects.filter(domain__id=domain.id, is_active=True)
        print(f"   Filter by ID ({domain.id}): {niches_by_id.count()} niches")
        
        # Test by slug
        niches_by_slug = Niche.objects.filter(domain__slug=domain.slug, is_active=True)
        print(f"   Filter by slug ({domain.slug}): {niches_by_slug.count()} niches")
        
        if niches_by_id.count() != niches_by_slug.count():
            print(f"   ❌ ERROR: ID and slug filtering return different counts!")
            return False
        
        if niches_by_id.count() > 0:
            print(f"   ✅ Filtering works correctly")
        else:
            print(f"   ⚠️  WARNING: No niches found for this domain")
    
    print()
    return True


def main():
    """Run all validations"""
    print("\n" + "="*80)
    print("WORKFLOW FIX VALIDATION SCRIPT")
    print("Date: October 29, 2025")
    print("="*80)
    
    results = {
        'Domain-Niche Relationships': validate_domain_niche_relationships(),
        'Cover Styles': validate_cover_styles(),
        'Book Styles': validate_book_styles(),
        'Niche Filtering': test_niche_filtering()
    }
    
    print("\n" + "="*80)
    print("VALIDATION RESULTS SUMMARY")
    print("="*80 + "\n")
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status:12} - {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL VALIDATIONS PASSED!")
        print("="*80 + "\n")
        return 0
    else:
        print("❌ SOME VALIDATIONS FAILED - Please review above")
        print("="*80 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

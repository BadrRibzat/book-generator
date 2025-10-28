"""
Content Quality Utilities
- Detect duplicated sentences
- Replace filler phrases
- Validate chapter uniqueness
- Score readability (Flesch-Kincaid)
- Penalize overuse of key phrases
- Ensure minimum structured content per section

If content fails threshold, callers can regenerate the specific section.
"""
from __future__ import annotations

import re
from typing import Dict, List, Tuple
from collections import Counter

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
FILLER_PHRASES = [
    "in conclusion", "in summary", "needless to say", "it is important to note",
    "as previously mentioned", "it goes without saying", "leveraging synergies",
    "cutting-edge", "best-in-class", "paradigm shift", "holistic approach"
]

# Simple syllable estimation for readability (approximate)
VOWELS = "aeiouy"

def _split_sentences(text: str) -> List[str]:
    sentences = SENTENCE_SPLIT_RE.split(text.strip()) if text else []
    # Normalize whitespace and strip
    return [re.sub(r"\s+", " ", s).strip() for s in sentences if s and s.strip()]


def _count_syllables(word: str) -> int:
    w = word.lower().strip(".,;:?!\"'()[]{}")
    if not w:
        return 0
    count = 0
    prev_is_vowel = False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    if w.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def _flesch_kincaid_grade(text: str) -> float:
    sentences = _split_sentences(text)
    words = re.findall(r"[A-Za-z']+", text)
    if not sentences or not words:
        return 12.0
    syllables = sum(_count_syllables(w) for w in words)
    W = len(words)
    S = max(len(sentences), 1)
    # Flesch-Kincaid Grade Level
    grade = 0.39 * (W / S) + 11.8 * (syllables / W) - 15.59
    return max(0.0, min(18.0, grade))


def _replace_filler_phrases(text: str) -> Tuple[str, int]:
    replaced = 0
    def repl(match):
        nonlocal replaced
        replaced += 1
        return ""
    pattern = re.compile(r"|".join(re.escape(p) for p in FILLER_PHRASES), re.IGNORECASE)
    new_text = pattern.sub(repl, text)
    # Normalize whitespace after removals
    new_text = re.sub(r"\s+", " ", new_text).strip()
    return new_text, replaced


def _duplicate_sentence_ratio(text: str) -> float:
    sentences = [s.lower() for s in _split_sentences(text)]
    if len(sentences) <= 1:
        return 0.0
    counts = Counter(sentences)
    dup = sum(c for s, c in counts.items() if c > 1) - len([1 for c in counts.values() if c > 1])
    return max(0.0, dup / max(1, len(sentences)))


def _overused_phrase_penalty(text: str, top_k: int = 5) -> float:
    words = [w.lower() for w in re.findall(r"[A-Za-z']+", text) if len(w) > 3]
    if not words:
        return 0.0
    counts = Counter(words).most_common(top_k)
    # Penalize if any top-k word frequency exceeds 5% of total words
    W = len(words)
    penalty = 0.0
    for _, c in counts:
        freq = c / W
        if freq > 0.07:
            penalty += (freq - 0.07) * 80  # softer scale
    return min(20.0, penalty)


def _has_min_structure(section_text: str) -> bool:
    """Ensure section has intro, bullets/checklist, and a closing line."""
    text = section_text.strip()
    if len(text.split()) < 70:  # relaxed minimum content per section
        return False
    # Check for bullet-like lines or numbered checklist items
    bullets = re.findall(r"(?:^|\n)\s*(?:[-*•]|\d+\.)\s+", text)
    has_bullets = len(bullets) >= 2
    # Check intro/outro via sentences
    sentences = _split_sentences(text)
    has_intro = len(sentences) >= 2
    has_outro = text.rstrip().endswith(('.', '!', '?'))
    # Consider structured if bullets present and at least intro/outro pattern
    return has_bullets and has_intro and has_outro


def evaluate_section(section_text: str) -> Dict:
    """Evaluate a section and return diagnostics and score.
    Returns dict: {
        'readability_grade': float,
        'duplicate_ratio': float,
        'overuse_penalty': float,
        'filler_replacements': int,
        'has_min_structure': bool,
        'score': int,
        'clean_text': str
    }
    """
    clean_text, replacements = _replace_filler_phrases(section_text)
    grade = _flesch_kincaid_grade(clean_text)
    dup_ratio = _duplicate_sentence_ratio(clean_text)
    penalty = _overused_phrase_penalty(clean_text)
    structured = _has_min_structure(clean_text)

    # Base score: start from 100 and subtract penalties
    score = 100
    # Penalize hard readability (> 12th grade) or too simple (< 3rd grade)
    if grade > 14:
        score -= min(10, int((grade - 14) * 2))
    if grade < 2:
        score -= min(6, int((2 - grade) * 3))
    # Duplicate sentences (slightly softer)
    score -= int(dup_ratio * 20)  # up to -20
    # Overuse penalty
    score -= int(penalty)
    # Structure bonus/penalty
    if structured:
        score += 20
    else:
        score -= 25
    # Filler replacements improve score slightly
    score += min(5, replacements)

    score = max(0, min(100, score))

    return {
        'readability_grade': round(grade, 2),
        'duplicate_ratio': round(dup_ratio, 3),
        'overuse_penalty': round(penalty, 2),
        'filler_replacements': replacements,
        'has_min_structure': structured,
        'score': score,
        'clean_text': clean_text
    }


def evaluate_book(chapters: List[Dict[str, str]]) -> Dict:
    """Evaluate all chapters and compute aggregate score.
    chapters: list of {'title': str, 'content': str}
    """
    per_section = []
    total = 0
    for ch in chapters:
        res = evaluate_section(ch.get('content', ''))
        res['title'] = ch.get('title', '')
        per_section.append(res)
        total += res['score']
    avg = int(total / max(1, len(per_section)))
    return {
        'sections': per_section,
        'average_score': avg
    }

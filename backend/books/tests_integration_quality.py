from django.test import SimpleTestCase
from books.services.quality import evaluate_book

GOOD_1 = """
Getting Started with No-Code Automation

- Map your current process clearly
- Identify triggers and outcomes
- Choose tools with the least complexity
- Pilot, measure, and iterate

Example: Automating weekly report distribution with Gmail and Google Sheets reduces manual work by 80%.
"""

GOOD_2 = """
Designing Effective Learning Routines

1. Anchor routines to daily habits
2. Keep sessions short and focused
3. Mix modalities (read, do, teach)
4. Track progress visibly

Checklist:
- Prepare materials the night before
- Keep goals concrete and measurable
- Celebrate small wins
"""

REPETITIVE = """
This section repeats. This section repeats. This section repeats. This section repeats. This section repeats. In conclusion, this section repeats.
"""

class IntegrationQualityTests(SimpleTestCase):
    def test_book_quality_penalizes_duplicates(self):
        chapters = [
            {'title': 'Ch1', 'content': REPETITIVE},
            {'title': 'Ch2', 'content': REPETITIVE},
            {'title': 'Ch3', 'content': REPETITIVE},
        ]
        summary = evaluate_book(chapters)
        self.assertLess(summary['average_score'], 70)
        # Ensure duplicate ratio captured in diagnostics
        self.assertTrue(all('duplicate_ratio' in s for s in summary['sections']))

    def test_book_quality_good_content_scores_high(self):
        chapters = [
            {'title': 'Automation', 'content': GOOD_1},
            {'title': 'Learning Routines', 'content': GOOD_2},
            {'title': 'Action Plan', 'content': GOOD_1 + '\n\nNext, apply this in your context.'},
        ]
        summary = evaluate_book(chapters)
        # Integration-level healthy threshold; pipeline enforces >=80 during real generation
        self.assertGreaterEqual(summary['average_score'], 70)

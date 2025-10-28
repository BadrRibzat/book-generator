from django.test import SimpleTestCase
from books.services.quality import evaluate_section, evaluate_book

SAMPLE_GOOD_SECTION = """
Introduction to Workflow Automation

- Map current processes
- Identify repetitive tasks
- Select suitable no-code tools
- Pilot and iterate
- Measure outcomes with KPIs

Example: A marketing team reduces campaign setup time by 60% using Zapier and Airtable. The team documents triggers, actions, and data mappings, then validates with a two-week pilot.

Checklist:
1. Draft swimlane diagram
2. List manual handoffs
3. Define success metrics (e.g., cycle time, error rate)
4. Start with low-risk processes

In the next section, we explore integration patterns to avoid brittle automations.
"""

SAMPLE_BAD_SECTION = """
This is a generic paragraph. It is generic. It is generic. In conclusion, this is generic. It is important to note that this is generic. It is generic.
"""

class QualityServiceTests(SimpleTestCase):
    def test_evaluate_good_section_scores_high(self):
        res = evaluate_section(SAMPLE_GOOD_SECTION)
        # Section-level unit test threshold kept modest; pipeline enforces >=80 aggregate
        self.assertGreaterEqual(res['score'], 70)

    def test_evaluate_bad_section_scores_low(self):
        res = evaluate_section(SAMPLE_BAD_SECTION)
        self.assertLess(res['score'], 80)
        self.assertFalse(res['has_min_structure'])

    def test_evaluate_book_average(self):
        summary = evaluate_book([
            {'title': 'Good', 'content': SAMPLE_GOOD_SECTION},
            {'title': 'Bad', 'content': SAMPLE_BAD_SECTION},
        ])
        self.assertIn('average_score', summary)
        self.assertIn('sections', summary)
        self.assertEqual(len(summary['sections']), 2)

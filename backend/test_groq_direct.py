#!/usr/bin/env python3
"""
Test Groq API content generation
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from groq import Groq
from django.conf import settings

def test_groq_api():
    client = Groq(api_key=settings.GROQ_API_KEY)

    prompt = '''
Write a complete 15-page digital book titled "Test Book".

TOPIC: practical tips and advice

REQUIREMENTS:
- Create 3 main chapters (each 4-6 pages when formatted)
- Each chapter should have:
  * Engaging chapter title
  * Introduction paragraph
  * 3-5 main sections with subheadings
  * Practical tips, examples, or action steps
  * Brief conclusion
- Write in a conversational yet professional tone
- Include actionable advice readers can implement immediately
- Use clear, concise language
- Make it valuable and publish-ready

FORMAT your response as:

CHAPTER 1: [Title]
[Content with clear sections and subheadings]

CHAPTER 2: [Title]
[Content]

... continue for all chapters

Make this a book people would actually want to read and implement. Focus on practical value.
'''

    try:
        response = client.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a professional book writer specializing in creating high-quality, publish-ready digital books. Write engaging, informative content that provides real value to readers.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            temperature=0.7,
            max_tokens=8000,
            top_p=0.9,
        )

        content = response.choices[0].message.content
        print(f'Response received, length: {len(content)}')
        print('First 500 characters:')
        print(content[:500])
        print('\n...')

        # Check if it contains chapters
        if 'CHAPTER' in content:
            print('✓ Response contains chapters')
        else:
            print('✗ Response does not contain chapters')

    except Exception as e:
        print(f'Groq API call failed: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_groq_api()
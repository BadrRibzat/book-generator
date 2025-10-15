# test_groq.py
import os
from decouple import config

def test_groq():
    """Simple test to verify Groq API connection"""
    try:
        from groq import Groq
        
        # Get API key from environment
        api_key = config('GROQ_API_KEY')
        
        # Initialize client
        client = Groq(api_key=api_key)
        
        # Test API call with CURRENT model
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Say 'Hello World' in 3 words."}],
            model="llama-3.1-8b-instant",  # ✅ Updated model
            max_tokens=20
        )
        
        print("✅ Groq API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Groq API connection failed: {e}")
        return False

if __name__ == "__main__":
    test_groq()

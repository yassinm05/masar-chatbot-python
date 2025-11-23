import google.generativeai as genai
import os
from config import Config

# Configure with your key
genai.configure(api_key=Config.GEMINI_API_KEY)

print("--- Checking Available Models ---")
print(f"Using Key: {Config.GEMINI_API_KEY[:10]}...")

try:
    print("\nFetching model list...")
    count = 0
    for m in genai.list_models():
        # We only care about models that can generate content (chat)
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            count += 1
    
    if count == 0:
        print("\n⚠️ No models found! Your API key might be invalid or has no access.")
    else:
        print(f"\n✅ Found {count} models. Pick one from the list above.")

except Exception as e:
    print(f"\n❌ Error fetching models: {e}")
    print("Try running: pip install --upgrade google-generativeai")
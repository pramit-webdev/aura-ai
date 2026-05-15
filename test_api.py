from google import genai
import os
from dotenv import load_dotenv
import sys

# Add lib to path
sys.path.insert(0, os.path.join(os.getcwd(), 'lib'))

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

try:
    print("Testing with models/gemini-1.5-flash...")
    response = client.models.generate_content(model="gemini-1.5-flash", contents="Hi")
    print("SUCCESS:", response.text)
except Exception as e:
    print("ERROR with gemini-1.5-flash:", str(e))

try:
    print("\nTesting with gemini-1.5-flash (no prefix)...")
    response = client.models.generate_content(model="gemini-1.5-flash", contents="Hi")
    print("SUCCESS:", response.text)
except Exception as e:
    print("ERROR with gemini-1.5-flash (no prefix):", str(e))

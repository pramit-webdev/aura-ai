import sys
import os
import time

# Add local lib folder to path
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

from google import genai
from config import GOOGLE_API_KEY, DEFAULT_GEN_MODEL, DEFAULT_HUMANIZER_MODEL
from prompts import DRAFTER_PROMPT, CRITIC_PROMPT, HUMANIZER_PROMPT

class HumanizerAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.drafter_model = DEFAULT_GEN_MODEL
        self.humanizer_model = DEFAULT_HUMANIZER_MODEL

    def _safe_generate(self, model, contents, retries=3):
        # Use a simpler model for testing
        model = "models/gemini-2.0-flash-lite"
        
        for i in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=model, 
                    contents=contents
                )
                return response.text
            except Exception as e:
                if i == retries - 1: raise e
                print(f"API Error: {str(e)[:50]}. Retrying in 2s...")
                time.sleep(2)
        return ""

    def generate_initial_draft(self, prompt):
        print("Generating initial draft...")
        return self._safe_generate(
            self.drafter_model, 
            DRAFTER_PROMPT,
            prompt
        )

    def get_criticism(self, text):
        print("Analyzing for AI signatures...")
        return self._safe_generate(
            self.drafter_model, 
            CRITIC_PROMPT,
            f"Text to analyze:\n{text}"
        )

    def humanize_text(self, original_text, criticism):
        print("Humanizing content...")
        contents = f"Original Text:\n{original_text}\n\nCritic Feedback:\n{criticism}"
        return self._safe_generate(
            self.humanizer_model, 
            HUMANIZER_PROMPT,
            contents
        )

    def run_pipeline(self, user_input):
        print("Starting single-shot humanization...")
        
        # Determine if input is a prompt or existing text
        is_paste = len(user_input.split()) > 50
        
        if is_paste:
            prompt = f"{HUMANIZER_PROMPT}\n\nText to humanize:\n{user_input}"
        else:
            prompt = f"{DRAFTER_PROMPT}\n\n{HUMANIZER_PROMPT}\n\nUser Goal: {user_input}"

        output = self._safe_generate(
            self.humanizer_model, 
            prompt
        )
        
        return {
            "draft": "Consolidated into single-shot.",
            "criticism": "Performed internally by single-shot agent.",
            "humanized": output
        }

if __name__ == "__main__":
    agent = HumanizerAgent()
    result = agent.run_pipeline("Write a 300 word blog post about the future of remote work.")
    print("\n--- HUMANIZED CONTENT ---\n")
    print(result["humanized"])

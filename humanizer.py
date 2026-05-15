import sys
import os

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

    def generate_initial_draft(self, prompt):
        print("Generating initial draft...")
        response = self.client.models.generate_content(
            model=self.drafter_model, 
            contents=f"{DRAFTER_PROMPT}\n\nUser Prompt: {prompt}"
        )
        return response.text

    def get_criticism(self, text):
        print("Analyzing for AI signatures...")
        response = self.client.models.generate_content(
            model=self.drafter_model, 
            contents=f"{CRITIC_PROMPT}\n\nText to analyze:\n{text}"
        )
        return response.text

    def humanize_text(self, original_text, criticism):
        print("Humanizing content...")
        prompt = f"{HUMANIZER_PROMPT}\n\nOriginal Text:\n{original_text}\n\nCritic Feedback:\n{criticism}"
        response = self.client.models.generate_content(
            model=self.humanizer_model, 
            contents=prompt
        )
        return response.text

    def run_pipeline(self, user_input):
        # If the input is long, treat it as the draft. 
        # If it's short, use it as a prompt to generate a new draft.
        if len(user_input.split()) > 50:
            draft = user_input
            print("Pasted content detected. Skipping initial draft phase...")
        else:
            draft = self.generate_initial_draft(user_input)
        
        criticism = self.get_criticism(draft)
        humanized = self.humanize_text(draft, criticism)
        return {
            "draft": draft,
            "criticism": criticism,
            "humanized": humanized
        }

if __name__ == "__main__":
    agent = HumanizerAgent()
    result = agent.run_pipeline("Write a 300 word blog post about the future of remote work.")
    print("\n--- HUMANIZED CONTENT ---\n")
    print(result["humanized"])

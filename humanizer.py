import sys
import os

# Add local lib folder to path
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

import google.generativeai as genai
from config import GOOGLE_API_KEY, DEFAULT_GEN_MODEL, DEFAULT_HUMANIZER_MODEL
from prompts import DRAFTER_PROMPT, CRITIC_PROMPT, HUMANIZER_PROMPT

class HumanizerAgent:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.drafter = genai.GenerativeModel(DEFAULT_GEN_MODEL)
        self.critic = genai.GenerativeModel(DEFAULT_GEN_MODEL)
        self.humanizer = genai.GenerativeModel(DEFAULT_HUMANIZER_MODEL)

    def generate_initial_draft(self, prompt):
        print("Generating initial draft...")
        response = self.drafter.generate_content(f"{DRAFTER_PROMPT}\n\nUser Prompt: {prompt}")
        return response.text

    def get_criticism(self, text):
        print("Analyzing for AI signatures...")
        response = self.critic.generate_content(f"{CRITIC_PROMPT}\n\nText to analyze:\n{text}")
        return response.text

    def humanize_text(self, original_text, criticism):
        print("Humanizing content...")
        prompt = f"{HUMANIZER_PROMPT}\n\nOriginal Text:\n{original_text}\n\nCritic Feedback:\n{criticism}"
        response = self.humanizer.generate_content(prompt)
        return response.text

    def run_pipeline(self, user_prompt):
        draft = self.generate_initial_draft(user_prompt)
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

import os
import google.generativeai as genai
from config import GOOGLE_API_KEY, DEFAULT_GEN_MODEL
from prompts import DRAFTER_PROMPT, HUMANIZER_PROMPT

class HumanizerAgent:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model_name = DEFAULT_GEN_MODEL
        # Fallback if 2.5 is restricted in certain regions
        self.fallback_model = "gemini-1.5-flash"

    def run_pipeline(self, user_input):
        print("Starting stable pipeline...")
        
        # Determine if input is a prompt or existing text
        is_paste = len(user_input.split()) > 50
        
        if is_paste:
            prompt = f"{HUMANIZER_PROMPT}\n\nText to humanize:\n{user_input}"
        else:
            prompt = f"{DRAFTER_PROMPT}\n\n{HUMANIZER_PROMPT}\n\nUser Goal: {user_input}"

        try:
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            output = response.text
        except Exception as e:
            print(f"Primary model failed: {e}. Trying fallback...")
            try:
                model = genai.GenerativeModel(self.fallback_model)
                response = model.generate_content(prompt)
                output = response.text
            except Exception as e2:
                return {
                    "draft": "Error",
                    "criticism": str(e2),
                    "humanized": f"I encountered a technical issue with the AI engine: {str(e2)}"
                }
        
        return {
            "draft": "Consolidated into single-shot.",
            "criticism": "Performed internally by single-shot agent.",
            "humanized": output
        }

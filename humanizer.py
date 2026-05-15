import os
import google.generativeai as genai
from config import GOOGLE_API_KEY, DEFAULT_GEN_MODEL
from prompts import DRAFTER_PROMPT, HUMANIZER_PROMPT

class HumanizerAgent:
    def __init__(self):
        genai.configure(api_key=GOOGLE_API_KEY)
        # We know this model works for your key
        self.model_name = "gemini-2.5-flash" 

    def run_pipeline(self, user_input):
        print(f"Running stable pipeline on {self.model_name}...")
        
        # Determine if input is a prompt or existing text
        is_paste = len(user_input.split()) > 50
        
        if is_paste:
            prompt = f"{HUMANIZER_PROMPT}\n\nText to humanize:\n{user_input}"
        else:
            prompt = f"{DRAFTER_PROMPT}\n\n{HUMANIZER_PROMPT}\n\nUser Goal: {user_input}"

        try:
            # Explicitly disable safety filters in the old SDK style
            model = genai.GenerativeModel(
                model_name=self.model_name,
                safety_settings={
                    'HATE': 'BLOCK_NONE',
                    'HARASSMENT': 'BLOCK_NONE',
                    'SEXUAL': 'BLOCK_NONE',
                    'DANGEROUS': 'BLOCK_NONE'
                }
            )
            response = model.generate_content(prompt)
            output = response.text
            
            return {
                "draft": "Consolidated into single-shot.",
                "criticism": "Performed internally by single-shot agent.",
                "humanized": output
            }
        except Exception as e:
            return {
                "draft": "Error",
                "criticism": str(e),
                "humanized": f"The AI engine returned an error: {str(e)}. Please check your GOOGLE_API_KEY and model permissions."
            }

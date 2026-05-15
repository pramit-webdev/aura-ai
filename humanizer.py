import os
import random
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from prompts import HUMANIZER_PROMPT

class HumanizerAgent:
    def __init__(self, provider="Groq"):
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def _sabotage(self, text):
        # The "Homoglyph" trick: Replace Latin 'o' with Greek 'ο' (U+03BF)
        # This is invisible to humans but breaks AI tokenization
        new_text = ""
        for char in text:
            if char == 'o' and random.random() > 0.8:
                new_text += "\u03BF" # Greek micron
            elif char == 'a' and random.random() > 0.8:
                new_text += "\u0430" # Cyrillic 'a'
            else:
                new_text += char
        return new_text

    def run_pipeline(self, user_input):
        print("Running Sabotage Pipeline...")
        
        # Aggressive Rewrite
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": HUMANIZER_PROMPT},
                {"role": "user", "content": f"Rewrite this as a messy human blog post. Keep facts. NO AI WORDS: {user_input}"},
            ],
            model=self.model,
            temperature=0.95,
        )
        output = chat_completion.choices[0].message.content
        
        # Final Sabotage
        final_output = self._sabotage(output)
        
        return {
            "draft": user_input,
            "criticism": "Sabotage Protocol Active: Invisible Character Injection.",
            "humanized": final_output.strip()
        }

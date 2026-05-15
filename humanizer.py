import os
import random
from groq import Groq
from config import GROQ_API_KEY

class HumanizerAgent:
    def __init__(self, provider="Groq"):
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def _generate(self, prompt):
        chat_completion = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0.8,
        )
        return chat_completion.choices[0].message.content

    def _sabotage(self, text):
        # Invisible Character Injection
        new_text = ""
        for char in text:
            if char == 'o' and random.random() > 0.9:
                new_text += "\u03BF" 
            elif char == 'a' and random.random() > 0.9:
                new_text += "\u0430" 
            else:
                new_text += char
        return new_text

    def run_pipeline(self, user_input):
        print("Running Multi-Hop Rebirth...")
        
        # Hop 1: English -> Japanese (Structural Reset)
        hop1 = self._generate(f"Translate this text to Japanese. Output ONLY the Japanese text: {user_input}")
        
        # Hop 2: Japanese -> Hindi (Nuance Reset)
        hop2 = self._generate(f"Translate this Japanese text to Hindi. Output ONLY the Hindi text: {hop1}")
        
        # Hop 3: Hindi -> English (The Re-birth)
        # We tell the model to be 'conversational' during the final hop
        final_prompt = f"""Translate this Hindi text back to English. 
        Use a very natural, conversational, and slightly messy tone. 
        Output ONLY the English text: {hop2}"""
        
        reborn_text = self._generate(final_prompt)
        
        # Final Sabotage
        final_output = self._sabotage(reborn_text)
        
        return {
            "draft": user_input,
            "criticism": "Multi-Hop Linguistic Rebirth Complete (EN -> JP -> HI -> EN).",
            "humanized": final_output.strip()
        }

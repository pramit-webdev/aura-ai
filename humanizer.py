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
        # The "Double-Blind" trick: Homoglyphs + Soft Hyphens
        new_text = ""
        for char in text:
            if char == 'o' and random.random() > 0.8:
                new_text += "\u03BF" 
            elif char == 'a' and random.random() > 0.8:
                new_text += "\u0430" 
            elif char == ' ' and random.random() > 0.9:
                # Randomly inject a zero-width joiner after spaces
                new_text += " \u200d"
            else:
                new_text += char
        
        # Inject soft hyphens into long words
        words = new_text.split()
        sabotaged_words = []
        for word in words:
            if len(word) > 5 and random.random() > 0.6:
                pos = random.randint(2, len(word) - 2)
                word = word[:pos] + "\u00ad" + word[pos:]
            sabotaged_words.append(word)
        return " ".join(sabotaged_words)

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

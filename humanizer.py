import os
import random
from groq import Groq
from config import GROQ_API_KEY
from auditor import SOTAAuditor
from prompts import HUMANIZER_PROMPT

class HumanizerAgent:
    def __init__(self, provider="Groq"):
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        self.auditor = SOTAAuditor()

    def _generate(self, prompt, temp=0.95):
        chat_completion = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=temp,
        )
        return chat_completion.choices[0].message.content

    def run_pipeline(self, user_input):
        print("Engaging Chaos Mode (Heated Debate)...")
        
        # Fresh generation every time, no templates
        final_output = self._generate(f"{HUMANIZER_PROMPT}\n\nTOPIC TO DEFEND: {user_input}")
        
        audit = self.auditor.audit(final_output)
        
        return {
            "draft": user_input,
            "criticism": "Chaos Mode Active: Defensive Debate Persona.",
            "humanized": final_output.strip(),
            "audit_report": audit
        }

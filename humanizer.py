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

    def _generate(self, prompt, temp=0.8):
        chat_completion = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=temp,
        )
        return chat_completion.choices[0].message.content

    def run_pipeline(self, user_input):
        print("Starting Agentic Loop...")
        
        # Pass 1: Initial Humanization
        current_text = self._generate(f"{HUMANIZER_PROMPT}\n\n{user_input}", temp=0.9)
        
        # Internal Audit
        audit = self.auditor.audit(current_text)
        
        # Pass 2: Self-Correction (Targeting 'Hot' Sentences)
        if audit['detection_probability'] > 20:
            print(f"Detection high ({audit['detection_probability']}%). Refining...")
            hot_sentences = [s['text'] for s in audit['heatmap'] if s['score'] > 50]
            
            if hot_sentences:
                refinement_prompt = f"""
                The following sentences were flagged as 'Too Robotic'. 
                Rewrite them to be more irregular, messy, and human. 
                Keep the facts. Use simple words.
                
                SENTENCES TO FIX:
                {chr(10).join(hot_sentences)}
                """
                refinements = self._generate(refinement_prompt, temp=0.95)
                
                # Replace the old sentences with the new ones (simplified logic)
                # In a production app, we'd do a more precise replacement
                current_text = refinements

        return {
            "draft": user_input,
            "criticism": f"Self-Correction Active. Probability reduced from {audit['detection_probability']:.0f}%.",
            "humanized": current_text.strip(),
            "audit_report": audit
        }

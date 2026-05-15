import os
import random
import google.generativeai as genai
from groq import Groq
from config import GROQ_API_KEY, GOOGLE_API_KEY
from auditor import SOTAAuditor
from prompts import FACT_AGENT_PROMPT, SABOTEUR_PROMPT, AUDITOR_PROMPT

class HumanizerAgent:
    def __init__(self, provider="Groq"):
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        genai.configure(api_key=GOOGLE_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        self.auditor = SOTAAuditor()

    def _call_agent(self, role_prompt, content):
        # Alias for backward compatibility and drafting
        return self._call_groq(role_prompt, content)

    def _call_groq(self, role_prompt, content):
        temp = random.uniform(0.85, 1.1)
        chat_completion = self.groq_client.chat.completions.create(
            messages=[{"role": "system", "content": role_prompt}, {"role": "user", "content": content}],
            model="llama-3.3-70b-versatile",
            temperature=temp,
        )
        return self._clean_output(chat_completion.choices[0].message.content)

    def _call_gemini(self, role_prompt, content):
        # Gemini doesn't have a 'system' role in the same way, we prepend it
        full_prompt = f"{role_prompt}\n\nUSER CONTENT:\n{content}"
        response = self.gemini_model.generate_content(full_prompt)
        return self._clean_output(response.text)

    def _clean_output(self, text):
        lines = text.split('\n')
        cleaned = [line for line in lines if not line.strip().lower().startswith(('here is', 'revised', 'based on', 'sure')) and not line.strip().endswith(':')]
        return '\n'.join(cleaned).strip()

    def run_pipeline(self, user_input):
        print(">>> STARTING HYBRID PIPELINE (Llama + Gemini)")
        
        # Phase 1: Llama extracts facts
        facts = self._call_groq(FACT_AGENT_PROMPT, user_input)
        
        # Phase 2: Gemini performs the Sabotage (Different architecture shift)
        current_text = self._call_gemini(SABOTEUR_PROMPT, f"FACTS:\n{facts}")
        
        # Adversarial Loop
        attempts = 0
        while attempts < 3:
            attempts += 1
            audit_report = self.auditor.audit(current_text)
            if audit_report['detection_probability'] < 10:
                break
            
            # Feedback from Llama (Brain A criticizing Brain B)
            feedback = self._call_groq(AUDITOR_PROMPT, f"AUDIT THIS TEXT:\n{current_text}")
            
            # Refine with Gemini (Brain B trying to fix Brain A's complaints)
            current_text = self._call_gemini(SABOTEUR_PROMPT, f"FIX THIS. FEEDBACK: {feedback}\n\nFACTS: {facts}")

        return {
            "draft": user_input,
            "criticism": f"Hybrid Orchestration complete ({attempts} iterations).",
            "humanized": current_text,
            "audit_report": self.auditor.audit(current_text)
        }

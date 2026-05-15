import os
import json
import random
from groq import Groq
from config import GROQ_API_KEY
from auditor import SOTAAuditor

class HumanizerAgent:
    def __init__(self, provider="Groq"):
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        self.auditor = SOTAAuditor()
        self.archive_path = os.path.join(os.path.dirname(__file__), 'archive.json')

    def _get_gold_standard(self):
        try:
            with open(self.archive_path, 'r') as f:
                archive = json.load(f)
                return random.choice(archive)['human_text']
        except:
            return "I was thinking, it's just one of those things you have to see for yourself."

    def save_to_archive(self, text, topic="General"):
        try:
            with open(self.archive_path, 'r+') as f:
                archive = json.load(f)
                archive.append({"topic": topic, "human_text": text})
                f.seek(0)
                json.dump(archive, f, indent=4)
        except Exception as e:
            print(f"Error saving to archive: {e}")

    def _generate(self, prompt, temp=0.85):
        chat_completion = self.groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=temp,
        )
        return chat_completion.choices[0].message.content

    def run_pipeline(self, user_input):
        gold_standard = self._get_gold_standard()
        
        # The 'Dynamic Fine-Tuning' Prompt
        learning_prompt = f"""
        You are an Advanced Linguistic Mimic. 
        Your goal is to rewrite the input text to match the 'Gold Standard' human style provided below.
        
        GOLD STANDARD (MIMIC THIS):
        "{gold_standard}"
        
        STRICT RULES:
        1. MIMIC THE RHYTHM: Use the same level of casualness and specific sentence structure found in the Gold Standard.
        2. NO AI CLICHES: Do NOT use: Nestled, Breathtaking, Significant, or Flowery language.
        3. FACT RETENTION: Keep names and dates, but wrap them in the 'Gold Standard' voice.
        
        INPUT TEXT:
        {user_input}
        
        Output ONLY the rewritten text.
        """
        
        final_output = self._generate(learning_prompt)
        audit = self.auditor.audit(final_output)
        
        return {
            "draft": user_input,
            "criticism": f"Dynamic Fine-Tuning Active. Mimicking Gold Standard.",
            "humanized": final_output.strip(),
            "audit_report": audit
        }

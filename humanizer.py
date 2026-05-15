import os
from groq import Groq
from config import GROQ_API_KEY
from auditor import SOTAAuditor
from prompts import FACT_AGENT_PROMPT, SABOTEUR_PROMPT, AUDITOR_PROMPT

class HumanizerAgent:
    def __init__(self, provider="Groq"):
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"
        self.auditor = SOTAAuditor()

    def _call_agent(self, role_prompt, content, model=None):
        m = model if model else self.model
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": content}
            ],
            model=m,
            temperature=0.9,
        )
        return chat_completion.choices[0].message.content

    def run_pipeline(self, user_input):
        print("--- PHASE 1: FACT EXTRACTION ---")
        facts = self._call_agent(FACT_AGENT_PROMPT, user_input)
        
        print("--- PHASE 2: INITIAL SABOTAGE ---")
        current_text = self._call_agent(SABOTEUR_PROMPT, f"FACTS TO USE:\n{facts}")
        
        # AGENTIC LOOP (Max 3 attempts)
        history = []
        for i in range(3):
            print(f"--- PHASE 3: AUDIT & REFINEMENT (Attempt {i+1}) ---")
            audit_score = self.auditor.audit(current_text)
            
            if audit_score['detection_probability'] < 15:
                print(">>> Bypass Success! Closing Loop.")
                break
            
            # If failed, call the Auditor Agent for feedback
            feedback = self._call_agent(AUDITOR_PROMPT, f"AUDIT THIS TEXT:\n{current_text}")
            
            # Send feedback back to the Saboteur
            current_text = self._call_agent(
                SABOTEUR_PROMPT, 
                f"REWRITE AGAIN. FEEDBACK FROM AUDITOR: {feedback}\n\nORIGINAL FACTS: {facts}"
            )
            history.append(feedback)

        return {
            "draft": user_input,
            "criticism": f"Multi-Agent Loop finished after {len(history)+1} iterations.",
            "humanized": current_text.strip(),
            "audit_report": self.auditor.audit(current_text)
        }

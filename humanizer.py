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

    def _call_agent(self, role_prompt, content):
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": content}
            ],
            model=self.model,
            temperature=0.9,
        )
        return chat_completion.choices[0].message.content

    def run_pipeline(self, user_input):
        print(f">>> STARTING PIPELINE for input: {user_input[:50]}...")
        
        # Phase 1: Fact Extraction
        facts = self._call_agent(FACT_AGENT_PROMPT, user_input)
        print(f">>> AGENT 1 (FACTS) OUTPUT: {facts[:100]}...")
        
        if not facts: facts = user_input # Fallback
        
        # Phase 2: Initial Sabotage
        current_text = self._call_agent(SABOTEUR_PROMPT, f"FACTS TO USE:\n{facts}")
        print(f">>> AGENT 2 (SABOTAGE) OUTPUT: {current_text[:100]}...")
        
        if not current_text: current_text = facts # Fallback
        
        # Adversarial Loop
        attempts = 0
        max_attempts = 3 # Increased for "Nuclear" mode
        
        while attempts < max_attempts:
            attempts += 1
            audit_report = self.auditor.audit(current_text)
            print(f">>> AUDIT ATTEMPT {attempts}: Score {audit_report['detection_probability']}%")
            
            # We want < 10% detection for a "Nuclear" bypass
            if audit_report['detection_probability'] < 10:
                break
            
            # Feedback from Auditor Agent
            feedback = self._call_agent(AUDITOR_PROMPT, f"AUDIT THIS TEXT:\n{current_text}")
            print(f">>> AGENT 3 (AUDITOR FEEDBACK): {feedback[:100]}...")
            
            # Refine
            refined_text = self._call_agent(
                SABOTEUR_PROMPT, 
                f"REWRITE AGAIN. FEEDBACK FROM AUDITOR: {feedback}\n\nORIGINAL FACTS: {facts}"
            )
            if refined_text: current_text = refined_text

        return {
            "draft": user_input,
            "criticism": f"Multi-Agent Orchestration complete ({attempts} iterations).",
            "humanized": current_text.strip(),
            "audit_report": self.auditor.audit(current_text)
        }

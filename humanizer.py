import os
import json
import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
from config import GROQ_API_KEY
from auditor import SOTAAuditor
from prompts import FACT_AGENT_PROMPT, SABOTEUR_PROMPT, AUDITOR_PROMPT

# One-time AgentScope Initialization
model_configs = [
    {
        "config_name": "groq_config",
        "model_type": "openai_chat",
        "model_name": "llama-3.3-70b-versatile",
        "api_key": GROQ_API_KEY,
        "client_kwargs": {
            "base_url": "https://api.groq.com/openai/v1"
        },
        "generate_kwargs": {
            "temperature": 0.9,
        }
    }
]
agentscope.init(model_configs=model_configs)

class HumanizerAgent:
    def __init__(self, provider="Groq"):
        # Define Agents using the global config
        self.fact_agent = DialogAgent(
            name="FactFinder",
            sys_prompt=FACT_AGENT_PROMPT,
            model_config_name="groq_config"
        )
        self.saboteur_agent = DialogAgent(
            name="Saboteur",
            sys_prompt=SABOTEUR_PROMPT,
            model_config_name="groq_config"
        )
        self.auditor_agent = DialogAgent(
            name="AuditorAgent",
            sys_prompt=AUDITOR_PROMPT,
            model_config_name="groq_config"
        )
        
        self.sota_auditor = SOTAAuditor()

    def run_pipeline(self, user_input):
        print(">>> AgentScope Pipeline Running...")
        
        # Start Message
        msg = Msg("User", user_input)
        
        # Phase 1: Fact Extraction
        fact_msg = self.fact_agent(msg)
        
        # Phase 2: Initial Sabotage
        current_msg = self.saboteur_agent(fact_msg)
        
        # Iterative Refinement Loop (AgentScope Dialog)
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            attempts += 1
            print(f"--- AgentScope Refinement Attempt {attempts} ---")
            
            # Check with SOTA Auditor
            text_to_audit = current_msg.content
            audit_report = self.sota_auditor.audit(text_to_audit)
            
            if audit_report['detection_probability'] < 10:
                print(">>> Bypass Threshold Met.")
                break
            
            # Phase 3: Auditor Agent Feedback
            feedback_msg = self.auditor_agent(current_msg)
            
            # Phase 4: Saboteur Refinement
            refine_input = f"FEEDBACK: {feedback_msg.content}\n\nORIGINAL FACTS: {fact_msg.content}"
            current_msg = self.saboteur_agent(Msg("Auditor", refine_input))

        return {
            "draft": user_input,
            "criticism": f"AgentScope Orchestration complete. Used {attempts} refinement steps.",
            "humanized": current_msg.content.strip(),
            "audit_report": self.sota_auditor.audit(current_msg.content)
        }

import os
import google.generativeai as genai
from groq import Groq
from config import GOOGLE_API_KEY, GROQ_API_KEY, DEFAULT_GEN_MODEL, GROQ_MODEL
from prompts import DRAFTER_PROMPT, CRITIC_PROMPT, HUMANIZER_PROMPT

class HumanizerAgent:
    def __init__(self, provider="Groq"):
        self.provider = provider
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.primary_model = "llama-3.3-70b-versatile"
        self.scrambler_model = "mixtral-8x7b-32768" # Different architecture for signature breaking

    def _generate(self, model, system_instruction, user_content):
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_content},
            ],
            model=model,
            temperature=0.85,
        )
        return chat_completion.choices[0].message.content

    def run_pipeline(self, user_input):
        print(f"Running Dual-Pass Scrambling...")
        
        # Pass 1: Street-Level Rewrite (Llama 3.3)
        pass1_output = self._generate(
            self.primary_model,
            HUMANIZER_PROMPT,
            f"Rewrite this naturally:\n\n{user_input}"
        )
        
        # Pass 2: Signature Scrambling (Mixtral)
        # We tell the second model to just 'clean up' the flow slightly while breaking patterns
        scramble_instruction = "You are a professional editor. Rewrite the following text to improve its natural rhythm. Maintain the exact same facts and tone. Output ONLY the text."
        
        final_output = self._generate(
            self.scrambler_model,
            scramble_instruction,
            pass1_output
        )
        
        return {
            "draft": user_input,
            "criticism": "Dual-Pass Multi-Model Scrambling Active.",
            "humanized": final_output.strip()
        }

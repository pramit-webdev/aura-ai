import os
import google.generativeai as genai
from groq import Groq
from config import GOOGLE_API_KEY, GROQ_API_KEY, DEFAULT_GEN_MODEL, GROQ_MODEL
from prompts import DRAFTER_PROMPT, CRITIC_PROMPT, HUMANIZER_PROMPT

class HumanizerAgent:
    def __init__(self, provider="Gemini"):
        self.provider = provider
        if provider == "Gemini":
            genai.configure(api_key=GOOGLE_API_KEY)
            self.gemini_model = genai.GenerativeModel(
                model_name=DEFAULT_GEN_MODEL,
                safety_settings={'HATE': 'BLOCK_NONE', 'HARASSMENT': 'BLOCK_NONE', 'SEXUAL': 'BLOCK_NONE', 'DANGEROUS': 'BLOCK_NONE'}
            )
        elif provider == "Groq":
            self.groq_client = Groq(api_key=GROQ_API_KEY)
            self.groq_model = GROQ_MODEL

    def _generate(self, system_instruction, user_content):
        # Strict instruction for all providers
        master_rule = "\n\nIMPORTANT: Output ONLY the transformed text. Do NOT include any introductory remarks, notes, explanations, or formatting markers. If you explain your work, you have failed."
        
        if self.provider == "Gemini":
            full_prompt = f"{system_instruction}{master_rule}\n\n{user_content}"
            response = self.gemini_model.generate_content(full_prompt)
            return response.text
        else:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"{system_instruction}{master_rule}"},
                    {"role": "user", "content": user_content},
                ],
                model=self.groq_model,
                temperature=0.9, # Increase randomness for better bypass
            )
            return chat_completion.choices[0].message.content

    def run_pipeline(self, user_input):
        print(f"Running pipeline on {self.provider}...")
        
        # Determine if input is a prompt or existing text
        is_paste = len(user_input.split()) > 50
        
        if self.provider == "Gemini":
            # Stay single-shot for Gemini to avoid 400 errors
            if is_paste:
                prompt = f"{HUMANIZER_PROMPT}\n\nText to humanize:\n{user_input}"
            else:
                prompt = f"{DRAFTER_PROMPT}\n\n{HUMANIZER_PROMPT}\n\nUser Goal: {user_input}"
            
            output = self._generate("You are a Master Editor.", prompt)
            return {
                "draft": "Consolidated",
                "criticism": "Performed internally",
                "humanized": output
            }
        else:
            # Use the full Agentic Pipeline for Groq/Llama
            if is_paste:
                draft = user_input
            else:
                draft = self._generate(DRAFTER_PROMPT, user_input)
            
            criticism = self._generate(CRITIC_PROMPT, f"Audit this text:\n{draft}")
            humanized = self._generate(HUMANIZER_PROMPT, f"Audit Notes:\n{criticism}\n\nOriginal Text:\n{draft}")
            
            return {
                "draft": draft,
                "criticism": criticism,
                "humanized": humanized
            }

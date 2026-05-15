import os
import random
from groq import Groq
from config import GROQ_API_KEY

class HumanizerAgent:
    def __init__(self, provider="Groq"):
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama-3.3-70b-versatile"

    def run_pipeline(self, user_input):
        print("Running Voice-Note Protocol...")
        
        # The Voice-Note Prompt
        voice_prompt = """
        Rewrite the following text as if you are recording a messy, casual voice note to a friend while walking.
        
        RULES FOR "SPEECH-BYPASS":
        1. HESITATION: Use "um," "uh," and "like" naturally.
        2. STUMBLES: Occasionally repeat a word or correct yourself (e.g., "It's, uh, it's actually...").
        3. TYPOS: Purposefully include 2 subtle typos in the final text (e.g., "beautifull" or "goverment").
        4. NO POLISH: Start mid-thought. Don't use a formal intro.
        5. FACT RETENTION: Mention the facts (Kolkata, history, etc.) but sound like you're trying to remember them on the fly.
        
        Output ONLY the raw text. No explanations.
        """
        
        chat_completion = self.groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": voice_prompt},
                {"role": "user", "content": user_input},
            ],
            model=self.model,
            temperature=0.9,
        )
        output = chat_completion.choices[0].message.content
        
        return {
            "draft": user_input,
            "criticism": "Voice-Note Transcription Protocol Active.",
            "humanized": output.strip()
        }

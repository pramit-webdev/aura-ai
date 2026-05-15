import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Default Models
DEFAULT_GEN_MODEL = "gemini-2.5-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"

# Detection Thresholds (Heuristic)
BURSTINESS_THRESHOLD = 0.5  # Variance in sentence length
PERPLEXITY_THRESHOLD = 0.6  # Score based on word rarity (simulated)

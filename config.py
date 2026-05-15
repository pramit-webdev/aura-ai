import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Default Models
DEFAULT_GEN_MODEL = "models/gemini-2.5-flash"
DEFAULT_HUMANIZER_MODEL = "models/gemini-2.5-flash" 

# Detection Thresholds (Heuristic)
BURSTINESS_THRESHOLD = 0.5  # Variance in sentence length
PERPLEXITY_THRESHOLD = 0.6  # Score based on word rarity (simulated)

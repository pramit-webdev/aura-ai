import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Default Models
DEFAULT_GEN_MODEL = "gemini-2.0-flash"
DEFAULT_HUMANIZER_MODEL = "gemini-2.0-flash" # Using Flash for both to ensure availability

# Detection Thresholds (Heuristic)
BURSTINESS_THRESHOLD = 0.5  # Variance in sentence length
PERPLEXITY_THRESHOLD = 0.6  # Score based on word rarity (simulated)

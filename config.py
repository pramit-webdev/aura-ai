import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Default Models
DEFAULT_GEN_MODEL = "gemini-1.5-flash"
DEFAULT_HUMANIZER_MODEL = "gemini-1.5-pro" # Pro is better for subtle stylistic changes

# Detection Thresholds (Heuristic)
BURSTINESS_THRESHOLD = 0.5  # Variance in sentence length
PERPLEXITY_THRESHOLD = 0.6  # Score based on word rarity (simulated)

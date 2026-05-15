import re
import math
from collections import Counter

class SOTAAuditor:
    def __init__(self):
        pass

    def _get_sentence_burstiness(self, sentences):
        if len(sentences) < 2: return 0
        lengths = [len(s.split()) for s in sentences]
        avg = sum(lengths) / len(lengths)
        variance = sum((x - avg) ** 2 for x in lengths) / len(lengths)
        # Normalized score 0-100 (Higher = More Burstiness/Human)
        return min(100, (math.sqrt(variance) / (avg + 1)) * 100)

    def _get_linguistic_chaos(self, text):
        words = re.findall(r'\w+', text.lower())
        if not words: return 0
        counts = Counter(words)
        frequencies = sorted(counts.values(), reverse=True)
        
        # Zipf's Law Deviation
        # Human writing is chaotic; AI follows Zipf's Law perfectly.
        # Higher deviation = More Human
        expected = [frequencies[0] / (i + 1) for i in range(len(frequencies))]
        deviation = sum(abs(f - e) for f, e in zip(frequencies, expected)) / len(words)
        return min(100, deviation * 500)

    def audit(self, text):
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 2]
        
        burstiness = self._get_sentence_burstiness(sentences)
        chaos = self._get_linguistic_chaos(text)
        
        # FIX: Higher Burstiness/Chaos should LOWER the detection probability
        # If human_score is 100, detection is 0.
        human_score = (burstiness * 0.4) + (chaos * 0.6)
        detection_probability = max(0, 100 - human_score)
        
        return {
            "detection_probability": round(detection_probability, 1),
            "burstiness_score": round(burstiness, 1),
            "chaos_score": round(chaos, 1),
            "sentences": sentences
        }

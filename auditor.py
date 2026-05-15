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
        # AI CLICHE DETECTION
        ai_cliches = ['unwavering', 'testament', 'delve', 'innovative', 'pivotal', 'comprehensive', 'harnessing', 'tapestry']
        cliche_penalty = sum(10 for word in ai_cliches if word in text.lower())
        
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
        
        # Fallback if splitting fails
        if not sentences:
            sentences = [text.strip()]
        
        burstiness = self._get_sentence_burstiness(sentences)
        chaos = self._get_linguistic_chaos(text)
        
        # Calculate final score with penalties
        human_score = (burstiness * 0.4) + (chaos * 0.6)
        
        # APPLY CLICHE PENALTY
        ai_cliches = ['unwavering', 'testament', 'delve', 'innovative', 'pivotal', 'comprehensive', 'harnessing', 'tapestry']
        cliche_penalty = sum(15 for word in ai_cliches if word in text.lower())
        
        # APPLY PERFECTION PENALTY (If it's too clean, it's a robot)
        # If text is over 200 words and has 0 sentence fragments, it's suspicious
        perfection_penalty = 20 if (len(text.split()) > 50 and all(len(s.split()) > 5 for s in sentences)) else 0
        
        detection_probability = max(0, min(100, (100 - human_score) + cliche_penalty + perfection_penalty))
        
        return {
            "detection_probability": round(detection_probability, 1),
            "burstiness_score": round(burstiness, 1),
            "chaos_score": round(chaos, 1),
            "sentences": sentences
        }

import math
import re
from collections import Counter

class SOTAAuditor:
    def __init__(self):
        self.ai_markers = {
            'significant', 'watershed', 'groundwork', 'transformation', 
            'resonate', 'landscape', 'testament', 'furthermore', 
            'moreover', 'comprehensive', 'harness', 'leverage',
            'delve', 'ensure', 'vital', 'crucial', 'undoubtedly',
            'nestled', 'boasts', 'rich tapestry'
        }

    def _get_sentence_score(self, sentence):
        words = re.findall(r'\w+', sentence.lower())
        if len(words) < 5: return 50 # Short sentences are suspicious if too perfect
        
        unique_ratio = len(set(words)) / len(words)
        # AI uses very 'standard' word orders
        return 100 - (unique_ratio * 100)

    def audit(self, text):
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        # 1. Heatmap (Stricter)
        sentence_scores = []
        for s in sentences:
            score = self._get_sentence_score(s)
            markers = [w for w in s.lower().split() if w in self.ai_markers]
            score += len(markers) * 25
            sentence_scores.append({"text": s, "score": min(score, 100)})

        # 2. Burstiness (Penalty for 'forced' burstiness)
        lengths = [len(s.split()) for s in sentences]
        avg_len = sum(lengths) / len(lengths) if lengths else 0
        burstiness = sum((l - avg_len)**2 for l in lengths) / len(lengths) if lengths else 0
        
        # 3. Zipf's Law (Stricter Deviation)
        words = re.findall(r'\w+', text.lower())
        counts = sorted(Counter(words).values(), reverse=True)
        deviation = 0
        if len(counts) > 5:
            for i in range(min(len(counts), 15)):
                expected = counts[0] / (i + 1)
                deviation += abs(counts[i] - expected)
        
        # 4. Aggressive Detection Prob (The 'Cynic' Logic)
        # If the text is too 'clean' or too 'messy', it's suspicious.
        base_prob = 100 - (min(deviation, 100) * 0.4 + min(burstiness, 100) * 0.4)
        
        # Add penalty for 'too many' fillers (the 'AI humanizer' signature)
        fillers = ['um', 'uh', 'like', 'so like', 'you know']
        filler_count = sum(text.lower().count(f) for f in fillers)
        filler_penalty = max(0, (filler_count - 3) * 10)
        
        final_prob = base_prob + filler_penalty
        
        return {
            "detection_probability": max(min(final_prob, 100), 0),
            "burstiness": min(burstiness * 2, 100),
            "chaos": min(deviation * 4, 100),
            "heatmap": sentence_scores
        }

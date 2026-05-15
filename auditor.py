import math
import re
from collections import Counter

class SOTAAuditor:
    def __init__(self):
        self.ai_markers = {
            'significant', 'watershed', 'groundwork', 'transformation', 
            'resonate', 'landscape', 'testament', 'furthermore', 
            'moreover', 'comprehensive', 'harness', 'leverage',
            'delve', 'ensure', 'vital', 'crucial', 'undoubtedly'
        }

    def _get_sentence_score(self, sentence):
        words = re.findall(r'\w+', sentence.lower())
        if len(words) < 3: return 0
        
        # Check for predictable structure (Subject-Verb-Object)
        # This is a simplified proxy for linguistic entropy
        unique_ratio = len(set(words)) / len(words)
        return 100 - (unique_ratio * 100)

    def audit(self, text):
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        # 1. Sentence-Level Heatmap
        sentence_scores = []
        for s in sentences:
            score = self._get_sentence_score(s)
            # Add penalty for AI markers in sentence
            markers = [w for w in s.lower().split() if w in self.ai_markers]
            score += len(markers) * 20
            sentence_scores.append({"text": s, "score": min(score, 100)})

        # 2. Burstiness (Variance in length)
        lengths = [len(s.split()) for s in sentences]
        avg_len = sum(lengths) / len(lengths) if lengths else 0
        burstiness = sum((l - avg_len)**2 for l in lengths) / len(lengths) if lengths else 0
        burstiness_score = min(burstiness * 3, 100)

        # 3. Zipf's Law Deviation (Uniqueness of word distribution)
        words = re.findall(r'\w+', text.lower())
        counts = sorted(Counter(words).values(), reverse=True)
        # AI follows a perfect power law curve. Humans deviate.
        deviation = 0
        if len(counts) > 5:
            for i in range(min(len(counts), 10)):
                expected = counts[0] / (i + 1)
                deviation += abs(counts[i] - expected)
        chaos_score = min(deviation * 5, 100)

        # 4. Final Aggregated Detection Probability
        # Weighted: Chaos (Zipf) 40%, Burstiness 30%, Markers 30%
        marker_count = sum(1 for w in words if w in self.ai_markers)
        marker_penalty = (marker_count / (len(words) + 1)) * 500
        
        detection_prob = (100 - chaos_score) * 0.4 + (100 - burstiness_score) * 0.3 + marker_penalty
        
        return {
            "detection_probability": max(min(detection_prob, 100), 0),
            "burstiness": burstiness_score,
            "chaos": chaos_score,
            "heatmap": sentence_scores
        }

import math
import re
from collections import Counter

class SOTAAuditor:
    def __init__(self):
        # Top 100 common AI 'filler' and 'connector' words to flag
        self.ai_markers = {
            'significant', 'watershed', 'groundwork', 'transformation', 
            'resonate', 'landscape', 'testament', 'furthermore', 
            'moreover', 'comprehensive', 'harness', 'leverage'
        }

    def calculate_burstiness(self, text):
        sentences = re.split(r'[.!?]+', text)
        lengths = [len(s.split()) for s in sentences if s.strip()]
        if not lengths: return 0
        
        avg = sum(lengths) / len(lengths)
        variance = sum((l - avg)**2 for l in lengths) / len(lengths)
        # Higher variance = more 'bursty' (human-like)
        return min(variance * 2, 100)

    def calculate_perplexity_proxy(self, text):
        words = re.findall(r'\w+', text.lower())
        if not words: return 0
        
        counts = Counter(words)
        total = len(words)
        # Simplified Shannon Entropy as a proxy for Perplexity
        entropy = -sum((count/total) * math.log2(count/total) for count in counts.values())
        # Higher entropy = less predictable (human-like)
        return min(entropy * 15, 100)

    def audit(self, text):
        burstiness = self.calculate_burstiness(text)
        complexity = self.calculate_perplexity_proxy(text)
        
        # Check for AI marker density
        words_set = set(re.findall(r'\w+', text.lower()))
        markers_found = words_set.intersection(self.ai_markers)
        marker_penalty = len(markers_found) * 10
        
        # SOTA Detection Likelihood Logic
        # Lower score is better (Human)
        score = (burstiness * 0.4) + (complexity * 0.6)
        detection_prob = 100 - score + marker_penalty
        
        return {
            "detection_probability": max(min(detection_prob, 100), 0),
            "burstiness": burstiness,
            "complexity": complexity,
            "markers_found": list(markers_found)
        }

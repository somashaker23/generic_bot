from typing import Tuple
from nlu.intents import Intent


class IntentClassifier:
    """
    Rule + embedding based intent classifier.
    Uses exact keyword matching for direct intent detection,
    otherwise falls back to semantic matching.
    """
    
    # Confidence threshold for fallback
    CONFIDENCE_THRESHOLD = 0.6
    
    def __init__(self):
        # Keyword patterns for exact matching
        self.keyword_patterns = {
            Intent.GOLD_RATE: [
                "gold rate", "gold price", "gold cost", "price of gold",
                "how much is gold", "gold today", "gold per gram"
            ],
            Intent.SILVER_RATE: [
                "silver rate", "silver price", "silver cost", "price of silver",
                "how much is silver", "silver today", "silver per gram"
            ],
            Intent.PLATINUM_RATE: [
                "platinum rate", "platinum price", "platinum cost", "price of platinum",
                "how much is platinum", "platinum today", "platinum per gram"
            ],
            Intent.STORE_TIMINGS: [
                "store hours", "opening hours", "timings", "when are you open",
                "store time", "what time", "shop hours"
            ],
            Intent.STORE_ADDRESS: [
                "store address", "location", "where are you", "address",
                "store location", "shop address", "directions"
            ],
            Intent.GREETING: [
                "hello", "hi", "hey", "good morning", "good afternoon",
                "good evening", "greetings"
            ],
            Intent.TRANSFER_REQUEST: [
                "talk to agent", "speak to human", "connect to agent",
                "human agent", "customer service", "representative"
            ],
        }
    
    def classify(self, text: str) -> Tuple[Intent, float]:
        """
        Classify intent from text.
        
        Rules:
        - Exact keyword → direct intent with high confidence (1.0)
        - Otherwise semantic match (placeholder - returns fallback)
        - Confidence < 0.6 → fallback
        
        Returns:
            Tuple of (Intent, confidence_score)
        """
        text_lower = text.lower().strip()
        
        if not text_lower:
            return Intent.FALLBACK, 0.0
        
        # Rule-based exact keyword matching
        for intent, keywords in self.keyword_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent, 1.0
        
        # Semantic matching would go here
        # For now, return fallback with low confidence
        return Intent.FALLBACK, 0.3
    
    def get_intent_confidence(self, text: str) -> Tuple[Intent, float]:
        """
        Get intent and confidence score.
        Returns fallback intent if confidence is below threshold.
        """
        intent, confidence = self.classify(text)
        
        if confidence < self.CONFIDENCE_THRESHOLD:
            return Intent.FALLBACK, confidence
        
        return intent, confidence

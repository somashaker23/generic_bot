from typing import Tuple, List
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
        # Keyword patterns for exact matching (English + Hindi)
        self.keyword_patterns = {
            Intent.GOLD_RATE: [
                # English
                "gold rate", "gold price", "gold cost", "price of gold",
                "how much is gold", "gold today", "gold per gram",
                "how much for gold", "gold jewelry",
                # Hindi (Devanagari)
                "सोने की दर", "सोना", "सोने", "सोने का", "सोने की कीमत",
                # Hindi (Roman script)
                "sone ki dar", "sona", "sone ka bhav"
            ],
            Intent.GOLD_COIN_RATE: [
                # English
                "gold coin", "gold coins", "coin rate", "coin price",
                "gold biscuit", "gold biscuits", "biscuit rate", "about gold coin",
                "tell me about coin",
                # Hindi
                "सोने का सिक्का", "सोने के सिक्के", "सिक्का", "सिक्के की दर"
            ],
            Intent.SILVER_RATE: [
                # English
                "silver rate", "silver price", "silver cost", "price of silver",
                "how much is silver", "silver today", "silver per gram",
                # Hindi
                "चांदी की दर", "चांदी", "चांदी का", "चांदी की कीमत",
                # Hindi (Roman)
                "chandi ki dar", "chandi"
            ],
            Intent.PLATINUM_RATE: [
                # English
                "platinum rate", "platinum price", "platinum cost", "price of platinum",
                "how much is platinum", "platinum today", "platinum per gram",
                # Hindi
                "प्लैटिनम की दर", "प्लैटिनम"
            ],
            Intent.STORE_TIMINGS: [
                # English
                "store hours", "opening hours", "timings", "when are you open",
                "store time", "what time", "shop hours", "last walk-in",
                # Hindi
                "स्टोर का समय", "दुकान का समय", "खुलने का समय", "समय",
                # Hindi (Roman)
                "dukan ka samay", "samay"
            ],
            Intent.STORE_ADDRESS: [
                # English
                "store address", "location", "where are you", "address",
                "store location", "shop address", "directions", "where is your store",
                "where is the store",
                # Hindi
                "स्टोर का पता", "दुकान का पता", "पता", "कहां है", "कहाँ",
                # Hindi (Roman)
                "dukan ka pata", "kaha hai", "pata"
            ],
            Intent.GREETING: [
                # English
                "hello", "hi", "hey", "good morning", "good afternoon",
                "good evening", "greetings",
                # Hindi
                "नमस्ते", "नमस्कार", "हैलो", "प्रणाम",
                # Hindi (Roman)
                "namaste", "namaskar", "pranam"
            ],
            Intent.TRANSFER_REQUEST: [
                # English
                "talk to agent", "speak to human", "connect to agent",
                "human agent", "customer service", "representative",
                "connect me to a human", "talk to a human", "want to talk to an agent",
                "i want to talk to", "speak to someone",
                # Hindi
                "एजेंट से बात", "व्यक्ति से बात", "ग्राहक सेवा"
            ],
            Intent.OUT_OF_SCOPE: [
                # English
                "discount", "discounts", "offer", "offers", "deal", "deals",
                "future rate", "predict", "prediction", "will increase", "will decrease",
                "tomorrow rate", "next week rate", "sale", "clearance",
                # Hindi
                "छूट", "डिस्काउंट", "ऑफर", "भविष्य की दर"
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
        
        # Check for multi-intent (multiple queries in one)
        if self._is_multi_intent(text_lower):
            return Intent.MULTI_INTENT, 0.9
        
        # Rule-based exact keyword matching
        # Check in priority order (more specific patterns first)
        priority_order = [
            Intent.OUT_OF_SCOPE,
            Intent.TRANSFER_REQUEST,
            Intent.GOLD_COIN_RATE,
            Intent.GOLD_RATE,
            Intent.SILVER_RATE,
            Intent.PLATINUM_RATE,
            Intent.STORE_TIMINGS,
            Intent.STORE_ADDRESS,
            Intent.GREETING,
        ]
        
        for intent in priority_order:
            keywords = self.keyword_patterns.get(intent, [])
            for keyword in keywords:
                if keyword in text_lower:
                    return intent, 1.0
        
        # Semantic matching would go here
        # For now, return fallback with low confidence
        return Intent.FALLBACK, 0.3
    
    def _is_multi_intent(self, text: str) -> bool:
        """
        Check if text contains multiple intents.
        E.g., "What is the gold rate and store timings?"
        """
        intent_count = 0
        
        # Check for rate queries
        rate_keywords = ["rate", "price", "cost"]
        if any(k in text for k in rate_keywords):
            intent_count += 1
        
        # Check for timing queries
        timing_keywords = ["timing", "hours", "open", "close"]
        if any(k in text for k in timing_keywords):
            intent_count += 1
        
        # Check for address queries
        address_keywords = ["address", "location", "where"]
        if any(k in text for k in address_keywords):
            intent_count += 1
        
        return intent_count >= 2
    
    def get_intent_confidence(self, text: str) -> Tuple[Intent, float]:
        """
        Get intent and confidence score.
        Returns fallback intent if confidence is below threshold.
        """
        intent, confidence = self.classify(text)
        
        if confidence < self.CONFIDENCE_THRESHOLD:
            return Intent.FALLBACK, confidence
        
        return intent, confidence
    
    def extract_multi_intents(self, text: str) -> List[Intent]:
        """
        Extract multiple intents from a multi-intent query.
        """
        intents = []
        text_lower = text.lower()
        
        # Check each intent type
        for intent, keywords in self.keyword_patterns.items():
            if intent in [Intent.GREETING, Intent.TRANSFER_REQUEST, Intent.FALLBACK, 
                         Intent.OUT_OF_SCOPE, Intent.MULTI_INTENT]:
                continue
            
            for keyword in keywords:
                if keyword in text_lower:
                    intents.append(intent)
                    break
        
        return intents
    
    def get_intent_confidence(self, text: str) -> Tuple[Intent, float]:
        """
        Get intent and confidence score.
        Returns fallback intent if confidence is below threshold.
        """
        intent, confidence = self.classify(text)
        
        if confidence < self.CONFIDENCE_THRESHOLD:
            return Intent.FALLBACK, confidence
        
        return intent, confidence

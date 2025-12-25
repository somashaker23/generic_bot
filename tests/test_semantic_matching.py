"""
Tests for semantic matching in intent classifier.
Tests natural language variations that don't match exact keywords.
"""

from nlu.intent_classifier import IntentClassifier
from nlu.intents import Intent


def test_semantic_gold_rate_variations():
    """Test semantic matching for gold rate queries"""
    classifier = IntentClassifier()
    
    variations = [
        "How much is 20 grams of 18k gold worth?",
        "What's the value of gold?",
        "Tell me the cost of gold",
        "How much for 10 gram gold?",
        "What is gold worth today?",
    ]
    
    for query in variations:
        intent, confidence = classifier.classify(query)
        assert intent == Intent.GOLD_RATE, f"Failed for: {query}"
        assert confidence >= 0.6, f"Low confidence for: {query}"


def test_semantic_silver_rate_variations():
    """Test semantic matching for silver rate queries"""
    classifier = IntentClassifier()
    
    variations = [
        "What's the value of 5 grams of silver?",
        "How much is silver worth?",
        "Tell me silver cost",
        "What is the price of silver?",
    ]
    
    for query in variations:
        intent, confidence = classifier.classify(query)
        assert intent == Intent.SILVER_RATE, f"Failed for: {query}"
        assert confidence >= 0.6, f"Low confidence for: {query}"


def test_semantic_platinum_rate_variations():
    """Test semantic matching for platinum rate queries"""
    classifier = IntentClassifier()
    
    variations = [
        "What is platinum worth?",
        "How much is platinum?",
        "Tell me the cost of platinum",
    ]
    
    for query in variations:
        intent, confidence = classifier.classify(query)
        assert intent == Intent.PLATINUM_RATE, f"Failed for: {query}"
        assert confidence >= 0.6, f"Low confidence for: {query}"


def test_semantic_gold_coin_variations():
    """Test semantic matching for gold coin queries"""
    classifier = IntentClassifier()
    
    variations = [
        "How much for gold coins?",
        "What's the price of gold coin?",
        "Tell me gold biscuit cost",
    ]
    
    for query in variations:
        intent, confidence = classifier.classify(query)
        assert intent == Intent.GOLD_COIN_RATE, f"Failed for: {query}"
        assert confidence >= 0.6, f"Low confidence for: {query}"


def test_semantic_store_timing_variations():
    """Test semantic matching for store timing queries"""
    classifier = IntentClassifier()
    
    variations = [
        "What time does the store open?",
        "When do you close?",
        "Store hours please",
    ]
    
    for query in variations:
        intent, confidence = classifier.classify(query)
        assert intent == Intent.STORE_TIMINGS, f"Failed for: {query}"
        assert confidence >= 0.6, f"Low confidence for: {query}"


def test_semantic_store_address_variations():
    """Test semantic matching for store address queries"""
    classifier = IntentClassifier()
    
    variations = [
        "Where can I find your shop?",
        "Where is the store located?",
        "How do I find your store?",
    ]
    
    for query in variations:
        intent, confidence = classifier.classify(query)
        assert intent == Intent.STORE_ADDRESS, f"Failed for: {query}"
        assert confidence >= 0.6, f"Low confidence for: {query}"


def test_semantic_hindi_variations():
    """Test semantic matching for Hindi queries"""
    classifier = IntentClassifier()
    
    test_cases = [
        ("10 ग्राम सोना कितना है?", Intent.GOLD_RATE),
        ("चांदी की कीमत क्या है?", Intent.SILVER_RATE),
        ("सोने का सिक्का कितना है?", Intent.GOLD_COIN_RATE),
    ]
    
    for query, expected_intent in test_cases:
        intent, confidence = classifier.classify(query)
        # Hindi keyword matching or semantic matching should work
        assert intent == expected_intent, f"Failed for: {query}"
        assert confidence >= 0.6, f"Low confidence for: {query}"


def test_semantic_confidence_levels():
    """Test that semantic matching returns appropriate confidence levels"""
    classifier = IntentClassifier()
    
    # Exact keyword match should have confidence 1.0
    intent1, conf1 = classifier.classify("gold rate")
    assert conf1 == 1.0
    
    # Semantic match should have confidence 0.8
    intent2, conf2 = classifier.classify("What is the worth of gold?")
    assert conf2 == 0.8
    
    # Both should return same intent
    assert intent1 == intent2 == Intent.GOLD_RATE

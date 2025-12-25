import pytest
from nlu.intent_classifier import IntentClassifier
from nlu.intents import Intent


def test_gold_rate_intent():
    """Test gold rate intent classification"""
    classifier = IntentClassifier()
    
    intent, confidence = classifier.classify("What is the gold rate today?")
    assert intent == Intent.GOLD_RATE
    assert confidence == 1.0
    
    intent, confidence = classifier.classify("gold price per gram")
    assert intent == Intent.GOLD_RATE
    assert confidence == 1.0


def test_silver_rate_intent():
    """Test silver rate intent classification"""
    classifier = IntentClassifier()
    
    intent, confidence = classifier.classify("silver rate today")
    assert intent == Intent.SILVER_RATE
    assert confidence == 1.0
    
    intent, confidence = classifier.classify("How much is silver?")
    assert intent == Intent.SILVER_RATE
    assert confidence == 1.0


def test_platinum_rate_intent():
    """Test platinum rate intent classification"""
    classifier = IntentClassifier()
    
    intent, confidence = classifier.classify("platinum price")
    assert intent == Intent.PLATINUM_RATE
    assert confidence == 1.0


def test_store_timings_intent():
    """Test store timings intent classification"""
    classifier = IntentClassifier()
    
    intent, confidence = classifier.classify("store hours")
    assert intent == Intent.STORE_TIMINGS
    assert confidence == 1.0
    
    intent, confidence = classifier.classify("when are you open")
    assert intent == Intent.STORE_TIMINGS
    assert confidence == 1.0


def test_store_address_intent():
    """Test store address intent classification"""
    classifier = IntentClassifier()
    
    intent, confidence = classifier.classify("store address")
    assert intent == Intent.STORE_ADDRESS
    assert confidence == 1.0
    
    intent, confidence = classifier.classify("where are you located")
    assert intent == Intent.STORE_ADDRESS
    assert confidence == 1.0


def test_greeting_intent():
    """Test greeting intent classification"""
    classifier = IntentClassifier()
    
    intent, confidence = classifier.classify("hello")
    assert intent == Intent.GREETING
    assert confidence == 1.0
    
    intent, confidence = classifier.classify("hi there")
    assert intent == Intent.GREETING
    assert confidence == 1.0


def test_transfer_request_intent():
    """Test transfer request intent classification"""
    classifier = IntentClassifier()
    
    intent, confidence = classifier.classify("talk to agent")
    assert intent == Intent.TRANSFER_REQUEST
    assert confidence == 1.0
    
    intent, confidence = classifier.classify("connect me to a human")
    assert intent == Intent.TRANSFER_REQUEST
    assert confidence == 1.0


def test_fallback_intent():
    """Test fallback for unknown intents"""
    classifier = IntentClassifier()
    
    intent, confidence = classifier.classify("random gibberish xyz")
    assert intent == Intent.FALLBACK
    assert confidence < 0.6


def test_confidence_threshold():
    """Test that low confidence results in fallback"""
    classifier = IntentClassifier()
    
    intent, confidence = classifier.get_intent_confidence("some random text")
    assert intent == Intent.FALLBACK
    assert confidence < IntentClassifier.CONFIDENCE_THRESHOLD

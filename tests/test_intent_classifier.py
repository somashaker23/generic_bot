from app.services.intent_classifier import IntentClassifier


def test_test_drive_intent():
    c = IntentClassifier()
    assert c.classify("I want a test drive") == "book_test_drive"


def test_service_intent():
    c = IntentClassifier()
    assert c.classify("Need car service") == "book_service"


def test_price_intent():
    c = IntentClassifier()
    assert c.classify("Price of Creta?") == "price_inquiry"

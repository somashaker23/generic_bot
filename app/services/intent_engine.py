from app.services.intent_classifier import IntentClassifier
from app.services.entity_extractor import EntityExtractor


class IntentEngine:

    def __init__(self):
        self.classifier = IntentClassifier()
        self.extractor = EntityExtractor()

    def analyze(self, text: str):
        intent = self.classifier.classify(text)
        model = self.extractor.extract_model(text)
        date = self.extractor.extract_date(text)

        return {
            "intent": intent,
            "model": model,
            "date": date
        }

    def analyze_with_transformer(self, text: str):
        # Placeholder for future ML model
        raise NotImplementedError("Transformer model not integrated yet")

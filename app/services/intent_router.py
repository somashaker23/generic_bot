from app.services.intent_engine import IntentEngine
from app.intent_handlers.test_drive_handler import TestDriveHandler
from app.intent_handlers.service_handler import ServiceHandler
from app.intent_handlers.price_handler import PriceHandler

class IntentRouter:

    def __init__(self):
        self.engine = IntentEngine()

        self.handlers = {
            "book_test_drive": TestDriveHandler(),
            "book_service": ServiceHandler(),
            "price_inquiry": PriceHandler()
        }

    def handle(self, text: str):
        result = self.engine.analyze(text)
        intent = result["intent"]

        handler = self.handlers.get(intent)
        if not handler:
            return {
                "reply": "I'm not sure I understood that. Could you please rephrase?",
                "intent": "unknown",
                "entities": result
            }

        reply = handler.handle(result)
        return {
            "reply": reply,
            "intent": intent,
            "entities": result
        }

from typing import Any

from app.services.humor_responder import HumorResponder
from app.services.intent_engine import IntentEngine
from app.services.context_manager import ContextManager
from app.services.intent_refiner import IntentRefiner
from app.intent_handlers.test_drive_handler import TestDriveHandler
from app.intent_handlers.service_handler import ServiceHandler
from app.intent_handlers.price_handler import PriceHandler
from app.services.knowledge_engine import KnowledgeEngine
from app.services.message_sanitizer import MessageSanitizer


class ConversationFlow:

    def __init__(self):
        self.faq_engine = KnowledgeEngine()
        self.engine = IntentEngine()
        self.ctx = ContextManager()
        self.refiner = IntentRefiner()
        self.sanitizer = MessageSanitizer()
        self.humor = HumorResponder()

        self.handlers = {
            "book_test_drive": TestDriveHandler(),
            "book_service": ServiceHandler(),
            "price_inquiry": PriceHandler()
        }

    def process(self, user_id: str, text: str) -> dict[str, Any]:
        clean_text = self.sanitizer.strip_noise(text)

        if not clean_text:
            if self.sanitizer.contains_humor_tokens(text):
                return {"reply": self.humor.playful_humor(), "context": {}}
            if self.sanitizer.is_offtopic(text):
                return {"reply": self.humor.playful_offtopic(), "context": {}}
            return {"reply": "I didn't catch that — can you rephrase?", "context": {}}

        faq_reply = self.faq_engine.search(clean_text)
        if faq_reply:
            return {"reply": faq_reply, "context": {}}

        context = self.ctx.get(user_id)
        analysis = self.engine.analyze(clean_text)

        # If user gives fresh intent, overwrite
        if analysis["intent"] != "unknown":
            context["intent"] = analysis["intent"]

        # Persist entities if present
        if analysis["model"]:
            context["model"] = analysis["model"]

        if analysis["date"]:
            context["date"] = analysis["date"]

        self.ctx.save(user_id, context)

        # Check missing info
        follow_up = self.refiner.missing_info(context.get("intent"), context)
        if follow_up:
            return {"reply": follow_up, "context": context}

        # All data available → finalize flow
        handler = self.handlers.get(context.get("intent"))
        if handler:
            try:
                reply = handler.handle(context)
            except Exception as e:
                import logging
                logging.error(f"Error in handler {context.get('intent')}: {e}")
                reply = "Sorry, something went wrong while processing your request."
            finally:
                self.ctx.clear(user_id)
            return {"reply": reply, "context": context}

        # Unknown
        return {"reply": "I'm not sure I understood that.", "context": context}

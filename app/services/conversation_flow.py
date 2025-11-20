from app.services.intent_engine import IntentEngine
from app.services.context_manager import ContextManager
from app.services.intent_refiner import IntentRefiner
from app.intent_handlers.test_drive_handler import TestDriveHandler
from app.intent_handlers.service_handler import ServiceHandler
from app.intent_handlers.price_handler import PriceHandler


class ConversationFlow:

    def __init__(self):
        self.engine = IntentEngine()
        self.ctx = ContextManager()
        self.refiner = IntentRefiner()

        self.handlers = {
            "book_test_drive": TestDriveHandler(),
            "book_service": ServiceHandler(),
            "price_inquiry": PriceHandler()
        }

    def process(self, user_id: str, text: str):
        context = self.ctx.get(user_id)
        analysis = self.engine.analyze(text)

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
            reply = handler.handle(context)
            self.ctx.clear(user_id)
            return {"reply": reply, "context": context}

        # Unknown
        return {"reply": "I'm not sure I understood that.", "context": context}

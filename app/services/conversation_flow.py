from app.services.message_sanitizer import MessageSanitizer
from app.services.humor_responder import HumorResponder
from app.services.knowledge_engine import KnowledgeEngine
from app.services.intent_engine import IntentEngine
from app.services.context_manager import ContextManager
from app.services.intent_refiner import IntentRefiner

from app.intent_handlers.test_drive_handler import TestDriveHandler
from app.intent_handlers.service_handler import ServiceHandler
from app.intent_handlers.price_handler import PriceHandler


class ConversationFlow:

    def __init__(self):
        self.sanitizer = MessageSanitizer()
        self.humor = HumorResponder()
        self.knowledge = KnowledgeEngine()
        self.engine = IntentEngine()
        self.ctx = ContextManager()
        self.refiner = IntentRefiner()

        self.handlers = {
            "book_test_drive": TestDriveHandler(),
            "book_service": ServiceHandler(),
            "price_inquiry": PriceHandler(),
        }

    def handle_message(self, user_id: str, text: str):
        """
        Master orchestrator:
        sanitize → humor/off-topic → FAQ → intent → slot-fill → refine → handler
        """

        # ─────────────────────────────────────────────
        # 1) SANITIZE FIRST
        # ─────────────────────────────────────────────
        cleaned = self.sanitizer.strip_noise(text)

        # Case: input becomes empty after cleaning
        if not cleaned:
            if self.sanitizer.contains_humor_tokens(text):
                return {"reply": self.humor.humor_reply(), "context": {}}

            if self.sanitizer.is_offtopic(text):
                return {"reply": self.humor.offtopic_reply(), "context": {}}

            return {"reply": "I didn't catch that. Can you rephrase?", "context": {}}

        # ─────────────────────────────────────────────
        # 2) FAQ HANDLING
        # ─────────────────────────────────────────────
        faq_reply = self.knowledge.search(cleaned)
        if faq_reply:
            return {"reply": faq_reply, "context": {}}

        # ─────────────────────────────────────────────
        # 3) INTENT + ENTITY DETECTION
        # ─────────────────────────────────────────────
        context = self.ctx.get(user_id)
        analysis = self.engine.analyze(cleaned)

        # If new intent detected, override previous one
        if analysis["intent"] != "unknown":
            context["intent"] = analysis["intent"]

        # Update extracted entities in context
        if analysis.get("model"):
            context["model"] = analysis["model"]

        if analysis.get("date"):
            context["date"] = analysis["date"]

        self.ctx.save(user_id, context)

        # ─────────────────────────────────────────────
        # 4) SLOT FILLING / CLARIFICATION
        # ─────────────────────────────────────────────
        follow_up = self.refiner.missing_info(context.get("intent"), context)
        if follow_up:
            return {"reply": follow_up, "context": context}

        # ─────────────────────────────────────────────
        # 5) CALL INTENT HANDLER
        # ─────────────────────────────────────────────
        intent = context.get("intent")
        handler = self.handlers.get(intent)

        if handler:
            reply = handler.handle(context)
            self.ctx.clear(user_id)
            return {"reply": reply, "context": context}

        # ─────────────────────────────────────────────
        # 6) FALLBACK
        # ─────────────────────────────────────────────
        return {
            "reply": "I'm not sure I understood that. Can you rephrase?",
            "context": context,
        }

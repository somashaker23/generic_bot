from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler


class GreetingHandler(BaseHandler):
    """Handler for GREETING intent"""
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can handle the intent"""
        return intent == Intent.GREETING
    
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle GREETING intent.
        
        Logic:
        - Return friendly greeting
        - Provide menu of options
        - Return CONTINUE action
        """
        greeting_text = (
            "Hello! Welcome to our jewelry store. 👋\n\n"
            "I can help you with:\n"
            "• Gold, Silver, and Platinum rates\n"
            "• Store timings and locations\n"
            "• General inquiries\n\n"
            "How can I assist you today?"
        )
        
        return OutgoingResponse(
            text=greeting_text,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={"last_query": "greeting"}
        )

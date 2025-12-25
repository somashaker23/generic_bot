from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from localization.language_service import LanguageDetector, ResponseTranslator


class GreetingHandler(BaseHandler):
    """Handler for GREETING intent"""
    
    def __init__(self, translator: ResponseTranslator = None):
        self.translator = translator or ResponseTranslator()
    
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
        - Return friendly greeting in user's language
        - Provide menu of options
        - Return CONTINUE action
        """
        language = context.language
        greeting_text = self.translator.get_response("greeting", language)
        
        return OutgoingResponse(
            text=greeting_text,
            language=language,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={"last_query": "greeting"}
        )

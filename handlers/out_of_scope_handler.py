from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from localization.language_service import ResponseTranslator


class OutOfScopeHandler(BaseHandler):
    """
    Handler for OUT_OF_SCOPE intent.
    
    Handles queries about:
    - Discounts and offers
    - Future rate predictions
    - Any other out-of-scope topics
    """
    
    def __init__(self, translator: ResponseTranslator = None):
        self.translator = translator or ResponseTranslator()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can handle the intent"""
        return intent == Intent.OUT_OF_SCOPE
    
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle OUT_OF_SCOPE intent.
        
        Logic:
        - Politely decline
        - Redirect to available services
        - Do NOT transfer immediately
        """
        language = context.language
        
        response_text = self.translator.get_response("out_of_scope", language)
        
        return OutgoingResponse(
            text=response_text,
            language=language,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={
                "last_query": "out_of_scope",
                "clarification_needed": False
            }
        )

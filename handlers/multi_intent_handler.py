from typing import List
from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from nlu.intent_classifier import IntentClassifier
from localization.language_service import ResponseTranslator


class MultiIntentHandler(BaseHandler):
    """
    Handler for MULTI_INTENT - handles multiple queries in one message.
    Example: "What is the gold rate and store timings?"
    """
    
    def __init__(self, translator: ResponseTranslator = None):
        self.translator = translator or ResponseTranslator()
        self.classifier = IntentClassifier()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can handle the intent"""
        return intent == Intent.MULTI_INTENT
    
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle MULTI_INTENT.
        
        Logic:
        - Extract individual intents from the query
        - Provide brief response acknowledging multiple queries
        - Set flag for bot engine to process each intent separately
        """
        language = context.language
        
        # Get intro message
        intro = self.translator.get_response("multi_intent_response", language)
        
        response_text = intro + "\n\n" + (
            "I'll help you with each query. Please ask them one at a time for detailed information." 
            if language == "en" else
            "मैं हर सवाल में आपकी मदद करूंगा। विस्तृत जानकारी के लिए कृपया एक-एक करके पूछें।"
        )
        
        return OutgoingResponse(
            text=response_text,
            language=language,
            action=ActionSignal.CLARIFY,
            confidence=0.8,
            context_update={
                "last_query": "multi_intent",
                "needs_clarification": True
            }
        )

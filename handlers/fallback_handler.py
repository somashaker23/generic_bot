from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from localization.language_service import ResponseTranslator


class FallbackHandler(BaseHandler):
    """
    Handler for FALLBACK intent.
    
    Rules:
    - Increment clarification_attempts
    - After 2 attempts → TRANSFER_TO_AGENT
    """
    
    def __init__(self, translator: ResponseTranslator = None):
        self.translator = translator or ResponseTranslator()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can handle the intent"""
        return intent == Intent.FALLBACK
    
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle FALLBACK intent.
        
        Logic:
        - Increment clarification attempts
        - Check if should transfer to agent
        - Return clarification or transfer message in user's language
        """
        language = context.language
        
        # Increment clarification attempts
        context.mark_clarification()
        
        # Check if we should transfer to agent
        if context.should_transfer():
            transfer_text = self.translator.get_response("transfer", language)
            return OutgoingResponse(
                text=transfer_text,
                language=language,
                action=ActionSignal.TRANSFER_TO_AGENT,
                confidence=0.0,
                context_update={"transfer_reason": "max_clarifications"}
            )
        
        # Still within clarification limit
        clarification_text = self.translator.get_response("clarification", language)
        
        # Add more detailed help on second attempt
        if context.clarification_attempts == 2:
            if language == "hi":
                clarification_text += "\n\nउदाहरण के लिए:\n• 'सोने की दर क्या है?'\n• 'स्टोर का समय'\n• 'आपका स्टोर कहां है?'"
            else:
                clarification_text += "\n\nFor example:\n• 'What is the gold rate?'\n• 'Store timings'\n• 'Where is your store located?'"
        
        return OutgoingResponse(
            text=clarification_text,
            language=language,
            action=ActionSignal.CLARIFY,
            confidence=0.3,
            context_update={
                "last_query": "fallback",
                "clarification_attempts": context.clarification_attempts
            }
        )

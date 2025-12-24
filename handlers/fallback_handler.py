from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler


class FallbackHandler(BaseHandler):
    """
    Handler for FALLBACK intent.
    
    Rules:
    - Increment clarification_attempts
    - After 2 attempts → TRANSFER_TO_AGENT
    """
    
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
        - Return clarification or transfer message
        """
        # Increment clarification attempts
        context.mark_clarification()
        
        # Check if we should transfer to agent
        if context.should_transfer():
            return OutgoingResponse(
                text=(
                    "I'm having trouble understanding your request. "
                    "Let me connect you with a customer service representative "
                    "who can better assist you."
                ),
                action=ActionSignal.TRANSFER_TO_AGENT,
                confidence=0.0,
                context_update={"transfer_reason": "max_clarifications"}
            )
        
        # Still within clarification limit
        clarification_messages = [
            (
                "I didn't quite understand that. Could you please rephrase?\n\n"
                "You can ask me about:\n"
                "• Gold, Silver, or Platinum rates\n"
                "• Store timings\n"
                "• Store address"
            ),
            (
                "I'm still not sure what you're looking for. Could you try asking differently?\n\n"
                "For example:\n"
                "• 'What is the gold rate?'\n"
                "• 'Store timings'\n"
                "• 'Where is your store located?'"
            )
        ]
        
        # Use different message based on attempt number
        message_index = min(context.clarification_attempts - 1, len(clarification_messages) - 1)
        
        return OutgoingResponse(
            text=clarification_messages[message_index],
            action=ActionSignal.CLARIFY,
            confidence=0.3,
            context_update={
                "last_query": "fallback",
                "clarification_attempts": context.clarification_attempts
            }
        )

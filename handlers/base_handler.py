from abc import ABC, abstractmethod
from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities
from contracts.outgoing_response import OutgoingResponse


class BaseHandler(ABC):
    """
    Abstract base class for intent handlers.
    One intent = one handler file.
    """
    
    @abstractmethod
    def can_handle(self, intent: Intent) -> bool:
        """
        Check if this handler can handle the given intent.
        
        Args:
            intent: Intent to check
        
        Returns:
            True if this handler can handle the intent
        """
        pass
    
    @abstractmethod
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle the intent with given context and entities.
        
        Args:
            context: Conversation context
            entities: Extracted entities
        
        Returns:
            OutgoingResponse with text and action signal
        """
        pass

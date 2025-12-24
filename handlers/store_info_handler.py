from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from services.store_service import StoreService


class StoreInfoHandler(BaseHandler):
    """Handler for STORE_TIMINGS and STORE_ADDRESS intents"""
    
    def __init__(self, store_service: StoreService = None):
        self.store_service = store_service or StoreService()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can handle the intent"""
        return intent in [Intent.STORE_TIMINGS, Intent.STORE_ADDRESS]
    
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle STORE_TIMINGS and STORE_ADDRESS intents.
        
        Logic:
        - Check if city or pincode is provided
        - Ask clarification if both missing
        - Else lookup store info and return
        """
        # Try to find store
        store = self.store_service.get_nearest_store(
            city=entities.city,
            pincode=entities.pincode
        )
        
        if not store:
            # No store found - ask for clarification
            context.mark_clarification()
            return OutgoingResponse(
                text="I couldn't find a store. Could you please provide your city or pincode?",
                action=ActionSignal.CLARIFY,
                confidence=0.5,
                context_update={"needs_location": True}
            )
        
        # Determine which info to return
        if context.last_intent == Intent.STORE_TIMINGS.value:
            response_text = self.store_service.format_store_timings(store)
        else:  # STORE_ADDRESS
            response_text = self.store_service.format_store_address(store)
        
        return OutgoingResponse(
            text=response_text,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={
                "last_query": "store_info",
                "city": store.get("city"),
                "pincode": store.get("pincode")
            }
        )

from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from services.store_service import StoreService
from localization.language_service import ResponseTranslator


class StoreInfoHandler(BaseHandler):
    """Handler for STORE_TIMINGS and STORE_ADDRESS intents"""
    
    def __init__(self, store_service: StoreService = None, translator: ResponseTranslator = None):
        self.store_service = store_service or StoreService()
        self.translator = translator or ResponseTranslator()
    
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
        - Else lookup store info and return in user's language
        """
        language = context.language
        
        # Try to find store
        store = self.store_service.get_nearest_store(
            city=entities.city,
            pincode=entities.pincode
        )
        
        if not store:
            # No store found - ask for clarification
            context.mark_clarification()
            need_location_text = self.translator.get_response("need_location", language)
            return OutgoingResponse(
                text=need_location_text,
                language=language,
                action=ActionSignal.CLARIFY,
                confidence=0.5,
                context_update={"needs_location": True}
            )
        
        # Determine which info to return
        if context.last_intent == Intent.STORE_TIMINGS.value:
            response_text = self.store_service.format_store_timings(store, language)
        else:  # STORE_ADDRESS
            response_text = self.store_service.format_store_address(store, language)
        
        return OutgoingResponse(
            text=response_text,
            language=language,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={
                "last_query": "store_info",
                "city": store.get("city"),
                "pincode": store.get("pincode")
            }
        )

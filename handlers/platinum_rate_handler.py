from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities, MetalType
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from services.rate_service import RateService


class PlatinumRateHandler(BaseHandler):
    """Handler for PLATINUM_RATE intent"""
    
    def __init__(self, rate_service: RateService = None):
        self.rate_service = rate_service or RateService()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can handle the intent"""
        return intent == Intent.PLATINUM_RATE
    
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle PLATINUM_RATE intent.
        
        Logic:
        - Check missing entities (weight has default)
        - Compute rate
        - Return response + CONTINUE
        """
        # Ensure metal type is platinum
        if not entities.metal_type:
            entities.metal_type = MetalType.PLATINUM
        
        # Calculate rate
        total_price, formatted_response = self.rate_service.calculate_rate(
            metal="platinum",
            weight=entities.weight
        )
        
        return OutgoingResponse(
            text=formatted_response,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={
                "last_query": "platinum_rate",
                "metal_type": "platinum",
                "weight": entities.weight
            }
        )

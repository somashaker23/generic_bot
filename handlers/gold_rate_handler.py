from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities, MetalType
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from services.rate_service import RateService


class GoldRateHandler(BaseHandler):
    """Handler for GOLD_RATE intent"""
    
    def __init__(self, rate_service: RateService = None):
        self.rate_service = rate_service or RateService()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can handle the intent"""
        return intent == Intent.GOLD_RATE
    
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle GOLD_RATE intent.
        
        Logic:
        - Check missing entities (purity optional, weight has default)
        - Ask clarification if needed
        - Else compute rate
        - Return response + CONTINUE
        """
        # Check if we need more information
        missing = []
        
        # Metal type should be gold (but might not be extracted if just asking "rate")
        if not entities.metal_type:
            entities.metal_type = MetalType.GOLD
        
        # Purity is optional - if not provided, use 22K as default
        if not entities.purity:
            from nlu.entities import Purity
            entities.purity = Purity.GOLD_22K
        
        # Weight has default of 1 gram, so always available
        
        # All required info available, calculate rate
        total_price, formatted_response = self.rate_service.calculate_rate(
            metal="gold",
            purity=entities.purity,
            weight=entities.weight
        )
        
        return OutgoingResponse(
            text=formatted_response,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={
                "last_query": "gold_rate",
                "metal_type": "gold",
                "purity": entities.purity.value if entities.purity else None,
                "weight": entities.weight
            }
        )

from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities, MetalType, Purity
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from services.rate_service import RateService
from localization.language_service import ResponseTranslator


class GoldRateHandler(BaseHandler):
    """Handler for GOLD_RATE intent"""
    
    def __init__(self, rate_service: RateService = None, translator: ResponseTranslator = None):
        self.rate_service = rate_service or RateService()
        self.translator = translator or ResponseTranslator()
    
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
        - Check for 18K chain constraint
        - Ask clarification if needed
        - Else compute rate in user's language
        - Return response + CONTINUE
        """
        language = context.language
        
        # Metal type should be gold (but might not be extracted if just asking "rate")
        if not entities.metal_type:
            entities.metal_type = MetalType.GOLD
        
        # Purity is optional - if not provided, use 22K as default
        if not entities.purity:
            entities.purity = Purity.GOLD_22K
        
        # Weight has default of 1 gram, so always available
        
        # All required info available, calculate rate
        total_price, formatted_response = self.rate_service.calculate_rate(
            metal="gold",
            purity=entities.purity,
            weight=entities.weight,
            product_type=entities.product_type
        )
        
        # Check for 18K chain unavailable message
        if total_price == 0.0:
            formatted_response = self.translator.get_response("18k_chain_unavailable", language)
        
        return OutgoingResponse(
            text=formatted_response,
            language=language,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={
                "last_query": "gold_rate",
                "metal_type": "gold",
                "purity": entities.purity.value if entities.purity else None,
                "weight": entities.weight
            }
        )

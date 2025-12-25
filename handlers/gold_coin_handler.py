from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities, MetalType, ProductType
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from services.rate_service import RateService
from localization.language_service import ResponseTranslator


class GoldCoinHandler(BaseHandler):
    """Handler for GOLD_COIN_RATE intent - handles gold coins and biscuits with GST"""
    
    def __init__(self, rate_service: RateService = None, translator: ResponseTranslator = None):
        self.rate_service = rate_service or RateService()
        self.translator = translator or ResponseTranslator()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can handle the intent"""
        return intent == Intent.GOLD_COIN_RATE
    
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle GOLD_COIN_RATE intent.
        
        Logic:
        - Gold coins/biscuits are only available in 24K (999 purity)
        - 3% GST is applicable
        - Calculate rate with GST
        """
        from nlu.entities import Purity
        
        # Ensure metal type is gold
        if not entities.metal_type:
            entities.metal_type = MetalType.GOLD
        
        # Gold coins/biscuits are only in 24K
        entities.purity = Purity.GOLD_24K
        
        # Set product type if not detected
        if not entities.product_type:
            entities.product_type = ProductType.COIN
        
        # Calculate rate with GST
        total_price, formatted_response = self.rate_service.calculate_rate(
            metal="gold",
            purity=entities.purity,
            weight=entities.weight,
            product_type=entities.product_type
        )
        
        # Get language from context
        language = context.language
        
        return OutgoingResponse(
            text=formatted_response,
            language=language,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={
                "last_query": "gold_coin_rate",
                "metal_type": "gold",
                "purity": "24K",
                "product_type": entities.product_type.value if entities.product_type else "coin",
                "weight": entities.weight
            }
        )

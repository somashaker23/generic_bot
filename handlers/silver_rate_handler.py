from nlu.intents import Intent
from conversation.context import ConversationContext
from nlu.entities import ExtractedEntities, MetalType
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from handlers.base_handler import BaseHandler
from services.rate_service import RateService
from localization.language_service import ResponseTranslator


class SilverRateHandler(BaseHandler):
    """Handler for SILVER_RATE intent"""
    
    def __init__(self, rate_service: RateService = None, translator: ResponseTranslator = None):
        self.rate_service = rate_service or RateService()
        self.translator = translator or ResponseTranslator()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can handle the intent"""
        return intent == Intent.SILVER_RATE
    
    def handle(
        self,
        context: ConversationContext,
        entities: ExtractedEntities
    ) -> OutgoingResponse:
        """
        Handle SILVER_RATE intent.
        
        Logic:
        - Check missing entities (weight has default)
        - Use regional rate if state/region is provided
        - Compute rate in user's language
        - Return response + CONTINUE
        """
        language = context.language
        
        # Ensure metal type is silver
        if not entities.metal_type:
            entities.metal_type = MetalType.SILVER
        
        # Calculate rate (with regional pricing if available)
        total_price, formatted_response = self.rate_service.calculate_rate(
            metal="silver",
            weight=entities.weight,
            region=entities.region
        )
        
        return OutgoingResponse(
            text=formatted_response,
            language=language,
            action=ActionSignal.CONTINUE,
            confidence=1.0,
            context_update={
                "last_query": "silver_rate",
                "metal_type": "silver",
                "weight": entities.weight,
                "region": entities.region.value if entities.region else None
            }
        )

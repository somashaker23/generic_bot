from typing import Dict
from contracts.incoming_event import IncomingEvent
from contracts.outgoing_response import OutgoingResponse, ActionSignal
from conversation.context import ConversationContext
from nlu.intent_classifier import IntentClassifier
from nlu.entity_resolver import EntityResolver
from nlu.intents import Intent
from handlers.gold_rate_handler import GoldRateHandler
from handlers.silver_rate_handler import SilverRateHandler
from handlers.platinum_rate_handler import PlatinumRateHandler
from handlers.store_info_handler import StoreInfoHandler
from handlers.greeting_handler import GreetingHandler
from handlers.fallback_handler import FallbackHandler
from services.rate_service import RateService
from services.store_service import StoreService


class BotEngine:
    """
    Orchestration layer - single entry point for the bot brain.
    Routes incoming events through the full pipeline.
    
    Steps:
    1. Build context
    2. Classify intent
    3. Resolve entities
    4. Select handler
    5. Build response
    6. Apply transfer rules
    """
    
    def __init__(
        self,
        rate_service: RateService = None,
        store_service: StoreService = None
    ):
        # Initialize services
        self.rate_service = rate_service or RateService()
        self.store_service = store_service or StoreService()
        
        # Initialize NLU components
        self.intent_classifier = IntentClassifier()
        self.entity_resolver = EntityResolver()
        
        # Initialize handlers
        self.handlers = {
            Intent.GOLD_RATE: GoldRateHandler(self.rate_service),
            Intent.SILVER_RATE: SilverRateHandler(self.rate_service),
            Intent.PLATINUM_RATE: PlatinumRateHandler(self.rate_service),
            Intent.STORE_TIMINGS: StoreInfoHandler(self.store_service),
            Intent.STORE_ADDRESS: StoreInfoHandler(self.store_service),
            Intent.GREETING: GreetingHandler(),
            Intent.FALLBACK: FallbackHandler(),
            Intent.TRANSFER_REQUEST: FallbackHandler(),  # Reuse fallback for transfer
        }
        
        # Context storage (in-memory for now)
        self.contexts: Dict[str, ConversationContext] = {}
    
    def process_event(self, event: IncomingEvent) -> OutgoingResponse:
        """
        Process incoming event through the full pipeline.
        
        Args:
            event: Normalized incoming event
        
        Returns:
            OutgoingResponse with text and action signal
        """
        # Step 1: Build/update context
        context = self._get_or_create_context(event)
        context.update_from_event(event)
        
        # Step 2: Classify intent
        intent, confidence = self.intent_classifier.get_intent_confidence(event.user_text)
        context.last_intent = intent.value
        
        # Step 3: Resolve entities
        entities = self.entity_resolver.resolve(event.user_text)
        
        # Step 4: Select handler
        handler = self.handlers.get(intent)
        if not handler:
            # Fallback to fallback handler if no handler found
            handler = self.handlers[Intent.FALLBACK]
        
        # Step 5: Build response
        response = handler.handle(context, entities)
        
        # Step 6: Apply transfer rules
        if context.should_transfer() and response.action != ActionSignal.TRANSFER_TO_AGENT:
            response = OutgoingResponse(
                text=(
                    "I notice we've been having some difficulty. "
                    "Let me connect you with a customer service representative."
                ),
                action=ActionSignal.TRANSFER_TO_AGENT,
                confidence=0.0,
                context_update={"transfer_reason": "context_rules"}
            )
        
        # Handle explicit transfer requests
        if intent == Intent.TRANSFER_REQUEST:
            response = OutgoingResponse(
                text="Connecting you to a customer service representative. Please hold.",
                action=ActionSignal.TRANSFER_TO_AGENT,
                confidence=1.0,
                context_update={"transfer_reason": "user_request"}
            )
        
        # Update context from response
        for key, value in response.context_update.items():
            setattr(context, key, value)
        
        # Store context
        self._store_context(context)
        
        return response
    
    def _get_or_create_context(self, event: IncomingEvent) -> ConversationContext:
        """Get existing context or create new one"""
        if event.session_id not in self.contexts:
            self.contexts[event.session_id] = ConversationContext(
                session_id=event.session_id,
                language=event.language
            )
        return self.contexts[event.session_id]
    
    def _store_context(self, context: ConversationContext) -> None:
        """Store context in memory"""
        self.contexts[context.session_id] = context
    
    def clear_context(self, session_id: str) -> None:
        """Clear context for a session"""
        if session_id in self.contexts:
            del self.contexts[session_id]

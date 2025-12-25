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
from handlers.gold_coin_handler import GoldCoinHandler
from handlers.store_info_handler import StoreInfoHandler
from handlers.greeting_handler import GreetingHandler
from handlers.fallback_handler import FallbackHandler
from handlers.out_of_scope_handler import OutOfScopeHandler
from handlers.multi_intent_handler import MultiIntentHandler
from services.rate_service import RateService
from services.store_service import StoreService
from localization.language_service import LanguageDetector, ResponseTranslator


class BotEngine:
    """
    Orchestration layer - single entry point for the bot brain.
    Routes incoming events through the full pipeline.
    
    Steps:
    1. Detect language
    2. Build context
    3. Classify intent
    4. Resolve entities
    5. Select handler
    6. Build response
    7. Apply transfer rules
    """
    
    def __init__(
        self,
        rate_service: RateService = None,
        store_service: StoreService = None,
        use_three_layer_pipeline: bool = False,
        enable_local_model: bool = False,
        enable_heavy_llm: bool = False
    ):
        """
        Initialize BotEngine with optional three-layer NLU pipeline.
        
        Args:
            rate_service: Service for rate calculations
            store_service: Service for store information
            use_three_layer_pipeline: Enable three-layer NLU pipeline (default: False)
            enable_local_model: Enable local model fallback (default: False)
            enable_heavy_llm: Enable heavy LLM fallback (default: False)
        """
        # Initialize services
        self.rate_service = rate_service or RateService()
        self.store_service = store_service or StoreService()
        
        # Initialize language services
        self.language_detector = LanguageDetector()
        self.translator = ResponseTranslator()
        
        # Initialize NLU components
        self.intent_classifier = IntentClassifier()
        self.entity_resolver = EntityResolver()
        
        # Initialize three-layer pipeline if enabled
        self.use_three_layer_pipeline = use_three_layer_pipeline
        self.three_layer_pipeline = None
        
        if use_three_layer_pipeline:
            from nlu.three_layer_pipeline import ThreeLayerNLUPipeline
            from nlu.local_model_classifier import LocalModelClassifier
            from nlu.heavy_llm_classifier import HeavyLLMClassifier
            
            # Initialize optional classifiers
            local_model = LocalModelClassifier() if enable_local_model else None
            heavy_llm = HeavyLLMClassifier() if enable_heavy_llm else None
            
            self.three_layer_pipeline = ThreeLayerNLUPipeline(
                fast_classifier=self.intent_classifier,
                fast_entity_resolver=self.entity_resolver,
                local_model_classifier=local_model,
                heavy_llm_classifier=heavy_llm,
                enable_local_model=enable_local_model,
                enable_heavy_llm=enable_heavy_llm
            )
        
        # Initialize handlers
        self.handlers = {
            Intent.GOLD_RATE: GoldRateHandler(self.rate_service, self.translator),
            Intent.SILVER_RATE: SilverRateHandler(self.rate_service, self.translator),
            Intent.PLATINUM_RATE: PlatinumRateHandler(self.rate_service, self.translator),
            Intent.GOLD_COIN_RATE: GoldCoinHandler(self.rate_service, self.translator),
            Intent.STORE_TIMINGS: StoreInfoHandler(self.store_service, self.translator),
            Intent.STORE_ADDRESS: StoreInfoHandler(self.store_service, self.translator),
            Intent.GREETING: GreetingHandler(self.translator),
            Intent.FALLBACK: FallbackHandler(self.translator),
            Intent.OUT_OF_SCOPE: OutOfScopeHandler(self.translator),
            Intent.MULTI_INTENT: MultiIntentHandler(self.translator),
            Intent.TRANSFER_REQUEST: self._create_transfer_handler(),
        }
        
        # Context storage (in-memory for now)
        self.contexts: Dict[str, ConversationContext] = {}
    
    def _create_transfer_handler(self):
        """Create a simple transfer handler"""
        class TransferHandler:
            def __init__(self, translator):
                self.translator = translator
            
            def can_handle(self, intent):
                return intent == Intent.TRANSFER_REQUEST
            
            def handle(self, context, entities):
                language = context.language
                text = self.translator.get_response("transfer_request", language)
                return OutgoingResponse(
                    text=text,
                    language=language,
                    action=ActionSignal.TRANSFER_TO_AGENT,
                    confidence=1.0,
                    context_update={"transfer_reason": "user_request"}
                )
        
        return TransferHandler(self.translator)
    
    def process_event(self, event: IncomingEvent) -> OutgoingResponse:
        """
        Process incoming event through the full pipeline.
        
        Uses three-layer NLU pipeline if enabled, otherwise uses standard pipeline.
        
        Args:
            event: Normalized incoming event
        
        Returns:
            OutgoingResponse with text and action signal
        """
        # Step 0: Detect language from user text
        detected_language = self.language_detector.detect_language(event.user_text)
        if event.language == "en" and detected_language != "en":
            event.language = detected_language
        
        # Step 1: Build/update context
        context = self._get_or_create_context(event)
        context.update_from_event(event)
        
        # Step 2: Classify intent and resolve entities
        if self.use_three_layer_pipeline and self.three_layer_pipeline:
            # Use three-layer pipeline
            nlu_result = self.three_layer_pipeline.process(event.user_text)
            intent = nlu_result.intent
            confidence = nlu_result.confidence
            entities = nlu_result.entities
            
            # Store NLU metadata in context
            context.nlu_metadata = {
                "nlu_path": nlu_result.path_taken.value,
                "nlu_processing_time_ms": nlu_result.processing_time_ms,
                "nlu_model_used": nlu_result.model_used,
                "nlu_confidence": confidence
            }
        else:
            # Use standard pipeline
            intent, confidence = self.intent_classifier.get_intent_confidence(event.user_text)
            entities = self.entity_resolver.resolve(event.user_text)
            context.nlu_metadata = {}
        
        context.last_intent = intent.value
        
        # Step 3: Select handler
        handler = self.handlers.get(intent)
        if not handler:
            # Fallback to fallback handler if no handler found
            handler = self.handlers[Intent.FALLBACK]
        
        # Step 5: Build response
        response = handler.handle(context, entities)
        
        # Step 6: Apply transfer rules
        if context.should_transfer() and response.action != ActionSignal.TRANSFER_TO_AGENT:
            language = context.language
            transfer_text = self.translator.get_response("transfer", language)
            response = OutgoingResponse(
                text=transfer_text,
                language=language,
                action=ActionSignal.TRANSFER_TO_AGENT,
                confidence=0.0,
                context_update={"transfer_reason": "context_rules"}
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
    
    def get_pipeline_statistics(self) -> Dict:
        """
        Get three-layer pipeline statistics.
        
        Returns:
            Dict with usage statistics and performance metrics,
            or None if three-layer pipeline is not enabled
        """
        if not self.use_three_layer_pipeline or not self.three_layer_pipeline:
            return {
                "enabled": False,
                "message": "Three-layer pipeline is not enabled"
            }
        
        stats = self.three_layer_pipeline.get_statistics()
        stats["enabled"] = True
        return stats
    
    def reset_pipeline_statistics(self) -> None:
        """Reset three-layer pipeline statistics"""
        if self.use_three_layer_pipeline and self.three_layer_pipeline:
            self.three_layer_pipeline.reset_statistics()

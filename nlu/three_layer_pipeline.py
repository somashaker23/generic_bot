"""
Three-layer NLU processing pipeline for optimized latency.

Layers:
1. Fast Path (0-50ms): Rule-based NLU
2. Fallback Path (100-300ms): Local small model (Qwen 1.5B, Phi-3 Mini, Gemma 2B)
3. Heavy LLM Path (~1-2s): Remote large LLM for deep reasoning

The pipeline routes requests based on confidence scores, ensuring fast responses
for common queries while preserving intelligence for complex cases.
"""

from typing import Tuple, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
import time
from nlu.intents import Intent
from nlu.entities import ExtractedEntities


class NLUPath(Enum):
    """Enum for tracking which NLU path was taken"""
    FAST = "fast"
    FALLBACK = "fallback"
    HEAVY = "heavy"
    

@dataclass
class NLUResult:
    """Result from NLU processing with metadata"""
    intent: Intent
    confidence: float
    entities: ExtractedEntities
    path_taken: NLUPath
    processing_time_ms: float
    model_used: Optional[str] = None
    

class ThreeLayerNLUPipeline:
    """
    Three-layer NLU processing pipeline with progressive fallback.
    
    Fast Path (0-50ms):
        Uses rule-based NLU with keyword and semantic matching.
        If confidence >= 0.7 → respond immediately
        
    Fallback Path (100-300ms):
        Uses local small model (Qwen 1.5B, Phi-3 Mini, Gemma 2B)
        If confidence >= 0.5 → respond with local model
        
    Heavy LLM Path (~1-2s):
        Uses remote large LLM (GPT-4, Claude, etc.)
        Only when both previous paths return confidence < 0.5
        
    Target: Heavy LLM used in <10% of queries
    """
    
    # Confidence thresholds
    FAST_PATH_THRESHOLD = 0.7
    FALLBACK_PATH_THRESHOLD = 0.5
    
    def __init__(
        self,
        fast_classifier,
        fast_entity_resolver,
        local_model_classifier=None,
        heavy_llm_classifier=None,
        enable_local_model: bool = False,
        enable_heavy_llm: bool = False
    ):
        """
        Initialize the three-layer NLU pipeline.
        
        Args:
            fast_classifier: Rule-based intent classifier
            fast_entity_resolver: Rule-based entity resolver
            local_model_classifier: Optional local model classifier
            heavy_llm_classifier: Optional heavy LLM classifier
            enable_local_model: Whether to enable fallback to local model
            enable_heavy_llm: Whether to enable fallback to heavy LLM
        """
        self.fast_classifier = fast_classifier
        self.fast_entity_resolver = fast_entity_resolver
        self.local_model_classifier = local_model_classifier
        self.heavy_llm_classifier = heavy_llm_classifier
        self.enable_local_model = enable_local_model
        self.enable_heavy_llm = enable_heavy_llm
        
        # Statistics tracking
        self.stats = {
            "total_queries": 0,
            "fast_path_count": 0,
            "fallback_path_count": 0,
            "heavy_path_count": 0,
            "fast_path_time_ms": [],
            "fallback_path_time_ms": [],
            "heavy_path_time_ms": []
        }
    
    def process(self, text: str) -> NLUResult:
        """
        Process text through the three-layer pipeline.
        
        Args:
            text: User input text
            
        Returns:
            NLUResult with intent, entities, and metadata
        """
        self.stats["total_queries"] += 1
        
        # Layer 1: Fast Path (Rule-based)
        result = self._try_fast_path(text)
        if result:
            return result
        
        # Layer 2: Fallback Path (Local Model)
        if self.enable_local_model and self.local_model_classifier:
            result = self._try_fallback_path(text)
            if result:
                return result
        
        # Layer 3: Heavy LLM Path
        if self.enable_heavy_llm and self.heavy_llm_classifier:
            result = self._try_heavy_path(text)
            if result:
                return result
        
        # Ultimate fallback - return fast path result with low confidence
        return self._get_fallback_result(text)
    
    def _try_fast_path(self, text: str) -> Optional[NLUResult]:
        """
        Try fast path with rule-based NLU.
        Target: 0-50ms
        """
        start_time = time.time()
        
        try:
            # Use existing rule-based classifier
            intent, confidence = self.fast_classifier.classify(text)
            entities = self.fast_entity_resolver.resolve(text)
            
            processing_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Check if confidence meets threshold
            if confidence >= self.FAST_PATH_THRESHOLD:
                self.stats["fast_path_count"] += 1
                self.stats["fast_path_time_ms"].append(processing_time)
                
                return NLUResult(
                    intent=intent,
                    confidence=confidence,
                    entities=entities,
                    path_taken=NLUPath.FAST,
                    processing_time_ms=processing_time,
                    model_used="rule_based"
                )
            
            # Confidence too low for fast path
            return None
            
        except Exception as e:
            # If fast path fails, return None to try next layer
            print(f"Fast path error: {e}")
            return None
    
    def _try_fallback_path(self, text: str) -> Optional[NLUResult]:
        """
        Try fallback path with local small model.
        Target: 100-300ms
        """
        start_time = time.time()
        
        try:
            # Use local model classifier (e.g., Qwen 1.5B, Phi-3 Mini, Gemma 2B)
            intent, confidence, entities = self.local_model_classifier.classify_with_entities(text)
            
            processing_time = (time.time() - start_time) * 1000
            
            # Check if confidence meets threshold
            if confidence >= self.FALLBACK_PATH_THRESHOLD:
                self.stats["fallback_path_count"] += 1
                self.stats["fallback_path_time_ms"].append(processing_time)
                
                return NLUResult(
                    intent=intent,
                    confidence=confidence,
                    entities=entities,
                    path_taken=NLUPath.FALLBACK,
                    processing_time_ms=processing_time,
                    model_used="local_small_model"
                )
            
            # Confidence too low for fallback path
            return None
            
        except Exception as e:
            print(f"Fallback path error: {e}")
            return None
    
    def _try_heavy_path(self, text: str) -> Optional[NLUResult]:
        """
        Try heavy path with remote large LLM.
        Target: ~1-2s
        """
        start_time = time.time()
        
        try:
            # Use heavy LLM classifier (e.g., GPT-4, Claude)
            intent, confidence, entities = self.heavy_llm_classifier.classify_with_entities(text)
            
            processing_time = (time.time() - start_time) * 1000
            
            self.stats["heavy_path_count"] += 1
            self.stats["heavy_path_time_ms"].append(processing_time)
            
            return NLUResult(
                intent=intent,
                confidence=confidence,
                entities=entities,
                path_taken=NLUPath.HEAVY,
                processing_time_ms=processing_time,
                model_used="heavy_llm"
            )
            
        except Exception as e:
            print(f"Heavy path error: {e}")
            return None
    
    def _get_fallback_result(self, text: str) -> NLUResult:
        """
        Ultimate fallback when all paths fail or are disabled.
        Returns FALLBACK intent with low confidence.
        """
        start_time = time.time()
        
        # Try fast path one more time but accept any result
        intent, confidence = self.fast_classifier.classify(text)
        entities = self.fast_entity_resolver.resolve(text)
        
        processing_time = (time.time() - start_time) * 1000
        
        return NLUResult(
            intent=intent if confidence > 0 else Intent.FALLBACK,
            confidence=confidence,
            entities=entities,
            path_taken=NLUPath.FAST,
            processing_time_ms=processing_time,
            model_used="rule_based_fallback"
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get pipeline usage statistics.
        
        Returns:
            Dict with usage statistics and performance metrics
        """
        total = self.stats["total_queries"]
        if total == 0:
            return {"total_queries": 0, "message": "No queries processed yet"}
        
        fast_pct = (self.stats["fast_path_count"] / total) * 100
        fallback_pct = (self.stats["fallback_path_count"] / total) * 100
        heavy_pct = (self.stats["heavy_path_count"] / total) * 100
        
        def avg(lst):
            return sum(lst) / len(lst) if lst else 0
        
        return {
            "total_queries": total,
            "path_distribution": {
                "fast_path": {
                    "count": self.stats["fast_path_count"],
                    "percentage": f"{fast_pct:.1f}%",
                    "avg_time_ms": f"{avg(self.stats['fast_path_time_ms']):.2f}"
                },
                "fallback_path": {
                    "count": self.stats["fallback_path_count"],
                    "percentage": f"{fallback_pct:.1f}%",
                    "avg_time_ms": f"{avg(self.stats['fallback_path_time_ms']):.2f}"
                },
                "heavy_path": {
                    "count": self.stats["heavy_path_count"],
                    "percentage": f"{heavy_pct:.1f}%",
                    "avg_time_ms": f"{avg(self.stats['heavy_path_time_ms']):.2f}"
                }
            },
            "performance": {
                "fast_path_target": "0-50ms",
                "fallback_path_target": "100-300ms",
                "heavy_path_target": "1000-2000ms",
                "heavy_llm_usage_target": "<10%",
                "heavy_llm_usage_actual": f"{heavy_pct:.1f}%",
                "target_met": heavy_pct < 10
            }
        }
    
    def reset_statistics(self):
        """Reset all statistics counters"""
        self.stats = {
            "total_queries": 0,
            "fast_path_count": 0,
            "fallback_path_count": 0,
            "heavy_path_count": 0,
            "fast_path_time_ms": [],
            "fallback_path_time_ms": [],
            "heavy_path_time_ms": []
        }

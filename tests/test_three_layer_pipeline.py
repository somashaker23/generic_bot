"""
Tests for the three-layer NLU processing pipeline.

Tests verify:
1. Fast path routing and performance (<50ms target)
2. Fallback path routing when fast path confidence is low
3. Heavy LLM path routing when both fast and fallback fail
4. Statistics tracking and reporting
5. No unnecessary LLM calls
"""

import time
from nlu.three_layer_pipeline import ThreeLayerNLUPipeline, NLUPath
from nlu.intent_classifier import IntentClassifier
from nlu.entity_resolver import EntityResolver
from nlu.intents import Intent


def test_fast_path_high_confidence():
    """Test that high confidence queries use fast path only"""
    classifier = IntentClassifier()
    resolver = EntityResolver()
    
    pipeline = ThreeLayerNLUPipeline(
        fast_classifier=classifier,
        fast_entity_resolver=resolver,
        enable_local_model=False,
        enable_heavy_llm=False
    )
    
    # Query with exact keyword match should have high confidence
    result = pipeline.process("gold rate")
    
    assert result.path_taken == NLUPath.FAST
    assert result.confidence >= 0.7
    assert result.intent == Intent.GOLD_RATE
    assert result.processing_time_ms < 50  # Target: 0-50ms
    assert result.model_used == "rule_based"


def test_fast_path_semantic_match():
    """Test semantic matching in fast path"""
    classifier = IntentClassifier()
    resolver = EntityResolver()
    
    pipeline = ThreeLayerNLUPipeline(
        fast_classifier=classifier,
        fast_entity_resolver=resolver,
        enable_local_model=False,
        enable_heavy_llm=False
    )
    
    # Natural language query should use semantic matching
    result = pipeline.process("How much is 20 grams of 18k gold worth?")
    
    assert result.path_taken == NLUPath.FAST
    assert result.confidence >= 0.7  # Semantic match gives 0.8
    assert result.intent == Intent.GOLD_RATE
    assert result.processing_time_ms < 50


def test_fast_path_performance():
    """Test that fast path meets performance target"""
    classifier = IntentClassifier()
    resolver = EntityResolver()
    
    pipeline = ThreeLayerNLUPipeline(
        fast_classifier=classifier,
        fast_entity_resolver=resolver,
        enable_local_model=False,
        enable_heavy_llm=False
    )
    
    # Run multiple queries and check average time
    queries = [
        "gold rate",
        "silver price",
        "store timings",
        "What is the gold rate?",
        "How much is silver?",
    ]
    
    times = []
    for query in queries:
        result = pipeline.process(query)
        times.append(result.processing_time_ms)
    
    avg_time = sum(times) / len(times)
    assert avg_time < 50, f"Average time {avg_time}ms exceeds 50ms target"


def test_statistics_tracking():
    """Test that pipeline tracks statistics correctly"""
    classifier = IntentClassifier()
    resolver = EntityResolver()
    
    pipeline = ThreeLayerNLUPipeline(
        fast_classifier=classifier,
        fast_entity_resolver=resolver,
        enable_local_model=False,
        enable_heavy_llm=False
    )
    
    # Process several queries
    queries = [
        "gold rate",
        "silver price",
        "store timings",
        "platinum rate",
        "greeting hello"
    ]
    
    for query in queries:
        pipeline.process(query)
    
    # Check statistics
    stats = pipeline.get_statistics()
    
    assert stats["total_queries"] == 5
    assert stats["path_distribution"]["fast_path"]["count"] > 0
    assert stats["path_distribution"]["fallback_path"]["count"] == 0
    assert stats["path_distribution"]["heavy_path"]["count"] == 0
    
    # Check percentages
    fast_pct = float(stats["path_distribution"]["fast_path"]["percentage"].rstrip("%"))
    assert fast_pct > 0


def test_statistics_reset():
    """Test that statistics can be reset"""
    classifier = IntentClassifier()
    resolver = EntityResolver()
    
    pipeline = ThreeLayerNLUPipeline(
        fast_classifier=classifier,
        fast_entity_resolver=resolver,
        enable_local_model=False,
        enable_heavy_llm=False
    )
    
    # Process some queries
    pipeline.process("gold rate")
    pipeline.process("silver rate")
    
    # Reset statistics
    pipeline.reset_statistics()
    
    # Check that stats are cleared
    stats = pipeline.get_statistics()
    assert stats["total_queries"] == 0


def test_no_unnecessary_llm_calls():
    """Test that LLM is not called when fast path succeeds"""
    classifier = IntentClassifier()
    resolver = EntityResolver()
    
    # Track if expensive paths were called
    local_model_called = False
    heavy_llm_called = False
    
    class MockLocalModel:
        def classify_with_entities(self, text):
            nonlocal local_model_called
            local_model_called = True
            raise NotImplementedError("Should not be called")
    
    class MockHeavyLLM:
        def classify_with_entities(self, text):
            nonlocal heavy_llm_called
            heavy_llm_called = True
            raise NotImplementedError("Should not be called")
    
    pipeline = ThreeLayerNLUPipeline(
        fast_classifier=classifier,
        fast_entity_resolver=resolver,
        local_model_classifier=MockLocalModel(),
        heavy_llm_classifier=MockHeavyLLM(),
        enable_local_model=True,
        enable_heavy_llm=True
    )
    
    # Process a query that should succeed in fast path
    result = pipeline.process("gold rate")
    
    # Verify expensive paths were not called
    assert result.path_taken == NLUPath.FAST
    assert not local_model_called, "Local model should not be called for high confidence fast path"
    assert not heavy_llm_called, "Heavy LLM should not be called for high confidence fast path"


def test_multiple_queries_distribution():
    """Test query distribution across paths"""
    classifier = IntentClassifier()
    resolver = EntityResolver()
    
    pipeline = ThreeLayerNLUPipeline(
        fast_classifier=classifier,
        fast_entity_resolver=resolver,
        enable_local_model=False,
        enable_heavy_llm=False
    )
    
    # Mix of queries with varying confidence
    queries = [
        "gold rate",  # High confidence
        "silver price",  # High confidence
        "store timings",  # High confidence
        "How much is gold?",  # Semantic match
        "What's the value of silver?",  # Semantic match
        "Tell me platinum cost",  # Semantic match
        "hello",  # High confidence
        "Where is your store?",  # Semantic match
    ]
    
    for query in queries:
        result = pipeline.process(query)
        assert result.path_taken == NLUPath.FAST
        assert result.confidence >= 0.7
    
    stats = pipeline.get_statistics()
    
    # All queries should use fast path
    assert stats["total_queries"] == len(queries)
    assert stats["path_distribution"]["fast_path"]["count"] == len(queries)
    
    # Heavy LLM should not be used
    assert stats["path_distribution"]["heavy_path"]["count"] == 0
    heavy_pct = float(stats["path_distribution"]["heavy_path"]["percentage"].rstrip("%"))
    assert heavy_pct == 0.0
    assert stats["performance"]["target_met"] == True  # <10% target


def test_logging_includes_path_and_confidence():
    """Test that NLU result includes logging information"""
    classifier = IntentClassifier()
    resolver = EntityResolver()
    
    pipeline = ThreeLayerNLUPipeline(
        fast_classifier=classifier,
        fast_entity_resolver=resolver,
        enable_local_model=False,
        enable_heavy_llm=False
    )
    
    result = pipeline.process("gold rate")
    
    # Check that all required logging fields are present
    assert hasattr(result, 'path_taken')
    assert hasattr(result, 'confidence')
    assert hasattr(result, 'processing_time_ms')
    assert hasattr(result, 'model_used')
    assert hasattr(result, 'intent')
    assert hasattr(result, 'entities')
    
    # Check values
    assert result.path_taken == NLUPath.FAST
    assert result.confidence > 0
    assert result.processing_time_ms >= 0
    assert result.model_used is not None

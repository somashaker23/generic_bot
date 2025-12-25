import pytest
from orchestrator.bot_engine import BotEngine
from contracts.incoming_event import IncomingEvent, Channel
from contracts.outgoing_response import ActionSignal
from nlu.intents import Intent


def test_bot_engine_greeting():
    """Test bot engine processing greeting"""
    engine = BotEngine()
    
    event = IncomingEvent(
        session_id="test123",
        user_text="Hello",
        language="en"
    )
    
    response = engine.process_event(event)
    
    assert "Welcome" in response.text or "Hello" in response.text
    assert response.action == ActionSignal.CONTINUE
    assert response.confidence > 0


def test_bot_engine_gold_rate():
    """Test bot engine processing gold rate query"""
    engine = BotEngine()
    
    event = IncomingEvent(
        session_id="test123",
        user_text="What is the gold rate today?",
        language="en"
    )
    
    response = engine.process_event(event)
    
    assert "Gold" in response.text or "gold" in response.text
    assert response.action == ActionSignal.CONTINUE


def test_bot_engine_silver_rate():
    """Test bot engine processing silver rate query"""
    engine = BotEngine()
    
    event = IncomingEvent(
        session_id="test123",
        user_text="silver price",
        language="en"
    )
    
    response = engine.process_event(event)
    
    assert "Silver" in response.text or "silver" in response.text
    assert response.action == ActionSignal.CONTINUE


def test_bot_engine_store_timings():
    """Test bot engine processing store timings query"""
    engine = BotEngine()
    
    event = IncomingEvent(
        session_id="test123",
        user_text="store hours in Mumbai",
        language="en"
    )
    
    response = engine.process_event(event)
    
    assert "Timings" in response.text or "AM" in response.text or "PM" in response.text
    assert response.action == ActionSignal.CONTINUE


def test_bot_engine_fallback():
    """Test bot engine fallback handling"""
    engine = BotEngine()
    
    event = IncomingEvent(
        session_id="test456",
        user_text="xyzabc random gibberish",
        language="en"
    )
    
    response = engine.process_event(event)
    
    assert response.action in [ActionSignal.CLARIFY, ActionSignal.CONTINUE]


def test_bot_engine_transfer_on_multiple_clarifications():
    """Test bot engine transfers after multiple clarifications"""
    engine = BotEngine()
    
    # Send multiple unclear messages
    for i in range(3):
        event = IncomingEvent(
            session_id="test789",
            user_text=f"unclear message {i}",
            language="en"
        )
        response = engine.process_event(event)
    
    # Should eventually transfer
    assert response.action == ActionSignal.TRANSFER_TO_AGENT


def test_bot_engine_explicit_transfer_request():
    """Test bot engine handles explicit transfer request"""
    engine = BotEngine()
    
    event = IncomingEvent(
        session_id="test999",
        user_text="I want to talk to an agent",
        language="en"
    )
    
    response = engine.process_event(event)
    
    assert response.action == ActionSignal.TRANSFER_TO_AGENT


def test_bot_engine_context_persistence():
    """Test context persists across messages"""
    engine = BotEngine()
    
    # First message
    event1 = IncomingEvent(
        session_id="test111",
        user_text="Hello",
        language="en"
    )
    engine.process_event(event1)
    
    # Second message
    event2 = IncomingEvent(
        session_id="test111",
        user_text="gold rate",
        language="en"
    )
    response2 = engine.process_event(event2)
    
    # Context should have recorded 2 turns
    context = engine.contexts.get("test111")
    assert context is not None
    assert context.turn_count == 2


def test_bot_engine_clear_context():
    """Test clearing context"""
    engine = BotEngine()
    
    event = IncomingEvent(
        session_id="test222",
        user_text="Hello",
        language="en"
    )
    engine.process_event(event)
    
    assert "test222" in engine.contexts
    
    engine.clear_context("test222")
    assert "test222" not in engine.contexts

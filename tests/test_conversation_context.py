import pytest
from conversation.context import ConversationContext
from contracts.incoming_event import IncomingEvent, Channel


def test_context_initialization():
    """Test conversation context initialization"""
    context = ConversationContext(session_id="test123", language="en")
    
    assert context.session_id == "test123"
    assert context.language == "en"
    assert context.turn_count == 0
    assert context.clarification_attempts == 0
    assert context.last_intent is None


def test_update_from_event():
    """Test updating context from event"""
    context = ConversationContext(session_id="test123")
    event = IncomingEvent(
        session_id="test123",
        user_text="Hello",
        language="en",
        channel=Channel.CHAT
    )
    
    context.update_from_event(event)
    assert context.turn_count == 1
    assert context.language == "en"


def test_mark_clarification():
    """Test marking clarification attempts"""
    context = ConversationContext(session_id="test123")
    
    assert context.clarification_attempts == 0
    
    context.mark_clarification()
    assert context.clarification_attempts == 1
    
    context.mark_clarification()
    assert context.clarification_attempts == 2


def test_should_transfer_clarification_limit():
    """Test transfer on clarification limit"""
    context = ConversationContext(session_id="test123")
    
    assert not context.should_transfer()
    
    context.mark_clarification()
    assert not context.should_transfer()
    
    context.mark_clarification()
    assert context.should_transfer()  # Should transfer after 2 attempts


def test_should_transfer_turn_limit():
    """Test transfer on turn count limit"""
    context = ConversationContext(session_id="test123")
    
    # Simulate many turns
    for _ in range(21):
        event = IncomingEvent(session_id="test123", user_text="test")
        context.update_from_event(event)
    
    assert context.should_transfer()  # Should transfer after 20 turns


def test_set_missing_slots():
    """Test setting missing slots"""
    context = ConversationContext(session_id="test123")
    
    context.set_missing_slots(["city", "pincode"])
    assert context.missing_slots == ["city", "pincode"]


def test_clear_missing_slots():
    """Test clearing missing slots"""
    context = ConversationContext(session_id="test123")
    
    context.set_missing_slots(["city", "pincode"])
    context.clear_missing_slots()
    assert context.missing_slots == []

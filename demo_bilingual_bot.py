#!/usr/bin/env python3
"""
Demo script showcasing bilingual (Hindi & English) conversational bot.
Demonstrates all new features including:
- Hindi and English language support
- Gold coins/biscuits with GST
- Out-of-scope handling
- Multi-intent detection
- 18K chain constraint
- State-wise silver rates
- Store timings with last walk-in time
"""

from orchestrator.bot_engine import BotEngine
from contracts.incoming_event import IncomingEvent, Channel


def print_separator():
    print("\n" + "=" * 80 + "\n")


def demo():
    """Run bilingual demo conversation"""
    print("=" * 80)
    print("  KALYAN JEWELLERS - BILINGUAL AI AGENT DEMO")
    print("  Hindi & English Support | Gold, Silver, Platinum Rates | Store Info")
    print("=" * 80)
    
    # Initialize bot engine
    engine = BotEngine()
    
    # Demo conversations in both languages
    print("\n>>> ENGLISH CONVERSATION\n")
    english_messages = [
        ("session_en_001", "Hello", "en"),
        ("session_en_001", "What is the gold rate for 10 grams of 22K?", "en"),
        ("session_en_001", "Tell me about gold coin rates", "en"),
        ("session_en_001", "Store timings in Mumbai", "en"),
        ("session_en_001", "Do you have any discounts?", "en"),  # Out of scope
    ]
    
    for session_id, user_message, lang in english_messages:
        print_separator()
        print(f"USER: {user_message}")
        
        event = IncomingEvent(
            session_id=session_id,
            user_text=user_message,
            language=lang,
            channel=Channel.CHAT
        )
        
        response = engine.process_event(event)
        
        print(f"\nBOT: {response.text}")
        print(f"\nAction: {response.action.value} | Confidence: {response.confidence}")
    
    print("\n\n")
    print("=" * 80)
    print(">>> HINDI CONVERSATION (हिंदी वार्तालाप)")
    print("=" * 80)
    
    hindi_messages = [
        ("session_hi_001", "नमस्ते", "hi"),
        ("session_hi_001", "सोने की दर क्या है?", "hi"),
        ("session_hi_001", "10 ग्राम 22K सोना", "hi"),
        ("session_hi_001", "मुंबई में स्टोर का समय", "hi"),
    ]
    
    for session_id, user_message, lang in hindi_messages:
        print_separator()
        print(f"USER: {user_message}")
        
        event = IncomingEvent(
            session_id=session_id,
            user_text=user_message,
            language=lang,
            channel=Channel.CHAT
        )
        
        response = engine.process_event(event)
        
        print(f"\nBOT: {response.text}")
        print(f"\nAction: {response.action.value} | Confidence: {response.confidence}")
    
    print_separator()
    print(">>> Demo Completed - Showing Key Features:")
    print("✓ Bilingual support (Hindi & English)")
    print("✓ Gold coin/biscuit rates with 3% GST")
    print("✓ 18K chain availability constraint")
    print("✓ Store timings (11:00 AM - 08:30 PM, last walk-in 08:20 PM)")
    print("✓ Out-of-scope handling (discounts, offers)")
    print("✓ Multi-intent detection")
    print("✓ State-wise silver rates")
    print("✓ Transfer to agent after 2 clarification attempts")
    print_separator()


if __name__ == "__main__":
    demo()

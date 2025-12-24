#!/usr/bin/env python3
"""
Simple demo script to showcase the text-based conversational bot.
This demonstrates the complete pipeline working end-to-end.
"""

from orchestrator.bot_engine import BotEngine
from contracts.incoming_event import IncomingEvent, Channel


def print_separator():
    print("\n" + "=" * 70 + "\n")


def demo():
    """Run demo conversation"""
    print("=" * 70)
    print("  TEXT-BASED CONVERSATIONAL BOT - DEMO")
    print("  Gold, Silver, Platinum Rates & Store Information")
    print("=" * 70)
    
    # Initialize bot engine
    engine = BotEngine()
    session_id = "demo_session_001"
    
    # Demo conversations
    test_messages = [
        "Hello",
        "What is the gold rate today?",
        "How much for 10 grams of 22K gold?",
        "What about silver price?",
        "Store timings in Mumbai",
        "Where is your store in Delhi?",
        "random gibberish",
        "more unclear text",
        "I want to talk to an agent"
    ]
    
    print("\n>>> Starting Demo Conversation...\n")
    
    for user_message in test_messages:
        print_separator()
        print(f"USER: {user_message}")
        
        # Create event
        event = IncomingEvent(
            session_id=session_id,
            user_text=user_message,
            language="en",
            channel=Channel.CHAT
        )
        
        # Process event
        response = engine.process_event(event)
        
        # Display response
        print(f"\nBOT: {response.text}")
        print(f"\nAction: {response.action.value}")
        print(f"Confidence: {response.confidence}")
        
        # Stop if transferred to agent
        if response.action.value == "transfer_to_agent":
            print("\n>>> Demo ended - transferred to agent")
            break
    
    print_separator()
    print(">>> Demo Completed")
    print_separator()


if __name__ == "__main__":
    demo()

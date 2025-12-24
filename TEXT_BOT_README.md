# Text-Based Conversational Bot Architecture

## Overview

This is a **text-based conversational bot** designed for handling gold, silver, and platinum rate inquiries, as well as store information queries. The architecture is explicitly designed to process **text only** - no voice, audio, or telephony components.

## Architecture Principles

### IN SCOPE
- Intent detection
- Entity extraction
- Business logic (gold rate, store info, rules)
- Conversation state & flow control
- Structured responses (text + metadata)
- Fallback & escalation decision logic

### OUT OF SCOPE
- ASR / TTS
- Audio streaming
- Telephony providers
- SIP / WebSocket audio
- Voice latency handling

## Architecture Flow

```
incoming_text_event
    ↓
ConversationContext
    ↓
IntentClassifier
    ↓
EntityResolver
    ↓
IntentHandler
    ↓
ResponseBuilder
    ↓
text_response + action_signal
```

## Action Signals

- `CONTINUE` - Continue conversation normally
- `CLARIFY` - Ask for clarification
- `TRANSFER_TO_AGENT` - Transfer to human agent
- `END_CALL` - End conversation

## Directory Structure

```
├── contracts/              # Input/Output contracts
│   ├── incoming_event.py   # Normalized text event format
│   └── outgoing_response.py # Response object with action signals
│
├── conversation/           # Conversation state management
│   └── context.py          # Context tracking and transfer rules
│
├── nlu/                    # Natural Language Understanding
│   ├── intents.py          # Intent enumeration
│   ├── intent_classifier.py # Rule-based intent classification
│   ├── entities.py         # Entity definitions
│   └── entity_resolver.py  # Entity extraction & normalization
│
├── services/               # Business logic services
│   ├── rate_service.py     # Metal rate calculations
│   └── store_service.py    # Store lookup service
│
├── handlers/               # Intent handlers (one per intent)
│   ├── base_handler.py
│   ├── gold_rate_handler.py
│   ├── silver_rate_handler.py
│   ├── platinum_rate_handler.py
│   ├── store_info_handler.py
│   ├── greeting_handler.py
│   └── fallback_handler.py
│
├── orchestrator/           # Orchestration layer
│   └── bot_engine.py       # Main entry point - routes through pipeline
│
├── knowledge/              # Knowledge base
│   └── faqs.json           # FAQ responses
│
└── tests/                  # Comprehensive test suite
    ├── test_nlu_intent_classifier.py
    ├── test_nlu_entity_resolver.py
    ├── test_rate_service.py
    ├── test_store_service.py
    ├── test_conversation_context.py
    └── test_bot_engine.py
```

## Key Components

### 1. Contracts (Phase 1)

**IncomingEvent**: Normalized input format
- `session_id`: Session identifier
- `user_text`: User's text input
- `language`: Language code (default: "en")
- `channel`: VOICE or CHAT (treated identically)
- `metadata`: Additional metadata

**OutgoingResponse**: Bot's response
- `text`: Response text
- `language`: Response language
- `action`: Action signal (CONTINUE, CLARIFY, TRANSFER, END)
- `confidence`: Confidence score
- `context_update`: Context updates

### 2. Conversation Context (Phase 2)

Tracks conversation state across turns:
- Session tracking
- Turn counting
- Clarification attempt tracking
- Missing slot management
- Transfer decision logic

**Transfer Rules**:
- `clarification_attempts >= 2` → TRANSFER
- `turn_count > 20` → TRANSFER

### 3. Intent Classification (Phase 3)

**Supported Intents**:
- `GOLD_RATE` - Gold rate inquiries
- `SILVER_RATE` - Silver rate inquiries
- `PLATINUM_RATE` - Platinum rate inquiries
- `STORE_TIMINGS` - Store hours
- `STORE_ADDRESS` - Store location
- `GREETING` - Greetings
- `FALLBACK` - Unrecognized input
- `TRANSFER_REQUEST` - Explicit agent request

**Classification Logic**:
- Rule-based keyword matching
- Confidence scoring
- Confidence < 0.6 → FALLBACK

### 4. Entity Extraction (Phase 4)

**Entities**:
- `metal_type`: gold, silver, platinum
- `purity`: 24K, 22K, 18K, 916 (auto-converted to 22K)
- `weight`: Weight in grams (default: 1.0)
- `city`: City name
- `pincode`: 6-digit pincode

**Rules**:
- 916 → 22K conversion
- Default weight = 1 gram
- No AI hallucination - rule-based only

### 5. Business Logic Services (Phase 5)

**RateService**:
- Calculates rates for gold, silver, platinum
- Purity conversion (24K → 22K, 18K)
- Weight multiplication
- Formatted response generation

**StoreService**:
- Store lookup by city or pincode
- Nearest store logic
- Store timings and address formatting

### 6. Intent Handlers (Phase 6)

Each handler:
- Checks for missing entities
- Requests clarification if needed
- Executes business logic
- Returns structured response

### 7. Orchestration (Phase 7)

**BotEngine** - Single entry point:
1. Build/update context
2. Classify intent
3. Resolve entities
4. Select handler
5. Build response
6. Apply transfer rules

## Usage Example

```python
from orchestrator.bot_engine import BotEngine
from contracts.incoming_event import IncomingEvent, Channel

# Initialize engine
engine = BotEngine()

# Create event
event = IncomingEvent(
    session_id="user123",
    user_text="What is the gold rate today?",
    language="en",
    channel=Channel.CHAT
)

# Process
response = engine.process_event(event)

print(response.text)
print(f"Action: {response.action.value}")
```

## Demo

Run the demo script to see the bot in action:

```bash
python demo_bot.py
```

## Testing

Run the comprehensive test suite:

```bash
pytest tests/test_nlu_intent_classifier.py
pytest tests/test_nlu_entity_resolver.py
pytest tests/test_rate_service.py
pytest tests/test_store_service.py
pytest tests/test_conversation_context.py
pytest tests/test_bot_engine.py
```

All 53 tests pass successfully.

## Configuration

**Base Rates** (configurable):
- Gold (24K): ₹6,500/gram
- Silver: ₹85/gram
- Platinum: ₹3,200/gram

**Stores** (configurable):
- Mumbai: 400001
- Delhi: 110001
- Bangalore: 560001

## Design Principles

1. **Stateless API** - Context passed explicitly
2. **No Magic** - Explicit rules, no hidden logic
3. **Deterministic** - Rule-based, predictable behavior
4. **Channel Agnostic** - Voice and chat treated identically
5. **Testable** - Comprehensive test coverage
6. **Extensible** - Easy to add new intents and handlers

## Extension Guide

### Adding a New Intent

1. Add intent to `nlu/intents.py`
2. Add keywords to `nlu/intent_classifier.py`
3. Create handler in `handlers/new_intent_handler.py`
4. Register handler in `orchestrator/bot_engine.py`
5. Add tests in `tests/test_new_intent.py`

### Adding a New Entity

1. Add entity to `nlu/entities.py`
2. Add extraction logic to `nlu/entity_resolver.py`
3. Update handlers to use new entity
4. Add tests

## Notes

- This is a **TEXT BRAIN** only - no voice/audio code
- All voice/audio handling should be done in separate components
- The bot is designed to be invoked by external systems (API, chat platforms, etc.)
- Context is stored in-memory; can be replaced with Redis/DB for production

from enum import Enum


class Intent(Enum):
    """Supported intents for the conversational bot"""
    GOLD_RATE = "gold_rate"
    SILVER_RATE = "silver_rate"
    PLATINUM_RATE = "platinum_rate"
    GOLD_COIN_RATE = "gold_coin_rate"
    GOLD_BISCUIT_RATE = "gold_biscuit_rate"
    STORE_TIMINGS = "store_timings"
    STORE_ADDRESS = "store_address"
    GREETING = "greeting"
    FALLBACK = "fallback"
    TRANSFER_REQUEST = "transfer_request"
    OUT_OF_SCOPE = "out_of_scope"  # For discounts, offers, future predictions
    MULTI_INTENT = "multi_intent"  # For handling multiple queries together

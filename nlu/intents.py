from enum import Enum


class Intent(Enum):
    """Supported intents for the conversational bot"""
    GOLD_RATE = "gold_rate"
    SILVER_RATE = "silver_rate"
    PLATINUM_RATE = "platinum_rate"
    STORE_TIMINGS = "store_timings"
    STORE_ADDRESS = "store_address"
    GREETING = "greeting"
    FALLBACK = "fallback"
    TRANSFER_REQUEST = "transfer_request"

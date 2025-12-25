from dataclasses import dataclass, field
from enum import Enum


class ActionSignal(Enum):
    """Action signals that determine conversation flow"""
    CONTINUE = "continue"
    CLARIFY = "clarify"
    TRANSFER_TO_AGENT = "transfer_to_agent"
    END_CALL = "end_call"


@dataclass
class OutgoingResponse:
    """
    Response object returned by the bot.
    Contains text response and action signals for conversation management.
    """
    text: str
    language: str = "en"
    action: ActionSignal = ActionSignal.CONTINUE
    confidence: float = 1.0
    context_update: dict = field(default_factory=dict)

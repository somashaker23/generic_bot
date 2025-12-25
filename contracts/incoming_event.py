from dataclasses import dataclass, field
from enum import Enum


class Channel(Enum):
    """Channel through which the message was received"""
    VOICE = "voice"
    CHAT = "chat"


@dataclass
class IncomingEvent:
    """
    Normalized incoming text event format.
    This is channel-agnostic - voice and chat are identical to the brain.
    """
    session_id: str
    user_text: str
    language: str = "en"
    channel: Channel = Channel.CHAT
    metadata: dict = field(default_factory=dict)

from dataclasses import dataclass, field
from typing import Optional
from contracts.incoming_event import IncomingEvent


@dataclass
class ConversationContext:
    """
    Tracks conversation state across turns.
    Stateless API + explicit context object pattern.
    """
    session_id: str
    language: str = "en"
    last_intent: Optional[str] = None
    missing_slots: list = field(default_factory=list)
    turn_count: int = 0
    clarification_attempts: int = 0
    
    # Maximum thresholds for transfer
    MAX_CLARIFICATION_ATTEMPTS = 2
    MAX_TURN_COUNT = 20
    
    def update_from_event(self, event: IncomingEvent) -> None:
        """Update context from incoming event"""
        self.session_id = event.session_id
        self.language = event.language
        self.turn_count += 1
    
    def mark_clarification(self) -> None:
        """Increment clarification attempt counter"""
        self.clarification_attempts += 1
    
    def should_transfer(self) -> bool:
        """
        Determine if conversation should be transferred to agent.
        Rules:
        - clarification_attempts >= 2 → TRANSFER
        - turn_count > MAX_TURN_COUNT → TRANSFER
        """
        return (
            self.clarification_attempts >= self.MAX_CLARIFICATION_ATTEMPTS
            or self.turn_count > self.MAX_TURN_COUNT
        )
    
    def set_missing_slots(self, slots: list) -> None:
        """Update missing slots that need to be filled"""
        self.missing_slots = slots
    
    def clear_missing_slots(self) -> None:
        """Clear missing slots once all are filled"""
        self.missing_slots = []

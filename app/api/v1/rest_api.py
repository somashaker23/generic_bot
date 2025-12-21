from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.repositories.deps import get_whatsapp_repository
from app.repositories.whatsapp_repository import WhatsAppRepository
from app.services.conversation_flow import ConversationFlow

router = APIRouter()
flow = ConversationFlow()


class LLMRequest(BaseModel):
    google_user_id: str
    text: str
    email: Optional[str] = None
    name: Optional[str] = None


@router.post("/chat")
async def chat_endpoint(
        payload: LLMRequest,
        db: Session = Depends(get_db),
        repo: WhatsAppRepository = Depends(get_whatsapp_repository),
):
    user_id = payload.google_user_id
    message = payload.text

    if not user_id or not message:
        raise HTTPException(status_code=400, detail="Missing user or message")

    # Log incoming
    # repo.log(db, user_id, message, direction="incoming")

    # Run conversation flow
    result = flow.handle_message(
        user_id=user_id,
        text=message,
    )

    reply = result.get("reply", "")

    # Log outgoing
    # repo.log(db, user_id, reply, direction="outgoing")

    return {"reply": reply}

from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.connector.whatsapp_connector import WhatsAppConnector
from app.db.deps import get_db
from app.repositories.deps import get_whatsapp_repository
from app.repositories.whatsapp_repository import WhatsAppRepository
from app.services.conversation_flow import ConversationFlow
from app.services.knowledge_engine import KnowledgeEngine
from app.services import intent_router

router = APIRouter()
connector = WhatsAppConnector()
knowledge_engine = KnowledgeEngine()
flow = ConversationFlow()


@router.post("/whatsapp")
async def whatsapp_webhook(
        request: Request,
        db: Session = Depends(get_db),
        whatsapp_repo: WhatsAppRepository = Depends(get_whatsapp_repository),
):
    payload = await request.json()

    if not connector.validate(request):
        raise HTTPException(status_code=400, detail="Invalid request signature")

    parsed = connector.parse_incoming(payload)
    user_id = parsed["user_id"]
    message = parsed["message"]

    if not user_id or not message:
        raise HTTPException(status_code=400, detail="Missing fields")

    # Log incoming
    whatsapp_repo.log(db, user_id, message, direction="incoming")
    faq_reply = knowledge_engine.search(message)

    if faq_reply:
        connector.send_message(user_id, faq_reply)
        whatsapp_repo.log(db, user_id, faq_reply, direction="outgoing")
        return {"status": "ok", "type": "faq"}

    result = flow.process(user_id, message)
    reply = result["reply"]

    # Auto-reply fall back
    connector.send_message(user_id, reply)

    # Log outgoing
    whatsapp_repo.log(db, user_id, reply, direction="outgoing")

    return {"status": "ok"}


@router.get("/webhook")
def verify_webhook(request: Request):
    return connector.verify_webhook(request.query_params, settings.VERIFY_TOKEN)

from fastapi import APIRouter, Request, HTTPException

from app.connector.whatsapp_connector import WhatsAppConnector
from app.repositories.whatsapp_repository import WhatsAppRepository
from app.db.session import SessionLocal
from config import settings

router = APIRouter()
connector = WhatsAppConnector()


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    payload = await request.json()

    if not connector.validate(request):
        raise HTTPException(status_code=400, detail="Invalid request signature")

    parsed = connector.parse_incoming(payload)
    user_id = parsed["user_id"]
    message = parsed["message"]

    if not user_id or not message:
        raise HTTPException(status_code=400, detail="Missing fields")

    db = SessionLocal()
    WhatsAppRepository().log(db, user_id, message, direction="incoming")

    # Auto-reply (or call flow engine later)
    connector.send_message(user_id, "Message received")

    WhatsAppRepository().log(db, user_id, "Message received", direction="outgoing")

    return {"status": "ok"}


@router.get("/webhook")
def verify_webhook(request: Request):
    connector.verify_webhook(request, settings.VERIFY_TOKEN)

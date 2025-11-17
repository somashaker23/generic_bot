from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.connector.whatsapp_connector import WhatsAppConnector
from app.db.deps import get_db
from app.repositories.deps import get_whatsapp_repository
from repositories.whatsapp_repository import WhatsAppRepository

router = APIRouter()
connector = WhatsAppConnector()


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

    # Auto-reply
    connector.send_message(user_id, "Message received")

    # Log outgoing
    whatsapp_repo.log(db, user_id, "Message received", direction="outgoing")

    return {"status": "ok"}



@router.get("/webhook")
def verify_webhook(request: Request):
    return connector.verify_webhook(request.query_params, settings.VERIFY_TOKEN)

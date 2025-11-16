from sqlalchemy.orm import Session
from app.models.whatsapp_log import WhatsAppLog


class WhatsAppRepository:

    def log(self, db: Session, user_id: str, message: str, direction: str):
        obj = WhatsAppLog(user_id=user_id, message=message, direction=direction)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

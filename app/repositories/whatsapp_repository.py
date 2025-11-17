from sqlalchemy.orm import Session


class WhatsAppRepository:

    @staticmethod
    def log(db: Session, user_id: str, message: str, direction: str):
        from app.models.whatsapp_log import WhatsAppLog

        obj = WhatsAppLog(user_id=user_id, message=message, direction=direction)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

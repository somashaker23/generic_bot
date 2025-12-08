from app.models.callback_request import CallbackRequest


class CallbackAction:
    def run(self, context, db):
        name = context.get("name")
        phone = context.get("phone")
        if not name or not phone:
            raise ValueError("Required fields 'name' and 'phone' are missing")

        record = CallbackRequest(
            name=context.get("name"),
            phone=context.get("phone"),
            reason=context.get("reason"),
            preferred_time=context.get("preferred_time"),
            status="pending",
            notes=context.get("notes")
        )

        try:
            db.add(record)
            db.commit()
            db.refresh(record)
            return record
        except Exception as e:
            db.rollback()
            raise

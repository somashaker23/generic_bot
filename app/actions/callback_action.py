from app.models.callback_request import CallbackRequest


class CallbackAction:
    def run(self, context, db):
        record = CallbackRequest(
            name=context.get("name"),
            phone=context.get("phone"),
            reason=context.get("reason"),
            preferred_time=context.get("preferred_time"),
            status="pending",
            notes=context.get("notes")
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        return record

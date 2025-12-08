from app.models.test_drive_booking import TestDriveBooking


class TestDriveAction:
    def run(self, context, db):

        record = TestDriveBooking(
            user_id=context.get("user_id"),
            car=context.get("model")
        )

        try:
            db.add(record)
            db.commit()
            db.refresh(record)
            return record
        except Exception as e:
            db.rollback()
            raise
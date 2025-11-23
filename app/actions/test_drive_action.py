from app.models.test_drive_booking import TestDriveBooking


class TestDriveAction:
    def run(self, context, db):
        print(context)
        record = TestDriveBooking(
            user_id=context.get("user_id"),
            car=context.get("model")
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        return record

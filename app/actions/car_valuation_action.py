from app.models.car_valuation import CarValuation


class CarValuationAction:
    def run(self, context, db):
        record = CarValuation(
            user_id=context.get("user_id"),
            name=context.get("name"),
            phone=context.get("phone"),

            brand=context.get("brand"),
            model=context.get("model"),
            year=context.get("year"),
            fuel_type=context.get("fuel_type"),
            owner=context.get("owner"),
            condition=context.get("condition"),
            location=context.get("location"),

            estimated_value=context.get("estimated_value")
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        return record

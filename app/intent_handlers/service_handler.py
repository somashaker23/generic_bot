class ServiceHandler:

    def handle(self, data: dict):
        model = data["model"]
        date = data["date"]

        if not model:
            return "Sure, which vehicle model do you want to book service for?"

        if not date:
            return f"When would you like to schedule service for your {model}?"

        return f"Your {model} service request is noted for {date}. Our service advisor will follow up."

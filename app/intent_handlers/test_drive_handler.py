class TestDriveHandler:

    def handle(self, data: dict):
        model = data["model"]
        date = data["date"]

        if not model:
            return "Sure! Which car model would you like to test drive?"

        if not date:
            return f"Got it. When would you like to schedule your {model} test drive?"

        return f"Your {model} test drive is noted for {date}. Our team will contact you shortly."

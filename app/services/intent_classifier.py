import re


class IntentClassifier:

    @staticmethod
    def classify(text: str):
        text = text.lower()

        # --- Test Drive Intent ---
        test_drive_keywords = [
            "test drive", "book test drive", "schedule test drive",
            "testdrive", "drive booking"
        ]
        if any(k in text for k in test_drive_keywords):
            return "book_test_drive"

        # --- Service Intent ---
        service_keywords = [
            "service", "book service", "schedule service",
            "car service", "vehicle service"
        ]
        if any(k in text for k in service_keywords):
            return "book_service"

        # --- Price inquiry ---
        price_keywords = [
            "price", "cost", "how much", "rate", "on road", "ex showroom"
        ]
        if any(k in text for k in price_keywords):
            return "price_inquiry"

        # --- Greeting (optional) ---
        if any(k in text for k in ["hello", "hi", "hey"]):
            return "greeting"

        # fallback
        return "unknown"

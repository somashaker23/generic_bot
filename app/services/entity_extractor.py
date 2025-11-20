import re


class EntityExtractor:

    def __init__(self):
        # Later load from DB
        self.models = [
            "creta", "venue", "i20", "i10", "verna", "alcazar", "exter"
        ]

    def extract_model(self, text: str):
        text = text.lower()
        for model in self.models:
            if model in text:
                return model.capitalize()
        return None

    def extract_date(self, text: str):
        text = text.lower()

        # Simple natural language
        if "today" in text:
            return "today"
        if "tomorrow" in text or "tmrw" in text:
            return "tomorrow"

        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for d in days:
            if d in text:
                return d.capitalize()

        # dd/mm or dd-mm
        m = re.search(r"\b(\d{1,2}[/-]\d{1,2})\b", text)
        if m:
            return m.group(1)

        return None

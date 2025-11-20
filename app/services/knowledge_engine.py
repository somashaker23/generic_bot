import json
import os


class KnowledgeEngine:

    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(os.path.dirname(os.path.dirname(base_path)), "knowledge/faq_knowledge.json")
        try:
            with open(path, "r") as f:
                self.faq_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"FAQ knowledge file not found at {path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in FAQ knowledge file: {e}")

    def search(self, text: str):
        if not text:
            return None
        text = text.lower()

        for item in self.faq_data:
            patterns = item.get("patterns", [])
            response = item.get("response")
            if not patterns or not response:
                continue
            for pattern in patterns:
                if pattern in text:
                    return response

        return None

# TODO: Implement advanced search logic (e.g., fuzzy matching, NLP techniques)
# If needed we can add:
#
# Fuzzy matching (difflib)
#
# Embedding search
#
# Keyword index

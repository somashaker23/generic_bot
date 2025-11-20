import json
import os


class KnowledgeEngine:

    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(os.path.dirname(base_path), "../knowledge/faq_knowledge.json")
        with open(path, "r") as f:
            self.faq_data = json.load(f)

    def search(self, text: str):
        text = text.lower()

        for item in self.faq_data:
            for pattern in item["patterns"]:
                if pattern in text:
                    return item["response"]

        return None

# TODO: Implement advanced search logic (e.g., fuzzy matching, NLP techniques)
# If needed we can add:
#
# Fuzzy matching (difflib)
#
# Embedding search
#
# Keyword index

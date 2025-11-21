from typing import Optional


class IntentRefiner:

    def missing_info(self, intent: str, ctx: dict)-> Optional[str]:
        if intent == "book_test_drive":
            if not ctx.get("model"):
                return "Sure! Which car model would you like to test drive?"

            if not ctx.get("date"):
                return f"Great. When would you like the test drive for {ctx['model']}?"

        if intent == "book_service":
            if not ctx.get("model"):
                return "Got it. Which car model do you want to service?"

            if not ctx.get("date"):
                return f"When would you like to schedule service for your {ctx['model']}?"

        if intent == "price_inquiry":
            if not ctx.get("model"):
                return "Which model's price would you like to know?"

        return None

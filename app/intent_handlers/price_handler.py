class PriceHandler:

    def handle(self, data: dict):
        model = data["model"]

        if not model:
            return "Which model's price would you like to know?"

        # Later: fetch model price from DB
        return f"The on-road price for {model} starts at approximately ₹9,00,000. For exact pricing, please tell your variant."

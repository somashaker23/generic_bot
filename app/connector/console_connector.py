from app.connector.base_connector import BaseConnector


class ConsoleConnector(BaseConnector):

    def validate(self, request):
        return True  # nothing to validate

    def parse_incoming(self, text: str):
        return {
            "user_id": "console_user",
            "message": text
        }

    def send_message(self, to: str, message: str):
        print(f"\nBOT: {message}\n")
        return True

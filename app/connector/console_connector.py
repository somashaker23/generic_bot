from app.connector.base_connector import BaseConnector


class ConsoleConnector(BaseConnector):
    """
      Implements a console-based communication channel for testing and development purposes.
      This connector allows interaction with the bot via the console, simulating user input and bot responses.
      """

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

    def verify_webhook(self, query_params, verify_token):
        # No webhook verification needed for console, but method required by BaseConnector
        return True

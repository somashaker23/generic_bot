import logging
from fastapi.responses import PlainTextResponse

from app.connector.base_connector import BaseConnector
from app.clients.whatsapp_client import WhatsAppClient


class WhatsAppConnector(BaseConnector):

    def validate(self, request):
        return True

    def parse_incoming(self, payload):
        return {
            "user_id": payload.get("from"),
            "message": payload.get("text", {}).get("body") or payload.get("interactive", {}).get("list_reply", {}).get(
                "title") or payload.get("interactive", {}).get("button_reply", {}).get("title")
        }

    def send_message(self, to, message):
        try:
            return WhatsAppClient().send_message(to, message)
        except Exception as e:
            logging.error(f"Error sending message to {to}: {str(e)}")
            return {"status": "failure", "message": str(e)}

    def verify_webhook(self, query_params, verify_token):
        mode = query_params.get("hub.mode")
        token = query_params.get("hub.verify_token")
        challenge = query_params.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return PlainTextResponse(challenge)

        return PlainTextResponse("Forbidden", status_code=403)

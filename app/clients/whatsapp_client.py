import requests
from app.config import settings


class WhatsAppClient:

    def __init__(self):
        self.phone_number = settings.WHATSAPP_PHONE_NUMBER
        self.base_url = settings.WHATSAPP_API_URL
        self.token = settings.WHATSAPP_API_TOKEN

    def send_message(self, to: str, message: str):
        url = f"{self.base_url}/${self.phone_number}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": to,
            "text": message
        }
        r = requests.post(url, json=payload, headers=headers)
        return r.status_code, r.text

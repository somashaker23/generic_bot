class BaseConnector:
    def parse_incoming(self, payload):
        raise NotImplementedError

    def validate(self, request):
        raise NotImplementedError

    def send_message(self, to, message):
        raise NotImplementedError

    def verify_webhook(self, query_params, verify_token):
        raise NotImplementedError

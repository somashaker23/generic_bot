import json
import redis
from app.config import settings


# Context examples:
# {
#   "intent": "book_test_drive",
#   "model": "Creta",
#   "date": null,
#   "stage": "awaiting_date"
# }


class ContextManager:

    def __init__(self):
        self.r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )

    def get(self, user_id: str):
        data = self.r.get(f"ctx:{user_id}")
        return json.loads(data) if data else {}

    def save(self, user_id: str, context: dict, ttl=900):
        self.r.set(
            f"ctx:{user_id}",
            json.dumps(context),
            ex=ttl  # 15 min default TTL
        )

    def update(self, user_id: str, key: str, value, ttl=900):
        ctx = self.get(user_id)
        ctx[key] = value
        self.save(user_id, ctx, ttl)

    def clear(self, user_id: str):
        self.r.delete(f"ctx:{user_id}")

from unittest.mock import patch, MagicMock

from app.services.conversation_flow import ConversationFlow


def test_multi_turn_test_drive():
    with patch("app.services.conversation_flow.ContextManager") as MockContextManager:
        # Set up a mock context manager instance with in-memory storage
        mock_instance = MagicMock()
        # Simulate get_context and set_context with a simple dict
        context_store = {}

        def get_context(user_id):
            return context_store.get(user_id, {})

        def set_context(user_id, context):
            context_store[user_id] = context

        mock_instance.get_context.side_effect = get_context
        mock_instance.set_context.side_effect = set_context
        MockContextManager.return_value = mock_instance

        bot = ConversationFlow()
        user = "u1"

        r1 = bot.process(user, "I want to book a test drive")
        assert "Which car model" in r1["reply"]

        r2 = bot.process(user, "Creta")
        assert "When would you like" in r2["reply"]

        r3 = bot.process(user, "tomorrow")
        assert "Your Creta test drive is scheduled for tomorrow" in r3["reply"]

from app.services.conversation_flow import ConversationFlow


def test_offtopic_response():
    bot = ConversationFlow()
    r = bot.process("u1", "idly sambar")
    assert "Haha!" in r["reply"]

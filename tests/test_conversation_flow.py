from app.services.conversation_flow import ConversationFlow

def test_multi_turn_test_drive():
    bot = ConversationFlow()
    user = "u1"

    r1 = bot.process(user, "I want to book a test drive")
    assert "Which car model" in r1["reply"]

    r2 = bot.process(user, "Creta")
    assert "When would you like" in r2["reply"]

    r3 = bot.process(user, "tomorrow")
    assert "Your Creta test drive is scheduled for tomorrow" in r3["reply"]

from app.services.conversation_flow import ConversationFlow

def test_end_to_end_test_drive_flow():
    bot = ConversationFlow()
    user = "u1"

    r1 = bot.handle_message(user, "I want a test drive")
    assert "which" in r1["reply"].lower()

    r2 = bot.handle_message(user, "creta")
    assert "when" in r2["reply"].lower()

    r3 = bot.handle_message(user, "tomorrow")
    assert "scheduled" in r3["reply"].lower()
    assert "creta" in r3["reply"].lower()


def test_faq_flow():
    bot = ConversationFlow()
    r = bot.handle_message("u1", "what are your showroom hours?")
    assert "open" in r["reply"].lower()


def test_humor_flow():
    bot = ConversationFlow()
    r = bot.handle_message("u1", "lol 😂😂")
    assert "haha" in r["reply"].lower() or "😂" in r["reply"]


def test_price_inquiry():
    bot = ConversationFlow()
    r = bot.handle_message("u1", "price of venue")
    assert "price" in r["reply"].lower()


def test_offtopic():
    bot = ConversationFlow()
    r = bot.handle_message("u1", "idly dosa sambar")
    assert "smile" in r["reply"].lower()

from app.services.message_sanitizer import MessageSanitizer

def test_strip_noise():
    s = MessageSanitizer()
    assert s.strip_noise("lol bro creta 😂😂") == "creta"

def test_off_topic():
    s = MessageSanitizer()
    assert s.is_totally_off_topic("idly sambar is great")

def test_joke():
    s = MessageSanitizer()
    assert s.is_joke("lol that was funny 😂")

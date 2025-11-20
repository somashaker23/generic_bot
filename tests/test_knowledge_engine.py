from app.services.knowledge_engine import KnowledgeEngine


def test_faq_match():
    engine = KnowledgeEngine()
    result = engine.search("What are your store hours?")
    assert result == "Our showroom is open from 9 AM to 8 PM, Monday to Sunday."


def test_faq_case_insensitive():
    engine = KnowledgeEngine()
    result = engine.search("STORE HOURS")
    assert result is not None

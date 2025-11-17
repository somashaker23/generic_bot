from app.services.knowledge_engine import KnowledgeEngine


def test_faq_match():
    engine = KnowledgeEngine()
    assert engine.search("What are your store hours?") is not None


def test_no_match():
    engine = KnowledgeEngine()
    assert engine.search("This is random text") is None

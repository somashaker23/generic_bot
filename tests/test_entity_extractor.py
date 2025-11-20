from app.services.entity_extractor import EntityExtractor


def test_model_extraction():
    e = EntityExtractor()
    assert e.extract_model("I want Creta test drive") == "Creta"


def test_date_extraction():
    e = EntityExtractor()
    assert e.extract_date("test drive tomorrow") == "tomorrow"


def test_day_extraction():
    e = EntityExtractor()
    assert e.extract_date("book service on Monday") == "Monday"

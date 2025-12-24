import pytest
from services.store_service import StoreService


def test_get_store_by_city():
    """Test getting store by city"""
    service = StoreService()
    
    store = service.get_store_by_city("Mumbai")
    assert store is not None
    assert store["city"] == "Mumbai"
    assert "address" in store
    assert "timings" in store


def test_get_store_by_city_case_insensitive():
    """Test city lookup is case insensitive"""
    service = StoreService()
    
    store = service.get_store_by_city("mumbai")
    assert store is not None
    assert store["city"] == "Mumbai"


def test_get_store_by_pincode():
    """Test getting store by pincode"""
    service = StoreService()
    
    store = service.get_store_by_pincode("400001")
    assert store is not None
    assert store["pincode"] == "400001"
    assert store["city"] == "Mumbai"


def test_get_nearest_store_by_city():
    """Test getting nearest store by city"""
    service = StoreService()
    
    store = service.get_nearest_store(city="Delhi")
    assert store is not None
    assert store["city"] == "Delhi"


def test_get_nearest_store_by_pincode():
    """Test getting nearest store by pincode"""
    service = StoreService()
    
    store = service.get_nearest_store(pincode="560001")
    assert store is not None
    assert store["city"] == "Bangalore"


def test_get_nearest_store_city_priority():
    """Test that city has priority over pincode"""
    service = StoreService()
    
    # Provide both city and pincode from different stores
    store = service.get_nearest_store(city="Mumbai", pincode="110001")
    assert store["city"] == "Mumbai"  # City should take priority


def test_get_nearest_store_default():
    """Test default store when nothing matches"""
    service = StoreService()
    
    store = service.get_nearest_store(city="Unknown", pincode="999999")
    assert store is not None  # Should return first store as default


def test_format_store_timings():
    """Test formatting store timings"""
    service = StoreService()
    store = service.get_store_by_city("Mumbai")
    
    formatted = service.format_store_timings(store)
    assert "Store Timings" in formatted
    assert store["timings"] in formatted
    assert "Mumbai" in formatted


def test_format_store_address():
    """Test formatting store address"""
    service = StoreService()
    store = service.get_store_by_city("Mumbai")
    
    formatted = service.format_store_address(store)
    assert "Store Address" in formatted
    assert store["address"] in formatted
    assert store["phone"] in formatted

import pytest
from services.rate_service import RateService
from nlu.entities import Purity


def test_gold_24k_rate_calculation():
    """Test 24K gold rate calculation"""
    service = RateService({"gold": 6000, "silver": 80, "platinum": 3000})
    
    total, formatted = service.calculate_rate("gold", Purity.GOLD_24K, 1.0)
    
    assert total == 6000.0
    assert "6000.00" in formatted
    assert "Gold" in formatted


def test_gold_22k_rate_calculation():
    """Test 22K gold rate calculation"""
    service = RateService({"gold": 6000, "silver": 80, "platinum": 3000})
    
    total, formatted = service.calculate_rate("gold", Purity.GOLD_22K, 1.0)
    
    # 22K is 22/24 of 24K rate
    expected = 6000 * (22.0 / 24.0)
    assert abs(total - expected) < 0.01
    assert "22K" in formatted


def test_gold_18k_rate_calculation():
    """Test 18K gold rate calculation"""
    service = RateService({"gold": 6000, "silver": 80, "platinum": 3000})
    
    total, formatted = service.calculate_rate("gold", Purity.GOLD_18K, 1.0)
    
    # 18K is 18/24 of 24K rate
    expected = 6000 * (18.0 / 24.0)
    assert abs(total - expected) < 0.01
    assert "18K" in formatted


def test_weight_multiplication():
    """Test weight multiplication in rate calculation"""
    service = RateService({"gold": 6000, "silver": 80, "platinum": 3000})
    
    total, formatted = service.calculate_rate("gold", Purity.GOLD_24K, 10.0)
    
    assert total == 60000.0
    assert "10" in formatted
    assert "60000" in formatted


def test_silver_rate_calculation():
    """Test silver rate calculation"""
    service = RateService({"gold": 6000, "silver": 80, "platinum": 3000})
    
    total, formatted = service.calculate_rate("silver", weight=1.0)
    
    assert total == 80.0
    assert "Silver" in formatted
    assert "80.00" in formatted


def test_platinum_rate_calculation():
    """Test platinum rate calculation"""
    service = RateService({"gold": 6000, "silver": 80, "platinum": 3000})
    
    total, formatted = service.calculate_rate("platinum", weight=1.0)
    
    assert total == 3000.0
    assert "Platinum" in formatted


def test_get_base_rate():
    """Test getting base rate"""
    service = RateService({"gold": 6000, "silver": 80, "platinum": 3000})
    
    assert service.get_base_rate("gold") == 6000
    assert service.get_base_rate("silver") == 80
    assert service.get_base_rate("platinum") == 3000


def test_update_base_rate():
    """Test updating base rate"""
    service = RateService({"gold": 6000})
    
    service.update_base_rate("gold", 6500)
    assert service.get_base_rate("gold") == 6500

import pytest
from nlu.entity_resolver import EntityResolver
from nlu.entities import MetalType, Purity


def test_extract_gold_metal_type():
    """Test gold metal type extraction"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("What is the gold rate?")
    assert entities.metal_type == MetalType.GOLD


def test_extract_silver_metal_type():
    """Test silver metal type extraction"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("silver price today")
    assert entities.metal_type == MetalType.SILVER


def test_extract_platinum_metal_type():
    """Test platinum metal type extraction"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("platinum rate per gram")
    assert entities.metal_type == MetalType.PLATINUM


def test_extract_24k_purity():
    """Test 24K purity extraction"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("24k gold rate")
    assert entities.purity == Purity.GOLD_24K


def test_extract_22k_purity():
    """Test 22K purity extraction"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("22k gold price")
    assert entities.purity == Purity.GOLD_22K


def test_extract_916_to_22k():
    """Test 916 to 22K conversion"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("916 gold rate")
    assert entities.purity == Purity.GOLD_22K  # Should be converted


def test_extract_weight():
    """Test weight extraction"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("gold rate for 10 grams")
    assert entities.weight == 10.0
    
    entities = resolver.resolve("5g silver")
    assert entities.weight == 5.0


def test_default_weight():
    """Test default weight is 1 gram"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("gold rate")
    assert entities.weight == 1.0


def test_extract_city():
    """Test city extraction"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("store in Mumbai")
    assert entities.city == "Mumbai"
    
    entities = resolver.resolve("bangalore store address")
    assert entities.city == "Bangalore"


def test_extract_pincode():
    """Test pincode extraction"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("store near 400001")
    assert entities.pincode == "400001"
    
    entities = resolver.resolve("560001 pincode")
    assert entities.pincode == "560001"


def test_no_entities():
    """Test when no entities are found"""
    resolver = EntityResolver()
    
    entities = resolver.resolve("hello there")
    assert entities.metal_type is None
    assert entities.purity is None
    assert entities.weight == 1.0  # Default
    assert entities.city is None
    assert entities.pincode is None

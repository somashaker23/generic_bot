from dataclasses import dataclass
from typing import Optional
from enum import Enum


class MetalType(Enum):
    """Supported metal types"""
    GOLD = "gold"
    SILVER = "silver"
    PLATINUM = "platinum"


class Purity(Enum):
    """Supported purity levels for metals"""
    GOLD_24K = "24K"
    GOLD_22K = "22K"
    GOLD_18K = "18K"
    GOLD_916 = "916"  # Will be converted to 22K
    SILVER_999 = "999"
    PLATINUM_950 = "950"


@dataclass
class ExtractedEntities:
    """Container for extracted entities"""
    metal_type: Optional[MetalType] = None
    purity: Optional[Purity] = None
    weight: float = 1.0  # Default weight in grams
    city: Optional[str] = None
    pincode: Optional[str] = None

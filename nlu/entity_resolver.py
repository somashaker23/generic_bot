import re
from typing import Optional
from nlu.entities import ExtractedEntities, MetalType, Purity


class EntityResolver:
    """
    Resolve entities from free text into structured slots.
    No AI hallucination - rule-based extraction only.
    """
    
    def __init__(self):
        # City patterns (can be extended)
        self.cities = [
            "mumbai", "delhi", "bangalore", "chennai", "kolkata",
            "hyderabad", "pune", "ahmedabad", "jaipur", "surat"
        ]
    
    def resolve(self, text: str) -> ExtractedEntities:
        """
        Extract and normalize entities from text.
        
        Rules:
        - 916 → 22K
        - default weight = 1 gram
        - missing city → returns None (triggers clarification)
        """
        entities = ExtractedEntities()
        text_lower = text.lower()
        
        # Extract metal type
        entities.metal_type = self._extract_metal_type(text_lower)
        
        # Extract purity
        entities.purity = self._extract_purity(text_lower)
        
        # Normalize 916 to 22K
        if entities.purity == Purity.GOLD_916:
            entities.purity = Purity.GOLD_22K
        
        # Extract weight (default 1 gram)
        entities.weight = self._extract_weight(text_lower)
        
        # Extract city
        entities.city = self._extract_city(text_lower)
        
        # Extract pincode
        entities.pincode = self._extract_pincode(text)
        
        return entities
    
    def _extract_metal_type(self, text: str) -> Optional[MetalType]:
        """Extract metal type from text"""
        if "gold" in text:
            return MetalType.GOLD
        elif "silver" in text:
            return MetalType.SILVER
        elif "platinum" in text:
            return MetalType.PLATINUM
        return None
    
    def _extract_purity(self, text: str) -> Optional[Purity]:
        """Extract purity level from text"""
        # Check for specific purity mentions
        if "24k" in text or "24 k" in text or "24 carat" in text:
            return Purity.GOLD_24K
        elif "22k" in text or "22 k" in text or "22 carat" in text:
            return Purity.GOLD_22K
        elif "18k" in text or "18 k" in text or "18 carat" in text:
            return Purity.GOLD_18K
        elif "916" in text:
            return Purity.GOLD_916
        elif "999" in text:
            return Purity.SILVER_999
        elif "950" in text:
            return Purity.PLATINUM_950
        return None
    
    def _extract_weight(self, text: str) -> float:
        """
        Extract weight from text.
        Default is 1 gram if not specified.
        """
        # Look for patterns like "10 gram", "10g", "10 grams"
        weight_match = re.search(r'(\d+\.?\d*)\s*(?:gram|grams|g|gm)\b', text)
        if weight_match:
            try:
                return float(weight_match.group(1))
            except ValueError:
                pass
        
        # Default weight
        return 1.0
    
    def _extract_city(self, text: str) -> Optional[str]:
        """Extract city name from text"""
        for city in self.cities:
            if city in text:
                return city.title()
        return None
    
    def _extract_pincode(self, text: str) -> Optional[str]:
        """Extract pincode from text (6-digit Indian pincode)"""
        pincode_match = re.search(r'\b(\d{6})\b', text)
        if pincode_match:
            return pincode_match.group(1)
        return None

import re
from typing import Optional
from nlu.entities import ExtractedEntities, MetalType, Purity, ProductType, Region


class EntityResolver:
    """
    Resolve entities from free text into structured slots.
    No AI hallucination - rule-based extraction only.
    """
    
    def __init__(self):
        # City patterns (can be extended)
        self.cities = [
            "mumbai", "delhi", "bangalore", "chennai", "kolkata",
            "hyderabad", "pune", "ahmedabad", "jaipur", "surat",
            "lucknow", "kanpur", "nagpur", "indore", "bhopal",
            "visakhapatnam", "vadodara", "coimbatore", "kochi", "guwahati"
        ]
        
        # State to region mapping for silver rates
        self.state_region_map = {
            # North
            "delhi": Region.NORTH, "punjab": Region.NORTH, "haryana": Region.NORTH,
            "rajasthan": Region.NORTH, "uttar pradesh": Region.NORTH, "himachal pradesh": Region.NORTH,
            "uttarakhand": Region.NORTH, "jammu": Region.NORTH, "kashmir": Region.NORTH,
            # South
            "karnataka": Region.SOUTH, "tamil nadu": Region.SOUTH, "kerala": Region.SOUTH,
            "andhra pradesh": Region.SOUTH, "telangana": Region.SOUTH, "puducherry": Region.SOUTH,
            # East
            "west bengal": Region.EAST, "odisha": Region.EAST, "bihar": Region.EAST,
            "jharkhand": Region.EAST, "assam": Region.EAST, "tripura": Region.EAST,
            # West
            "maharashtra": Region.WEST, "gujarat": Region.WEST, "goa": Region.WEST,
            # Central
            "madhya pradesh": Region.CENTRAL, "chhattisgarh": Region.CENTRAL,
        }
    
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
        
        # Extract state
        entities.state = self._extract_state(text_lower)
        
        # Extract region from state
        if entities.state:
            entities.region = self.state_region_map.get(entities.state)
        
        # Extract product type
        entities.product_type = self._extract_product_type(text_lower)
        
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
        if "24k" in text or "24 k" in text or "24 carat" in text or "999" in text:
            return Purity.GOLD_24K
        elif "22k" in text or "22 k" in text or "22 carat" in text:
            return Purity.GOLD_22K
        elif "18k" in text or "18 k" in text or "18 carat" in text or "18ct" in text:
            return Purity.GOLD_18K
        elif "916" in text:
            return Purity.GOLD_916
        elif "950" in text:
            return Purity.PLATINUM_950
        return None
    
    def _extract_weight(self, text: str) -> float:
        """
        Extract weight from text (supports Hindi and English).
        Default is 1 gram if not specified.
        """
        # Look for patterns like "10 gram", "10g", "10 grams" (English)
        weight_match = re.search(r'(\d+\.?\d*)\s*(?:gram|grams|g|gm)\b', text)
        if weight_match:
            try:
                return float(weight_match.group(1))
            except ValueError:
                pass
        
        # Look for Hindi patterns like "10 ग्राम"
        weight_match_hindi = re.search(r'(\d+\.?\d*)\s*(?:ग्राम|ग्राम)', text)
        if weight_match_hindi:
            try:
                return float(weight_match_hindi.group(1))
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
    
    def _extract_state(self, text: str) -> Optional[str]:
        """Extract state name from text"""
        for state in self.state_region_map.keys():
            if state in text:
                return state
        return None
    
    def _extract_product_type(self, text: str) -> Optional[ProductType]:
        """Extract product type from text"""
        if "coin" in text or "coins" in text:
            return ProductType.COIN
        elif "biscuit" in text or "biscuits" in text:
            return ProductType.BISCUIT
        elif "chain" in text or "chains" in text:
            return ProductType.CHAIN
        elif "jewelry" in text or "jewellery" in text:
            return ProductType.JEWELRY
        return ProductType.GENERAL

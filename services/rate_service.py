from typing import Tuple
from nlu.entities import Purity


class RateService:
    """
    Rate calculation service for precious metals.
    
    Rules:
    - Accept base 24K rate
    - Convert to 22K / 18K
    - Multiply by weight
    - Return formatted string + numeric value
    
    No API calls here - rates are injected via config or cache.
    """
    
    # Conversion factors from 24K
    PURITY_CONVERSION = {
        Purity.GOLD_24K: 1.0,
        Purity.GOLD_22K: 22.0 / 24.0,  # 0.9167
        Purity.GOLD_18K: 18.0 / 24.0,  # 0.75
    }
    
    def __init__(self, base_rates: dict = None):
        """
        Initialize with base rates.
        
        Args:
            base_rates: Dict with base 24K rates per gram
                       e.g., {"gold": 6000, "silver": 80, "platinum": 3000}
        """
        self.base_rates = base_rates or {
            "gold": 6500,     # Base 24K gold per gram
            "silver": 85,     # Base silver per gram
            "platinum": 3200  # Base platinum per gram
        }
    
    def calculate_rate(
        self,
        metal: str,
        purity: Purity = None,
        weight: float = 1.0
    ) -> Tuple[float, str]:
        """
        Calculate rate for given metal, purity, and weight.
        
        Args:
            metal: Metal type ("gold", "silver", "platinum")
            purity: Purity level (for gold)
            weight: Weight in grams
        
        Returns:
            Tuple of (numeric_value, formatted_string)
        """
        if metal not in self.base_rates:
            return 0.0, "Metal type not supported"
        
        base_rate = self.base_rates[metal]
        
        # Apply purity conversion for gold
        if metal == "gold" and purity in self.PURITY_CONVERSION:
            conversion_factor = self.PURITY_CONVERSION[purity]
            rate_per_gram = base_rate * conversion_factor
        else:
            rate_per_gram = base_rate
        
        # Calculate total
        total_price = rate_per_gram * weight
        
        # Format response
        purity_str = f" {purity.value}" if purity else ""
        formatted = (
            f"Current {metal.title()}{purity_str} rate: "
            f"₹{rate_per_gram:.2f} per gram\n"
            f"For {weight}g: ₹{total_price:.2f}"
        )
        
        return total_price, formatted
    
    def get_base_rate(self, metal: str) -> float:
        """Get base rate for a metal"""
        return self.base_rates.get(metal, 0.0)
    
    def update_base_rate(self, metal: str, rate: float) -> None:
        """Update base rate for a metal"""
        self.base_rates[metal] = rate

from typing import Tuple, Optional
from nlu.entities import Purity, ProductType, Region


class RateService:
    """
    Rate calculation service for precious metals.
    
    Rules:
    - Accept base 24K rate (from IBJA or similar source)
    - Convert to 22K / 18K
    - Multiply by weight
    - Add GST for gold coins/biscuits (3%)
    - State-wise silver rates
    - Return formatted string + numeric value
    
    No API calls here - rates are injected via config or cache.
    """
    
    # Conversion factors from 24K
    PURITY_CONVERSION = {
        Purity.GOLD_24K: 1.0,
        Purity.GOLD_22K: 22.0 / 24.0,  # 0.9167
        Purity.GOLD_18K: 18.0 / 24.0,  # 0.75
    }
    
    # GST rate for gold coins/biscuits
    GST_RATE_COINS = 0.03  # 3%
    
    def __init__(self, base_rates: dict = None, regional_silver_rates: dict = None):
        """
        Initialize with base rates.
        
        Args:
            base_rates: Dict with base 24K rates per gram
                       e.g., {"gold": 6000, "silver": 80, "platinum": 3000}
            regional_silver_rates: Dict with region-wise silver rates
        """
        self.base_rates = base_rates or {
            "gold": 6500,     # Base 24K gold per gram (IBJA reference)
            "silver": 85,     # Base silver per gram
            "platinum": 3200  # Base platinum per gram
        }
        
        # State-wise silver rates (per gram)
        self.regional_silver_rates = regional_silver_rates or {
            Region.NORTH: 85,
            Region.SOUTH: 83,
            Region.EAST: 84,
            Region.WEST: 86,
            Region.CENTRAL: 85,
        }
    
    def calculate_rate(
        self,
        metal: str,
        purity: Purity = None,
        weight: float = 1.0,
        product_type: ProductType = None,
        region: Region = None
    ) -> Tuple[float, str]:
        """
        Calculate rate for given metal, purity, and weight.
        
        Args:
            metal: Metal type ("gold", "silver", "platinum")
            purity: Purity level (for gold)
            weight: Weight in grams
            product_type: Product type (coin, biscuit, chain, jewelry)
            region: Region for state-wise rates (silver)
        
        Returns:
            Tuple of (numeric_value, formatted_string)
        """
        if metal not in self.base_rates:
            return 0.0, "Metal type not supported"
        
        # Handle 18K chain constraint
        if metal == "gold" and purity == Purity.GOLD_18K and product_type == ProductType.CHAIN:
            return 0.0, "Sorry, 18K gold chains are not available at Kalyan Jewellers."
        
        base_rate = self.base_rates[metal]
        
        # Apply purity conversion for gold
        if metal == "gold" and purity in self.PURITY_CONVERSION:
            conversion_factor = self.PURITY_CONVERSION[purity]
            rate_per_gram = base_rate * conversion_factor
        elif metal == "silver" and region:
            # Use regional rate for silver
            rate_per_gram = self.regional_silver_rates.get(region, base_rate)
        else:
            rate_per_gram = base_rate
        
        # Calculate total before GST
        total_price = rate_per_gram * weight
        
        # Add GST for gold coins/biscuits (3%)
        gst_amount = 0.0
        if metal == "gold" and product_type in [ProductType.COIN, ProductType.BISCUIT]:
            gst_amount = total_price * self.GST_RATE_COINS
            total_with_gst = total_price + gst_amount
        else:
            total_with_gst = total_price
        
        # Format response
        purity_str = f" {purity.value}" if purity else ""
        product_str = f" {product_type.value}" if product_type else ""
        
        if gst_amount > 0:
            formatted = (
                f"Current Gold{purity_str}{product_str} rate: "
                f"₹{rate_per_gram:.2f} per gram\n"
                f"For {weight}g: ₹{total_price:.2f}\n"
                f"GST (3%): ₹{gst_amount:.2f}\n"
                f"Total with GST: ₹{total_with_gst:.2f}"
            )
        else:
            formatted = (
                f"Current {metal.title()}{purity_str}{product_str} rate: "
                f"₹{rate_per_gram:.2f} per gram\n"
                f"For {weight}g: ₹{total_price:.2f}"
            )
        
        return total_with_gst, formatted
    
    def get_base_rate(self, metal: str) -> float:
        """Get base rate for a metal"""
        return self.base_rates.get(metal, 0.0)
    
    def update_base_rate(self, metal: str, rate: float) -> None:
        """Update base rate for a metal"""
        self.base_rates[metal] = rate
    
    def get_silver_rate_by_region(self, region: Region) -> float:
        """Get silver rate for a specific region"""
        return self.regional_silver_rates.get(region, self.base_rates["silver"])

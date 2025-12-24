from typing import Optional, Dict


class StoreService:
    """
    Lookup store timings and address from data source.
    
    Supports:
    - city lookup
    - pincode fallback
    - "nearest store" logic stub
    """
    
    def __init__(self, store_data: list = None):
        """
        Initialize with store data.
        
        Args:
            store_data: List of store dicts with city, pincode, address, timings
        """
        self.store_data = store_data or self._default_store_data()
    
    def _default_store_data(self) -> list:
        """Default store data"""
        return [
            {
                "city": "Mumbai",
                "pincode": "400001",
                "address": "123 Gold Street, Fort, Mumbai - 400001",
                "timings": "9:00 AM - 8:00 PM, Monday to Sunday",
                "phone": "+91-9876543210"
            },
            {
                "city": "Delhi",
                "pincode": "110001",
                "address": "456 Silver Avenue, Connaught Place, Delhi - 110001",
                "timings": "10:00 AM - 9:00 PM, Monday to Sunday",
                "phone": "+91-9876543211"
            },
            {
                "city": "Bangalore",
                "pincode": "560001",
                "address": "789 Platinum Road, MG Road, Bangalore - 560001",
                "timings": "9:30 AM - 8:30 PM, Monday to Sunday",
                "phone": "+91-9876543212"
            }
        ]
    
    def get_store_by_city(self, city: str) -> Optional[Dict]:
        """
        Get store information by city name.
        
        Args:
            city: City name
        
        Returns:
            Store dict or None if not found
        """
        city_lower = city.lower()
        for store in self.store_data:
            if store["city"].lower() == city_lower:
                return store
        return None
    
    def get_store_by_pincode(self, pincode: str) -> Optional[Dict]:
        """
        Get store information by pincode.
        
        Args:
            pincode: Pincode string
        
        Returns:
            Store dict or None if not found
        """
        for store in self.store_data:
            if store["pincode"] == pincode:
                return store
        return None
    
    def get_nearest_store(self, city: str = None, pincode: str = None) -> Optional[Dict]:
        """
        Get nearest store based on city or pincode.
        
        Args:
            city: City name (optional)
            pincode: Pincode string (optional)
        
        Returns:
            Store dict or None if not found
        """
        # Try city first
        if city:
            store = self.get_store_by_city(city)
            if store:
                return store
        
        # Fallback to pincode
        if pincode:
            store = self.get_store_by_pincode(pincode)
            if store:
                return store
        
        # Return first store as default if nothing matches
        return self.store_data[0] if self.store_data else None
    
    def format_store_timings(self, store: Dict) -> str:
        """Format store timings for response"""
        return (
            f"Store Timings:\n"
            f"{store['timings']}\n"
            f"Location: {store['city']}"
        )
    
    def format_store_address(self, store: Dict) -> str:
        """Format store address for response"""
        return (
            f"Store Address:\n"
            f"{store['address']}\n"
            f"Phone: {store['phone']}"
        )

"""
Language detection and translation service for Hindi and English.
Phase 1: Hindi and English support
"""
from typing import Optional


class LanguageDetector:
    """
    Detects language from user input.
    Supports Hindi and English as per Phase 1 requirements.
    """
    
    # Hindi words/characters that indicate Hindi language
    HINDI_INDICATORS = [
        # Devanagari script range
        '\u0900', '\u0901', '\u0902', '\u0903', '\u0904', '\u0905', '\u0906', '\u0907',
        '\u0908', '\u0909', '\u090a', '\u090b', '\u090c', '\u090d', '\u090e', '\u090f',
        '\u0910', '\u0911', '\u0912', '\u0913', '\u0914', '\u0915', '\u0916', '\u0917',
        '\u0918', '\u0919', '\u091a', '\u091b', '\u091c', '\u091d', '\u091e', '\u091f',
        '\u0920', '\u0921', '\u0922', '\u0923', '\u0924', '\u0925', '\u0926', '\u0927',
        '\u0928', '\u0929', '\u092a', '\u092b', '\u092c', '\u092d', '\u092e', '\u092f',
        '\u0930', '\u0931', '\u0932', '\u0933', '\u0934', '\u0935', '\u0936', '\u0937',
        '\u0938', '\u0939', '\u093e', '\u093f', '\u0940', '\u0941', '\u0942', '\u0943',
        '\u0944', '\u0945', '\u0946', '\u0947', '\u0948', '\u0949', '\u094a', '\u094b',
        '\u094c', '\u094d',
        # Common Hindi words in Roman script
        "sona", "chandi", "dukan", "samay", "kaha", "kitna", "kya", "hai", "aur",
        "mein", "ka", "ki", "ke", "se", "ko", "par", "sunaar"
    ]
    
    def detect_language(self, text: str) -> str:
        """
        Detect language from text.
        Returns 'hi' for Hindi, 'en' for English.
        
        Detection logic:
        - If Devanagari script is present → Hindi
        - If Hindi words in Roman script → Hindi
        - Otherwise → English (default)
        """
        if not text:
            return "en"
        
        text_lower = text.lower()
        
        # Check for Devanagari script
        for char in text:
            if '\u0900' <= char <= '\u097f':
                return "hi"
        
        # Check for common Hindi words in Roman script
        for indicator in self.HINDI_INDICATORS:
            if indicator in text_lower:
                return "hi"
        
        # Default to English
        return "en"


class ResponseTranslator:
    """
    Translates responses between Hindi and English.
    Contains bilingual templates for all bot responses.
    """
    
    def __init__(self):
        # Bilingual response templates
        self.templates = {
            "greeting": {
                "en": "Hello! Welcome to Kalyan Jewellers. 👋\n\nI am your virtual assistant. I can help you with:\n• Gold, Silver, and Platinum rates\n• Store timings and locations\n• General inquiries\n\nHow can I assist you today?",
                "hi": "नमस्ते! कल्याण ज्वैलर्स में आपका स्वागत है। 👋\n\nमैं आपका वर्चुअल असिस्टेंट हूं। मैं आपकी मदद कर सकता हूं:\n• सोने, चांदी और प्लैटिनम की दरें\n• स्टोर का समय और स्थान\n• सामान्य जानकारी\n\nआज मैं आपकी कैसे मदद कर सकता हूं?"
            },
            "store_timings": {
                "en": "Store Timings:\n{timings}\nLast walk-in: 08:20 PM\nLocation: {city}",
                "hi": "स्टोर का समय:\n{timings}\nअंतिम प्रवेश: रात 08:20 बजे\nस्थान: {city}"
            },
            "store_address": {
                "en": "Store Address:\n{address}\nPhone: {phone}",
                "hi": "स्टोर का पता:\n{address}\nफोन: {phone}"
            },
            "gold_rate": {
                "en": "Current Gold {purity} rate: ₹{rate} per gram\nFor {weight}g: ₹{total}",
                "hi": "वर्तमान सोने {purity} की दर: ₹{rate} प्रति ग्राम\n{weight}g के लिए: ₹{total}"
            },
            "silver_rate": {
                "en": "Current Silver rate: ₹{rate} per gram\nFor {weight}g: ₹{total}",
                "hi": "वर्तमान चांदी की दर: ₹{rate} प्रति ग्राम\n{weight}g के लिए: ₹{total}"
            },
            "platinum_rate": {
                "en": "Current Platinum rate: ₹{rate} per gram\nFor {weight}g: ₹{total}",
                "hi": "वर्तमान प्लैटिनम की दर: ₹{rate} प्रति ग्राम\n{weight}g के लिए: ₹{total}"
            },
            "gold_coin_gst": {
                "en": "Current Gold {purity} {product} rate: ₹{rate} per gram\nFor {weight}g: ₹{subtotal}\nGST (3%): ₹{gst}\nTotal with GST: ₹{total}",
                "hi": "वर्तमान सोने {purity} {product} की दर: ₹{rate} प्रति ग्राम\n{weight}g के लिए: ₹{subtotal}\nजीएसटी (3%): ₹{gst}\nजीएसटी के साथ कुल: ₹{total}"
            },
            "clarification": {
                "en": "I didn't quite understand that. Could you please rephrase?\n\nYou can ask me about:\n• Gold, Silver, or Platinum rates\n• Store timings\n• Store address",
                "hi": "मैं समझ नहीं पाया। कृपया दोबारा बताएं?\n\nआप मुझसे पूछ सकते हैं:\n• सोने, चांदी या प्लैटिनम की दरें\n• स्टोर का समय\n• स्टोर का पता"
            },
            "transfer": {
                "en": "I'm having trouble understanding your request. Let me connect you with a customer service representative who can better assist you.",
                "hi": "मुझे आपका अनुरोध समझने में परेशानी हो रही है। मैं आपको एक ग्राहक सेवा प्रतिनिधि से जोड़ता हूं जो आपकी बेहतर मदद कर सकते हैं।"
            },
            "transfer_request": {
                "en": "Connecting you to a customer service representative. Please hold.",
                "hi": "आपको ग्राहक सेवा प्रतिनिधि से जोड़ रहा हूं। कृपया प्रतीक्षा करें।"
            },
            "out_of_scope": {
                "en": "I apologize, but I cannot provide information about discounts, offers, or future rate predictions. I can help you with current rates, store timings, and locations.\n\nWould you like to know about current rates or store information?",
                "hi": "मुझे खेद है, लेकिन मैं छूट, ऑफर या भविष्य की दर के बारे में जानकारी नहीं दे सकता। मैं आपको वर्तमान दरों, स्टोर के समय और स्थानों के बारे में मदद कर सकता हूं।\n\nक्या आप वर्तमान दरों या स्टोर की जानकारी जानना चाहेंगे?"
            },
            "18k_chain_unavailable": {
                "en": "Sorry, 18K gold chains are not available at Kalyan Jewellers.",
                "hi": "क्षमा करें, कल्याण ज्वैलर्स में 18K सोने की चेन उपलब्ध नहीं है।"
            },
            "need_location": {
                "en": "Could you please provide your city or pincode?",
                "hi": "क्या आप कृपया अपना शहर या पिनकोड बता सकते हैं?"
            },
            "multi_intent_response": {
                "en": "I can help you with multiple queries. Let me answer each one:",
                "hi": "मैं आपके कई सवालों में मदद कर सकता हूं। मुझे हर एक का जवाब देने दें:"
            }
        }
    
    def get_response(self, key: str, language: str = "en", **kwargs) -> str:
        """
        Get response in specified language with placeholders filled.
        
        Args:
            key: Template key
            language: Language code ('en' or 'hi')
            **kwargs: Values to fill in template placeholders
        
        Returns:
            Formatted response string
        """
        template = self.templates.get(key, {}).get(language, self.templates.get(key, {}).get("en", ""))
        
        if not template:
            return ""
        
        try:
            return template.format(**kwargs)
        except KeyError:
            # If some placeholder is missing, return template as-is
            return template
    
    def translate_metal_name(self, metal: str, language: str) -> str:
        """Translate metal names"""
        translations = {
            "en": {"gold": "Gold", "silver": "Silver", "platinum": "Platinum"},
            "hi": {"gold": "सोना", "silver": "चांदी", "platinum": "प्लैटिनम"}
        }
        return translations.get(language, translations["en"]).get(metal.lower(), metal)
    
    def translate_product_name(self, product: str, language: str) -> str:
        """Translate product names"""
        translations = {
            "en": {"coin": "coin", "biscuit": "biscuit", "chain": "chain", "jewelry": "jewelry"},
            "hi": {"coin": "सिक्का", "biscuit": "बिस्किट", "chain": "चेन", "jewelry": "आभूषण"}
        }
        return translations.get(language, translations["en"]).get(product.lower(), product)

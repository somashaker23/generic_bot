"""
Local small model classifier for the fallback path.

This module provides integration with local small models like:
- Qwen 1.5B
- Phi-3 Mini
- Gemma 2B

Target latency: 100-300ms
"""

from typing import Tuple, Optional
from nlu.intents import Intent
from nlu.entities import ExtractedEntities, MetalType, Purity


class LocalModelClassifier:
    """
    Local small model classifier for intent and entity extraction.
    
    Uses lightweight models that can run locally without API calls:
    - Qwen 1.5B
    - Phi-3 Mini  
    - Gemma 2B
    
    These models provide a balance between accuracy and speed,
    targeting 100-300ms inference time.
    """
    
    def __init__(self, model_name: str = "qwen-1.5b", model_path: Optional[str] = None):
        """
        Initialize local model classifier.
        
        Args:
            model_name: Name of the model to use (qwen-1.5b, phi-3-mini, gemma-2b)
            model_path: Optional path to local model files
        """
        self.model_name = model_name
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        
        # Model will be lazy-loaded on first use
        self._initialized = False
    
    def _initialize_model(self):
        """
        Lazy initialization of the model.
        
        This is a stub that should be implemented based on the chosen model.
        For production use, you would:
        1. Load the model using transformers or similar
        2. Set up the tokenizer
        3. Configure inference settings
        """
        if self._initialized:
            return
        
        # TODO: Implement actual model loading
        # Example for Qwen:
        # from transformers import AutoModelForCausalLM, AutoTokenizer
        # self.model = AutoModelForCausalLM.from_pretrained(self.model_path or f"Qwen/{self.model_name}")
        # self.tokenizer = AutoTokenizer.from_pretrained(self.model_path or f"Qwen/{self.model_name}")
        
        print(f"[LocalModelClassifier] Model loading not yet implemented. Using stub.")
        self._initialized = True
    
    def classify_with_entities(self, text: str) -> Tuple[Intent, float, ExtractedEntities]:
        """
        Classify intent and extract entities using local model.
        
        Args:
            text: User input text
            
        Returns:
            Tuple of (Intent, confidence, ExtractedEntities)
        """
        self._initialize_model()
        
        # TODO: Implement actual model inference
        # This is a stub implementation that returns None to indicate
        # the model is not available
        
        # For production, you would:
        # 1. Create a prompt for the model
        # 2. Run inference
        # 3. Parse the model output
        # 4. Map to Intent enum and extract entities
        
        # Return None values to indicate model not available
        # This will cause the pipeline to skip this layer
        raise NotImplementedError(
            "Local model inference not yet implemented. "
            "To enable fallback path, implement model loading and inference."
        )
    
    def _create_prompt(self, text: str) -> str:
        """
        Create a prompt for the local model.
        
        This should be optimized for the specific model being used.
        """
        prompt = f"""You are a jewelry store assistant. Analyze the following customer query and extract:
1. Intent (one of: gold_rate, silver_rate, platinum_rate, gold_coin_rate, store_timings, store_address, greeting, out_of_scope, transfer_request)
2. Entities (metal type, purity, weight, city, pincode)
3. Your confidence (0.0 to 1.0)

Customer query: "{text}"

Respond in JSON format:
{{
  "intent": "...",
  "confidence": 0.0,
  "entities": {{
    "metal_type": "...",
    "purity": "...",
    "weight": 0.0
  }}
}}
"""
        return prompt
    
    def _parse_model_output(self, output: str) -> Tuple[Intent, float, ExtractedEntities]:
        """
        Parse model output and convert to Intent and ExtractedEntities.
        
        Args:
            output: Raw model output
            
        Returns:
            Tuple of (Intent, confidence, ExtractedEntities)
        """
        # TODO: Implement parsing logic
        # This would parse JSON or structured output from the model
        # and map it to our Intent enum and ExtractedEntities
        
        pass

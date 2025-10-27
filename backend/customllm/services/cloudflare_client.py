"""
Cloudflare Workers AI Client
Handles communication with Cloudflare's AI platform for custom model inference
"""

import os
import requests
import logging
from typing import Dict, List, Optional, Any
import json

logger = logging.getLogger(__name__)


class CloudflareAIClient:
    """
    Client for Cloudflare Workers AI platform
    Supports custom fine-tuned models and Cloudflare's built-in models
    """
    
    def __init__(self):
        self.api_key = os.getenv('CLOUDFLARE_API_TOKEN')
        self.account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        self.custom_model_id = os.getenv('CUSTOM_MODEL_ID', '@cf/meta/llama-3.1-8b-instruct')
        
        if not self.api_key or not self.account_id:
            raise ValueError("CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID must be set in environment variables")
        
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def call_model(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call Cloudflare AI model with given prompt
        
        Args:
            prompt: Input prompt for the model
            model: Model identifier (uses custom model by default)
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0-1)
            **kwargs: Additional model-specific parameters
        
        Returns:
            Dict containing model response and metadata
        """
        model_to_use = model or self.custom_model_id
        url = f"{self.base_url}/{model_to_use}"
        
        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            **kwargs
        }
        
        try:
            logger.info(f"Calling Cloudflare model: {model_to_use}")
            start_time = time.time()
            
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Model call successful in {elapsed_time:.2f}s")
                
                return {
                    "success": True,
                    "response": result.get("result", {}).get("response", ""),
                    "model": model_to_use,
                    "elapsed_time": elapsed_time,
                    "tokens": result.get("result", {}).get("tokens_used", 0)
                }
            else:
                logger.error(f"Cloudflare API error: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "model": model_to_use
                }
                
        except requests.Timeout:
            logger.error("Cloudflare API timeout")
            return {
                "success": False,
                "error": "Request timeout",
                "model": model_to_use
            }
        except Exception as e:
            logger.error(f"Cloudflare API call failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "model": model_to_use
            }
    
    def generate_text_stream(
        self,
        prompt: str,
        model: Optional[str] = None,
        **kwargs
    ):
        """
        Stream text generation from Cloudflare AI
        
        Args:
            prompt: Input prompt
            model: Model identifier
            **kwargs: Additional parameters
        
        Yields:
            Chunks of generated text
        """
        model_to_use = model or self.custom_model_id
        url = f"{self.base_url}/{model_to_use}"
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            **kwargs
        }
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                stream=True,
                timeout=120
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode('utf-8'))
                            if 'response' in data:
                                yield data['response']
                        except json.JSONDecodeError:
                            continue
            else:
                logger.error(f"Stream generation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Stream generation error: {str(e)}")
    
    def generate_image(
        self,
        prompt: str,
        model: str = "@cf/stabilityai/stable-diffusion-xl-base-1.0",
        **kwargs
    ) -> Optional[bytes]:
        """
        Generate image using Cloudflare AI
        
        Args:
            prompt: Image description prompt
            model: Image generation model
            **kwargs: Additional parameters (width, height, steps, etc.)
        
        Returns:
            Image bytes or None if failed
        """
        url = f"{self.base_url}/{model}"
        
        payload = {
            "prompt": prompt,
            **kwargs
        }
        
        try:
            logger.info(f"Generating image with Cloudflare: {model}")
            
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                logger.info("Image generated successfully")
                return response.content
            else:
                logger.error(f"Image generation failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Image generation error: {str(e)}")
            return None
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available Cloudflare AI models
        
        Returns:
            List of model identifiers
        """
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/models"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return [model.get("name") for model in result.get("result", [])]
            else:
                logger.error(f"Failed to fetch models: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching models: {str(e)}")
            return []
    
    def test_connection(self) -> bool:
        """
        Test Cloudflare API connection
        
        Returns:
            True if connection successful
        """
        try:
            result = self.call_model("Say 'hello'", max_tokens=10)
            return result.get("success", False)
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False


# Add time import
import time

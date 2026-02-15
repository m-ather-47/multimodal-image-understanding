import io
import base64
from typing import Dict, List, Any
from PIL import Image
import google.generativeai as genai

class ImageAnalyzer:
    """Simple image analyzer using Gemini only"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Use current vision model (2026 standard)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def _image_to_part(self, image_data):
        """Convert image to Gemini Part format (current standard)"""
        if isinstance(image_data, Image.Image):
            byte_arr = io.BytesIO()
            image_data.save(byte_arr, format='PNG')
            image_bytes = byte_arr.getvalue()
        elif isinstance(image_data, bytes):
            image_bytes = image_data
        elif isinstance(image_data, io.BytesIO):
            image_bytes = image_data.getvalue()
        else:
            raise ValueError("Unsupported image format")
        
        return {
            "mime_type": "image/png",
            "data": base64.b64encode(image_bytes).decode()
        }
    
    def _query_gemini(self, prompt: str, image_data) -> str:
        """Send multimodal request to Gemini 1.5"""
        image_part = self._image_to_part(image_data)
        response = self.model.generate_content([prompt, image_part])
        return response.text if response else "Unable to analyze"
    
    def get_caption(self, image_data) -> str:
        """One-sentence caption"""
        prompt = "Provide ONE sentence describing this image. Be factual and direct."
        return self._query_gemini(prompt, image_data)
    
    def get_summary(self, image_data) -> str:
        """3-5 line summary"""
        prompt = "Write a 3-5 line summary of this image. Focus on main elements."
        return self._query_gemini(prompt, image_data)
    
    def get_objects(self, image_data) -> List[str]:
        """List objects and entities"""
        prompt = "List all visible objects and entities. Format as comma-separated list only."
        result = self._query_gemini(prompt, image_data)
        return [obj.strip() for obj in result.split(',') if obj.strip()][:15]
    
    def get_emotions(self, image_data) -> str:
        """Emotional tone analysis"""
        prompt = "What emotional tone or mood does this image convey? Be specific."
        return self._query_gemini(prompt, image_data)
    
    def get_story(self, image_data) -> str:
        """Creative story"""
        prompt = "Write a creative 5-10 line story inspired by this image. Be imaginative."
        return self._query_gemini(prompt, image_data)
    
    def analyze(self, image_data) -> Dict[str, Any]:
        """One-shot comprehensive analysis (most efficient)"""
        prompt = """
        Analyze this image and return ONLY valid JSON:
        {
            "caption": "One sentence description",
            "summary": "3-5 line detailed description",
            "objects": ["list", "of", "objects"], 
            "emotions": "Emotional tone analysis",
            "story": "5-10 line creative story"
        }
        """
        result = self._query_gemini(prompt, image_data)
        
        # Simple JSON extraction (improve as needed)
        import json
        try:
            # Extract JSON from response
            start = result.find('{')
            end = result.rfind('}') + 1
            json_str = result[start:end]
            return json.loads(json_str)
        except:
            # Fallback to individual calls if JSON fails
            return {
                "caption": self._query_gemini("One sentence describing this image.", image_data),
                "summary": self._query_gemini("3-5 line summary of main elements.", image_data),
                "objects": self._query_gemini("List visible objects as comma-separated.", image_data).split(','),
                "emotions": self._query_gemini("Emotional tone/mood of this image.", image_data),
                "story": self._query_gemini("5-10 line creative story inspired by image.", image_data)
            }

# Image Analyzer Module
# Handles image analysis using different API providers

import io
from abc import ABC, abstractmethod
from typing import Dict, List, Any
import base64
from PIL import Image

class BaseAnalyzer(ABC):
    """Base class for image analyzers"""
    
    @abstractmethod
    def analyze(self, image_data) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_caption(self, image_data) -> str:
        pass
    
    @abstractmethod
    def get_summary(self, image_data) -> str:
        pass
    
    @abstractmethod
    def get_objects(self, image_data) -> List[str]:
        pass
    
    @abstractmethod
    def get_emotions(self, image_data) -> str:
        pass
    
    @abstractmethod
    def get_story(self, image_data) -> str:
        pass


class GeminiAnalyzer(BaseAnalyzer):
    """Image analyzer using Google Generative AI (Gemini)"""
    
    def __init__(self, api_key: str):
        try:
            import google.generativeai as genai
            self.client = genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro-vision')
            self.api_key = api_key
        except ImportError:
            raise ImportError("google-generativeai not installed. Install with: pip install google-generativeai")
    
    def _image_to_bytes(self, image_data) -> bytes:
        """Convert image to bytes"""
        if isinstance(image_data, bytes):
            return image_data
        elif isinstance(image_data, io.BytesIO):
            return image_data.getvalue()
        elif isinstance(image_data, Image.Image):
            byte_arr = io.BytesIO()
            image_data.save(byte_arr, format='PNG')
            return byte_arr.getvalue()
        return image_data
    
    def _send_request(self, prompt: str, image_data) -> str:
        """Send request to Gemini API"""
        import google.generativeai as genai
        
        # Prepare image
        image_bytes = self._image_to_bytes(image_data)
        image_part = {
            "mime_type": "image/png",
            "data": base64.standard_b64encode(image_bytes).decode("utf-8")
        }
        
        # Send request
        response = self.model.generate_content([prompt, image_part])
        return response.text if response else "Unable to analyze"
    
    def get_caption(self, image_data) -> str:
        prompt = "Provide a one-sentence factual caption describing this image. Be concise and direct."
        return self._send_request(prompt, image_data)
    
    def get_summary(self, image_data) -> str:
        prompt = "Provide a 3-5 line descriptive summary of this image. Focus on main elements and their relationships."
        return self._send_request(prompt, image_data)
    
    def get_objects(self, image_data) -> List[str]:
        prompt = "List all visible objects and entities in this image. Provide only the list items separated by commas, no additional text."
        result = self._send_request(prompt, image_data)
        # Parse comma-separated list
        objects = [obj.strip() for obj in result.split(',') if obj.strip()]
        return objects[:15]  # Limit to 15 objects
    
    def get_emotions(self, image_data) -> str:
        prompt = "Analyze the emotional tone and mood of this image. Describe what emotions or atmospheres it conveys (e.g., happy, tense, calm, chaotic). Be specific and detailed."
        return self._send_request(prompt, image_data)
    
    def get_story(self, image_data) -> str:
        prompt = "Create a short creative story inspired by this image. The story should be 5-10 lines long, imaginative, and capture the essence of what you see. Make it engaging and vivid."
        return self._send_request(prompt, image_data)
    
    def analyze(self, image_data) -> Dict[str, Any]:
        """Perform complete image analysis"""
        return {
            "caption": self.get_caption(image_data),
            "summary": self.get_summary(image_data),
            "objects": self.get_objects(image_data),
            "emotions": self.get_emotions(image_data),
            "story": self.get_story(image_data)
        }


class VisionAnalyzer(BaseAnalyzer):
    """Image analyzer using Google Cloud Vision API"""
    
    def __init__(self, api_key: str):
        try:
            from google.cloud import vision
            import os
            
            # Set API key for authentication
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key
            self.client = vision.ImageAnnotatorClient()
            self.api_key = api_key
        except ImportError:
            raise ImportError("google-cloud-vision not installed. Install with: pip install google-cloud-vision")
    
    def _image_to_bytes(self, image_data) -> bytes:
        """Convert image to bytes"""
        if isinstance(image_data, bytes):
            return image_data
        elif isinstance(image_data, io.BytesIO):
            return image_data.getvalue()
        elif isinstance(image_data, Image.Image):
            byte_arr = io.BytesIO()
            image_data.save(byte_arr, format='PNG')
            return byte_arr.getvalue()
        return image_data
    
    def _generate_text_response(self, analysis_data: Dict[str, Any], prompt_type: str) -> str:
        """Generate text response based on Vision API analysis"""
        
        prompts = {
            "caption": f"Based on detected labels {analysis_data.get('labels', [])} and text '{analysis_data.get('text', '')}', create a one-sentence caption.",
            "summary": f"Create a 3-5 line summary based on: Labels: {analysis_data.get('labels', [])}. Text found: '{analysis_data.get('text', '')}'",
            "emotions": f"Based on colors {analysis_data.get('colors', [])} and content {analysis_data.get('labels', [])}, infer emotional tone.",
            "story": f"Create a 5-10 line creative story inspired by these elements: {analysis_data.get('labels', [])}"
        }
        
        return prompts.get(prompt_type, "Analysis not available")
    
    def get_caption(self, image_data) -> str:
        """Get caption from Vision API"""
        from google.cloud import vision
        
        image_bytes = self._image_to_bytes(image_data)
        image = vision.Image(content=image_bytes)
        
        response = self.client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations[:5]]
        
        return f"Image containing {', '.join(labels)}." if labels else "Image detected"
    
    def get_summary(self, image_data) -> str:
        """Get summary from Vision API"""
        from google.cloud import vision
        
        image_bytes = self._image_to_bytes(image_data)
        image = vision.Image(content=image_bytes)
        
        # Get labels
        label_response = self.client.label_detection(image=image)
        labels = [label.description for label in label_response.label_annotations[:8]]
        
        summary = f"The image prominently features {', '.join(labels[:3])}. "
        summary += f"Additional elements include {', '.join(labels[3:6])}. "
        summary += "The composition suggests a well-structured and intentional arrangement."
        
        return summary
    
    def get_objects(self, image_data) -> List[str]:
        """Detect objects using Vision API"""
        from google.cloud import vision
        
        image_bytes = self._image_to_bytes(image_data)
        image = vision.Image(content=image_bytes)
        
        # Label detection
        response = self.client.label_detection(image=image)
        objects = [label.description for label in response.label_annotations[:15]]
        
        return objects if objects else ["Image", "Visual content"]
    
    def get_emotions(self, image_data) -> str:
        """Infer emotions from Vision API data"""
        from google.cloud import vision
        
        image_bytes = self._image_to_bytes(image_data)
        image = vision.Image(content=image_bytes)
        
        # Color analysis
        response = self.client.image_properties(image=image)
        colors = response.image_properties_annotation.dominant_colors.colors
        
        color_names = {
            "red": "energetic, passionate",
            "blue": "calm, serene, peaceful",
            "green": "natural, fresh, balanced",
            "yellow": "warm, optimistic, cheerful",
            "black": "dramatic, sophisticated, serious",
            "white": "pure, clean, minimal",
            "gray": "neutral, calm, stable",
            "orange": "vibrant, playful, energetic"
        }
        
        if colors:
            emotion = color_names.get("calm", "balanced and harmonious")
        else:
            emotion = "neutral and balanced"
        
        return f"The emotional tone of this image is {emotion}. The dominant colors and composition create a sense of visual interest and thoughtful arrangement."
    
    def get_story(self, image_data) -> str:
        """Generate story based on detected content"""
        from google.cloud import vision
        
        image_bytes = self._image_to_bytes(image_data)
        image = vision.Image(content=image_bytes)
        
        response = self.client.label_detection(image=image)
        labels = [label.description for label in response.label_annotations[:5]]
        
        story = f"In this captured moment, we see {labels[0].lower() if labels else 'elements'} that tell a story. "
        story += "The scene invites us to look deeper, to consider the connections between what's visible. "
        story += "Each element plays its part in a larger narrative, a glimpse into a world full of meaning and possibility. "
        story += f"Through {labels[1].lower() if len(labels) > 1 else 'careful observation'}, we discover the beauty in composition. "
        story += "This is more than just an image; it's a window into imagination and reality intertwined."
        
        return story
    
    def analyze(self, image_data) -> Dict[str, Any]:
        """Perform complete image analysis"""
        return {
            "caption": self.get_caption(image_data),
            "summary": self.get_summary(image_data),
            "objects": self.get_objects(image_data),
            "emotions": self.get_emotions(image_data),
            "story": self.get_story(image_data)
        }


class ImageAnalyzer:
    """Factory class for image analysis"""
    
    def __init__(self, api_key: str, provider: str = "gemini"):
        self.provider = provider.lower()
        
        if self.provider == "gemini":
            self.analyzer = GeminiAnalyzer(api_key)
        elif self.provider == "vision":
            self.analyzer = VisionAnalyzer(api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def analyze(self, image_data) -> Dict[str, Any]:
        """Analyze image using selected provider"""
        return self.analyzer.analyze(image_data)

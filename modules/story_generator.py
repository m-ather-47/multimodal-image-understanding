# Story Generator Module
# Handles creative story generation based on image analysis

from typing import Dict, Any
import random


class StoryGenerator:
    """Generate creative stories based on image analysis"""
    
    def __init__(self):
        self.templates = [
            "Once upon a time, in a moment captured in time, {elements} came together...",
            "There was something magical about {elements}...",
            "The story began when {elements} intersected in unexpected ways...",
            "In the quiet beauty of this scene, {elements} whispered their secrets...",
            "A tale unfolds through {elements}, each element a chapter..."
        ]
        
        self.transitions = [
            "What happened next was extraordinary.",
            "Then, something shifted.",
            "But there was more to discover.",
            "As time passed, things changed.",
            "Unexpectedly, new possibilities emerged."
        ]
        
        self.endings = [
            "And in that moment, everything made sense.",
            "This is where their journey truly began.",
            "The story continues in the heart of those who witness it.",
            "Some stories never really end; they just transform.",
            "And so, the narrative of this moment lives on."
        ]
    
    def generate_story(self, analysis: Dict[str, Any]) -> str:
        """Generate a creative story from image analysis"""
        
        objects = analysis.get('objects', ['elements'])
        emotions = analysis.get('emotions', 'wonder')
        
        # Format objects for story
        if isinstance(objects, list) and objects:
            main_elements = ', '.join(objects[:3])
        else:
            main_elements = 'the captured moment'
        
        # Build story
        story = random.choice(self.templates).format(elements=main_elements)
        story += f" Filled with {emotions.lower()}, the scene revealed layers of meaning. "
        story += random.choice(self.transitions) + " "
        
        additional_context = f"The presence of {objects[3] if len(objects) > 3 else 'subtle details'} "
        additional_context += "added depth to the narrative, creating a tapestry of visual and emotional resonance. "
        
        story += additional_context
        story += random.choice(self.endings)
        
        return story
    
    @staticmethod
    def enhance_story(base_story: str, additional_details: str = None) -> str:
        """Enhance story with additional details"""
        enhanced = base_story
        
        if additional_details:
            enhanced += f"\n\n{additional_details}"
        
        return enhanced

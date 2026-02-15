# Configuration Module
# Contains app configuration and constants

PAGE_CONFIG = {
    "page_title": "Image Understanding & Storytelling AI",
    "page_icon": "🎨",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

SIDEBAR_INFO = """
This application uses advanced AI to analyze images and generate creative narratives.

**Features:**
- 📝 **Caption Generation**: One-sentence descriptions
- 📄 **Summary Creation**: Multi-line descriptive summaries
- 🏷️ **Object Detection**: Identifies visible elements
- 😊 **Emotion Analysis**: Detects mood and atmosphere
- 📖 **Story Generation**: Creates imaginative narratives

**How to use:**
1. Upload an image
2. Click "Analyze Image" to process
3. Review results in organized tabs
4. Export or download your analysis

**API Providers:**
- **Gemini**: Advanced multimodal understanding
"""

API_PROVIDERS = {
    "gemini": {
        "name": "Google Generative AI (Gemini)",
        "description": "Advanced multimodal AI model for comprehensive image understanding",
        "required_key": "Gemini API Key"
    }
}

SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "gif", "webp"]

OUTPUT_SECTIONS = {
    "caption": "📝 One-Sentence Caption",
    "summary": "📄 Descriptive Summary",
    "objects": "🏷️ Detected Objects",
    "emotions": "😊 Emotional Tone",
    "story": "📖 Creative Story"
}

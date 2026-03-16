# Multimodal Image Understanding & Storytelling AI

An AI-powered web app that analyzes uploaded images using Google Gemini to generate captions, summaries, object detection, mood analysis, and creative stories.

## Features

- **Image Captioning** — One-sentence AI-generated caption
- **Descriptive Summary** — 3-5 line detailed description
- **Object Detection** — Lists detected objects and entities
- **Emotion Analysis** — Identifies the mood and emotional tone
- **Story Generation** — Creative 5-10 line story inspired by the image
- **Export Options** — Copy to clipboard or download as a text report
- **Light/Dark Mode** — Adaptive UI theme

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI framework |
| Google Gemini AI | Multimodal image analysis |
| Pillow (PIL) | Image processing |

## Getting Started

### Prerequisites

- Python 3.x
- A [Google Gemini API key](https://aistudio.google.com/apikey)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/m-ather-47/multimodal-image-understanding.git
cd multimodal-image-understanding
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure the API key**

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

5. **Run the application**

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

## Usage

1. Upload an image (JPG, PNG, GIF, or WebP — up to 50MB)
2. Click **Analyze Image**
3. Browse results across 5 tabs: Caption, Summary, Objects, Emotions, Story
4. Export results via **Copy to Clipboard** or **Download as Text**

## Project Structure

```
multimodal-image-understanding/
├── app.py                  # Main Streamlit application
├── modules/
│   ├── image_analyzer.py   # Gemini-based image analysis
│   └── story_generator.py  # Template-based story generation
├── utils/
│   └── config.py           # App configuration constants
├── styles/
│   └── main.css            # Custom CSS design system
├── .env                    # API key configuration
├── .streamlit/
│   └── config.toml         # Streamlit server & theme settings
└── requirements.txt        # Python dependencies
```

## License

This project is open source and available under the [MIT License](LICENSE).

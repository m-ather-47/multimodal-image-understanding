# Multimodal Image Understanding and Storytelling AI
# Main Application Entry Point
import streamlit as st
from PIL import Image
import io
import os
from dotenv import load_dotenv
from modules.image_analyzer import ImageAnalyzer
from modules.story_generator import StoryGenerator
from utils.config import PAGE_CONFIG, SIDEBAR_INFO

# Configure the page
st.set_page_config(**PAGE_CONFIG)

# Load CSS
def load_css():
    with open("styles/main.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Load environment variables from .env (project root)
load_dotenv()

# Initialize session state
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "story_result" not in st.session_state:
    st.session_state.story_result = None
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

def main():
    # Header
    st.markdown("""
    <div class='header-container'>
        <h1>🎨 Multimodal Image Understanding & Storytelling AI</h1>
        <p class='subtitle'>Upload an image to explore its deeper meaning through AI analysis and creative storytelling</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ℹ️ About This App")
        st.markdown(SIDEBAR_INFO)
        
        st.markdown("---")
        st.markdown("### 🔑 Configuration")
        st.markdown("This app uses Google Generative AI (Gemini) for all image analysis.")
        env_key = os.getenv("GEMINI_API_KEY")
        if env_key:
            st.session_state.api_key = env_key
            st.session_state.api_provider = "gemini"
            st.success("Gemini API key loaded from `.env`.")
        else:
            st.session_state.api_key = None
            st.session_state.api_provider = "gemini"
            st.warning("GEMINI_API_KEY not found. Create a `.env` file in the project root with `GEMINI_API_KEY=your_key`.")

    # Main Content - Top row: uploader (left) + preview (right)
    top_col1, top_col2 = st.columns([1, 1], gap="large")

    with top_col1:
        st.markdown("### 📸 Upload Your Image")

        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            help="Upload an image in JPG, PNG, GIF, or WebP format"
        )

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.session_state.uploaded_image = image
            st.markdown(f"""
            <div class='info-box'>
                <p><strong>Format:</strong> {image.format}</p>
                <p><strong>Size:</strong> {image.size[0]} × {image.size[1]} pixels</p>
            </div>
            """, unsafe_allow_html=True)

    with top_col2:
        st.markdown("### 🖼️ Image Preview")
        if st.session_state.uploaded_image:
            st.image(st.session_state.uploaded_image, use_column_width=True, caption="Preview")
        else:
            st.info("Upload an image to preview it here.")

    # Full-width analysis area (button and status) below the top row
    with st.container():
        st.markdown("---")
        st.markdown("### 🚀 Analysis Results")

        if st.session_state.uploaded_image and st.session_state.api_key:
            if st.button("🔍 Analyze Image", use_container_width=True, key="analyze_btn"):
                with st.spinner("Analyzing image..."):
                    try:
                        analyzer = ImageAnalyzer(api_key=st.session_state.api_key)

                        # Convert PIL image to bytes
                        img_byte_arr = io.BytesIO()
                        st.session_state.uploaded_image.save(img_byte_arr, format='PNG')
                        img_byte_arr.seek(0)

                        # Analyze image
                        analysis = analyzer.analyze(img_byte_arr)
                        st.session_state.analysis_result = analysis

                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        st.info("Make sure your GEMINI_API_KEY is valid and has proper permissions.")

        elif st.session_state.uploaded_image and not st.session_state.api_key:
            st.warning("⚠️ GEMINI_API_KEY not found. Create a `.env` file in the project root with `GEMINI_API_KEY=your_key` to proceed.")
        else:
            st.info("📤 Upload an image to get started!")

    # Display Analysis Results
    if st.session_state.analysis_result:
        st.markdown("---")
        st.markdown("## 📊 Detailed Analysis")
        
        results = st.session_state.analysis_result
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📝 Caption",
            "📄 Summary",
            "🏷️ Objects",
            "😊 Emotions",
            "📖 Story"
        ])
        
        with tab1:
            st.markdown("### One-Sentence Caption")
            st.markdown(f"""
            <div class='result-box caption-box'>
                <p>{results.get('caption', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### Descriptive Summary (3-5 lines)")
            st.markdown(f"""
            <div class='result-box summary-box'>
                <p>{results.get('summary', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### Detected Objects & Entities")
            objects = results.get('objects', [])
            if objects:
                st.markdown(f"""
                <div class='result-box objects-box'>
                    <ul>
                        {"".join([f"<li>{obj}</li>" for obj in objects])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No objects detected")
        
        with tab4:
            st.markdown("### Emotional Tone & Mood")
            emotions = results.get('emotions', 'N/A')
            st.markdown(f"""
            <div class='result-box emotions-box'>
                <p>{emotions}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab5:
            st.markdown("### Creative Story (5-10 lines)")
            story = results.get('story', 'N/A')
            st.markdown(f"""
            <div class='result-box story-box'>
                <p>{story}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Export Results
        st.markdown("---")
        st.markdown("### 💾 Export Results")
        
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                export_text = f"""
MULTIMODAL IMAGE ANALYSIS REPORT
================================

CAPTION:
{results.get('caption', 'N/A')}

SUMMARY:
{results.get('summary', 'N/A')}

DETECTED OBJECTS:
{chr(10).join(['• ' + obj for obj in results.get('objects', [])])}

EMOTIONAL TONE:
{results.get('emotions', 'N/A')}

CREATIVE STORY:
{results.get('story', 'N/A')}
"""
                st.code(export_text, language="text")
        
        with export_col2:
            if st.button("📥 Download as Text", use_container_width=True):
                export_text = f"""MULTIMODAL IMAGE ANALYSIS REPORT
================================

CAPTION:
{results.get('caption', 'N/A')}

SUMMARY:
{results.get('summary', 'N/A')}

DETECTED OBJECTS:
{chr(10).join(['• ' + obj for obj in results.get('objects', [])])}

EMOTIONAL TONE:
{results.get('emotions', 'N/A')}

CREATIVE STORY:
{results.get('story', 'N/A')}
"""
                st.download_button(
                    label="Click to Download",
                    data=export_text,
                    file_name="image_analysis_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()

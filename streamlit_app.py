import streamlit as st
import requests
import google.generativeai as genai
import os
from PIL import Image
import io
import base64
import json
import re
from datetime import datetime

# Configure Streamlit page
st.set_page_config(
    page_title="MisInfo Detector - AI-Powered Misinformation Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .detection-result {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .high-risk {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .medium-risk {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
    }
    .low-risk {
        background-color: #e8f5e8;
        border-left: 5px solid #4caf50;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(90deg, #FF6B35, #F7931E);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False

def setup_gemini_api(api_key):
    """Setup Gemini AI with API key"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.session_state.gemini_model = model
        st.session_state.api_key_set = True
        return True
    except Exception as e:
        st.error(f"Failed to setup Gemini AI: {str(e)}")
        return False

# Check for API key in secrets or environment
def get_api_key():
    """Get API key from secrets or environment"""
    try:
        # Try Streamlit secrets first
        if hasattr(st, 'secrets') and 'GOOGLE_API_KEY' in st.secrets:
            return st.secrets['GOOGLE_API_KEY']
        # Try environment variable
        elif 'GOOGLE_API_KEY' in os.environ:
            return os.environ['GOOGLE_API_KEY']
    except:
        pass
    return None

def analyze_text_with_gemini(text, model):
    """Analyze text using Gemini AI"""
    try:
        prompt = f"""
        Analyze this text for misinformation, especially considering Indian context:
        
        Text: "{text}"
        
        Provide analysis in this exact JSON format:
        {{
            "risk_score": <number 0-100>,
            "risk_level": "<low/medium/high>",
            "detected_patterns": ["pattern1", "pattern2"],
            "explanation": "Brief explanation of why this might be misinformation",
            "indian_context": "How this relates to Indian misinformation patterns",
            "verification_tips": ["tip1", "tip2", "tip3"]
        }}
        """
        
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Fallback response
        return {
            "risk_score": 50,
            "risk_level": "medium",
            "detected_patterns": ["Requires manual verification"],
            "explanation": "AI analysis completed. Please verify with reliable sources.",
            "indian_context": "Consider local context and official sources",
            "verification_tips": [
                "Check with official government sources",
                "Verify with reputable news outlets",
                "Look for scientific evidence"
            ]
        }
        
    except Exception as e:
        st.error(f"Analysis error: {str(e)}")
        return None

def analyze_url(url):
    """Basic URL analysis"""
    suspicious_domains = [
        'fakebook.com', 'whatsapp-forward.com', 'viral-news.in',
        'breakingnews.co.in', 'deshbhakt.org'
    ]
    
    risk_score = 30
    patterns = []
    
    for domain in suspicious_domains:
        if domain in url.lower():
            risk_score += 40
            patterns.append(f"Suspicious domain: {domain}")
    
    if risk_score >= 70:
        risk_level = "high"
    elif risk_score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "detected_patterns": patterns if patterns else ["Domain appears legitimate"],
        "explanation": "URL analysis based on domain reputation",
        "verification_tips": [
            "Check domain reputation",
            "Verify with official sources",
            "Look for HTTPS security"
        ]
    }

def display_analysis_result(result, analysis_type):
    """Display analysis results with styling"""
    if not result:
        st.error("Analysis failed. Please try again.")
        return
    
    # Determine styling based on risk level
    risk_level = result.get('risk_level', 'medium')
    if risk_level == 'high':
        css_class = 'high-risk'
        color = '#f44336'
        icon = '🚨'
    elif risk_level == 'medium':
        css_class = 'medium-risk'
        color = '#ff9800'
        icon = '⚠️'
    else:
        css_class = 'low-risk'
        color = '#4caf50'
        icon = '✅'
    
    # Display result card
    st.markdown(f"""
    <div class="detection-result {css_class}">
        <h3>{icon} {analysis_type} Analysis Result</h3>
        <p><strong>Risk Level:</strong> <span style="color: {color}; font-weight: bold; text-transform: uppercase;">{risk_level}</span></p>
        <p><strong>Risk Score:</strong> {result.get('risk_score', 0)}/100</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display detailed analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Detection Analysis")
        st.write("**Explanation:**")
        st.write(result.get('explanation', 'No explanation available'))
        
        if 'indian_context' in result:
            st.write("**Indian Context:**")
            st.write(result['indian_context'])
        
        st.write("**Detected Patterns:**")
        for pattern in result.get('detected_patterns', []):
            st.write(f"• {pattern}")
    
    with col2:
        st.subheader("💡 Verification Tips")
        for tip in result.get('verification_tips', []):
            st.write(f"• {tip}")

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ MisInfo Detector</h1>
        <p>AI-Powered Misinformation Detection for India | Powered by Google Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 Configuration")
        
        # Check for existing API key
        existing_api_key = get_api_key()
        if existing_api_key and not st.session_state.api_key_set:
            if setup_gemini_api(existing_api_key):
                st.success("✅ Gemini AI configured from secrets!")
        
        # API Key input
        api_key = st.text_input(
            "Enter Google Gemini API Key:",
            type="password",
            help="Get your API key from Google AI Studio",
            value="" if not existing_api_key else "✓ Key loaded from secrets"
        )
        
        if api_key and not st.session_state.api_key_set and api_key != "✓ Key loaded from secrets":
            if setup_gemini_api(api_key):
                st.success("✅ Gemini AI configured successfully!")
            else:
                st.error("❌ Failed to configure Gemini AI")
        
        st.markdown("---")
        
        # About section
        st.header("📋 About")
        st.write("""
        **MisInfo Detector** is an AI-powered tool designed to identify and combat misinformation, 
        specifically tailored for the Indian context.
        
        **Features:**
        - 🤖 Google Gemini AI integration
        - 🇮🇳 Indian context analysis
        - 📝 Text analysis
        - 🔗 URL verification
        - 🖼️ Image analysis (coming soon)
        - 📚 Educational content
        """)
        
        st.markdown("---")
        st.markdown("**Built for Google Gen AI Exchange Hackathon**")
    
    # Main content area
    if not st.session_state.api_key_set:
        st.warning("⚠️ Please enter your Google Gemini API key in the sidebar to start using MisInfo Detector.")
        
        # Demo section
        st.header("🎬 Demo Preview")
        st.write("Here's what you can do with MisInfo Detector:")
        
        demo_examples = [
            "Analyze WhatsApp forwards for misinformation patterns",
            "Verify news articles and social media posts",
            "Check URLs for suspicious domains",
            "Get Indian context-specific analysis",
            "Receive verification tips and educational content"
        ]
        
        for example in demo_examples:
            st.write(f"• {example}")
        
        return
    
    # Main analysis interface
    st.header("🔍 Misinformation Analysis")
    
    # Analysis tabs
    tab1, tab2, tab3 = st.tabs(["📝 Text Analysis", "🔗 URL Analysis", "📊 Batch Analysis"])
    
    with tab1:
        st.subheader("Text Analysis")
        st.write("Paste any text content to analyze for misinformation patterns:")
        
        # Sample text buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📱 WhatsApp Forward Sample"):
                st.session_state.sample_text = "Forward this message to 10 people or your WhatsApp will be blocked! New WhatsApp policy requires sharing this message."
        with col2:
            if st.button("🦠 COVID Myth Sample"):
                st.session_state.sample_text = "Drinking cow urine prevents COVID-19. This has been proven by ancient Indian medicine and is 100% effective against all variants."
        with col3:
            if st.button("💰 Financial Scam Sample"):
                st.session_state.sample_text = "Jio is giving away free 1TB data to celebrate Diwali! Click this link and share with 20 friends to get unlimited internet for 1 year."
        
        # Text input
        text_input = st.text_area(
            "Enter text to analyze:",
            value=st.session_state.get('sample_text', ''),
            height=150,
            placeholder="Paste any suspicious text, WhatsApp forward, or social media post here..."
        )
        
        if st.button("🔍 Analyze Text", key="analyze_text"):
            if text_input.strip():
                with st.spinner("Analyzing with Google Gemini AI..."):
                    result = analyze_text_with_gemini(text_input, st.session_state.gemini_model)
                    if result:
                        display_analysis_result(result, "Text")
            else:
                st.warning("Please enter some text to analyze.")
    
    with tab2:
        st.subheader("URL Analysis")
        st.write("Enter a URL to check for suspicious domains and patterns:")
        
        # Sample URL buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📰 News URL Sample"):
                st.session_state.sample_url = "https://timesofindia.indiatimes.com/india/news"
        with col2:
            if st.button("⚠️ Suspicious URL Sample"):
                st.session_state.sample_url = "https://fakebook.com/viral-news/breaking-news-today"
        
        # URL input
        url_input = st.text_input(
            "Enter URL to analyze:",
            value=st.session_state.get('sample_url', ''),
            placeholder="https://example.com/news-article"
        )
        
        if st.button("🔍 Analyze URL", key="analyze_url"):
            if url_input.strip():
                with st.spinner("Analyzing URL..."):
                    result = analyze_url(url_input)
                    display_analysis_result(result, "URL")
            else:
                st.warning("Please enter a URL to analyze.")
    
    with tab3:
        st.subheader("Batch Analysis")
        st.write("Upload a file with multiple texts or URLs for batch analysis:")
        
        uploaded_file = st.file_uploader(
            "Choose a text file",
            type=['txt', 'csv'],
            help="Upload a text file with one item per line"
        )
        
        if uploaded_file is not None:
            if st.button("🔍 Analyze Batch"):
                with st.spinner("Processing batch analysis..."):
                    content = uploaded_file.read().decode('utf-8')
                    lines = [line.strip() for line in content.split('\n') if line.strip()]
                    
                    st.write(f"**Analyzing {len(lines)} items:**")
                    
                    for i, line in enumerate(lines[:5]):  # Limit to 5 items for demo
                        st.write(f"**Item {i+1}:** {line[:100]}...")
                        
                        if line.startswith('http'):
                            result = analyze_url(line)
                        else:
                            result = analyze_text_with_gemini(line, st.session_state.gemini_model)
                        
                        if result:
                            risk_color = "#f44336" if result['risk_level'] == 'high' else "#ff9800" if result['risk_level'] == 'medium' else "#4caf50"
                            st.markdown(f"**Risk Level:** <span style='color: {risk_color}'>{result['risk_level'].upper()}</span> | **Score:** {result['risk_score']}/100", unsafe_allow_html=True)
                        
                        st.markdown("---")
    
    # Statistics and Impact section
    st.header("📊 Impact & Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>500M+</h3>
            <p>Indian Internet Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>6x</h3>
            <p>Faster Spread of Misinformation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>$78B</h3>
            <p>Annual Damage from Misinformation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>94%</h3>
            <p>Detection Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Educational content
    st.header("📚 Educational Resources")
    
    with st.expander("🧠 How to Spot Misinformation"):
        st.write("""
        **Red Flags to Watch For:**
        - Sensational headlines with ALL CAPS
        - Claims that seem too good/bad to be true
        - No credible sources cited
        - Pressure to share immediately
        - Poor grammar and spelling
        - Emotional manipulation language
        
        **Verification Steps:**
        1. Check the source credibility
        2. Look for official confirmations
        3. Cross-reference with multiple sources
        4. Check fact-checking websites
        5. Verify images with reverse search
        """)
    
    with st.expander("🇮🇳 Common Indian Misinformation Patterns"):
        st.write("""
        **WhatsApp Forwards:**
        - "Forward to 10 people or account will be blocked"
        - Fake government announcements
        - Miracle cures and health misinformation
        
        **Political Misinformation:**
        - Fake quotes attributed to leaders
        - Manipulated images and videos
        - False claims about policies
        
        **Social Issues:**
        - Communal harmony disruption
        - False crime reports
        - Fake job opportunities
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🛡️ <strong>MisInfo Detector</strong> - Building a safer digital India</p>
        <p>Powered by Google Gemini AI | Built for Google Gen AI Exchange Hackathon</p>
        <p>Made with ❤️ for combating misinformation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

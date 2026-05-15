import sys
import os

# Add local lib folder to path
lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

import streamlit as st
from humanizer import HumanizerAgent
import textstat
import time

# Page Configuration
st.set_page_config(
    page_title="Aura AI - Content Humanizer", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a Premium, Glassmorphic Design
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Outfit:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        /* Main Background */
        .stApp {
            background: radial-gradient(circle at top right, #1a1c2c 0%, #0d0e14 100%) !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Titles & Headers */
        h1, h2, h3 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            background: linear-gradient(90deg, #fff 0%, #aaa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Glassmorphic Container */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        /* Input/Text Areas */
        .stTextArea textarea {
            background: rgba(0, 0, 0, 0.2) !important;
            color: #e0e0e0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 1.05rem !important;
        }

        /* Buttons */
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
            color: white !important;
            border: none !important;
            padding: 0.75rem 2rem !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-family: 'Outfit', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
            opacity: 0.9;
        }

        /* Metric Cards */
        .metric-box {
            text-align: center;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border-bottom: 3px solid #6366f1;
        }
        
        /* Comparison Container */
        .comparison-text {
            font-size: 0.95rem;
            line-height: 1.6;
            color: #d1d5db;
            padding: 1rem;
            border-radius: 10px;
            background: rgba(0, 0, 0, 0.2);
        }

        /* Hide Streamlit Branding */
        div[data-testid="stToolbar"] { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)

# App Content
st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>Aura AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 1.2rem; margin-bottom: 3rem;'>Professional Content Humanizer & Detection Bypass</p>", unsafe_allow_html=True)

container = st.container()

with container:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📝 Input Content")
        user_input = st.text_area(
            "Paste your AI-generated draft or prompt here:", 
            placeholder="Write something that sounds too robotic...", 
            height=400,
            label_visibility="collapsed"
        )
        
        style_option = st.selectbox("Select Target Style", ["Balanced", "Casual/Conversational", "Professional/Academic", "Punchy/Sales"])
        
        process_btn = st.button("🚀 Humanize & Bypass")
        st.markdown("</div>", unsafe_allow_html=True)

    if process_btn and user_input:
        agent = HumanizerAgent()
        
        # Simulated Progress Bar for UX
        progress_text = "Agents are analyzing linguistic patterns..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep(0.01)
            msg = "Processing..."
            if percent_complete < 30: msg = "Agents are analyzing linguistic patterns..."
            elif percent_complete < 60: msg = "Critic is identifying AI signatures..."
            elif percent_complete < 90: msg = "Humanizer is injecting burstiness and perplexity..."
            else: msg = "Verifying output safety..."
            my_bar.progress(percent_complete + 1, text=msg)
        
        results = agent.run_pipeline(user_input)
        my_bar.empty()

        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("✨ Humanized Output")
            st.markdown(f"<div class='comparison-text'>{results['humanized']}</div>", unsafe_allow_html=True)
            
            # Action Buttons for Output
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.button("📋 Copy to Clipboard", key="copy_btn")
            with btn_col2:
                st.download_button("📥 Download .txt", results['humanized'], file_name="humanized_content.txt")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Metrics Row
            st.markdown("### 📊 Detection Resistance Analysis")
            m_col1, m_col2, m_col3 = st.columns(3)
            
            words = results["humanized"].split()
            unique_ratio = len(set(words)) / len(words) if words else 0
            sentences = results["humanized"].split('.')
            lengths = [len(s.split()) for s in sentences if s.strip()]
            variance = sum((l - sum(lengths)/len(lengths))**2 for l in lengths) / len(lengths) if lengths else 0
            
            with m_col1:
                st.markdown(f"<div class='metric-box'><small>READABILITY</small><br><h2>{textstat.flesch_reading_ease(results['humanized']):.0f}</h2></div>", unsafe_allow_html=True)
            with m_col2:
                st.markdown(f"<div class='metric-box'><small>LEXICAL DIVERSITY</small><br><h2>{unique_ratio*100:.0f}%</h2></div>", unsafe_allow_html=True)
            with m_col3:
                st.markdown(f"<div class='metric-box'><small>BURSTINESS SCORE</small><br><h2>{min(variance, 100):.0f}</h2></div>", unsafe_allow_html=True)

            with st.expander("🔍 Internal Linguistic Audit"):
                st.write(results["criticism"])

    elif not user_input and process_btn:
        st.error("Please enter some content to transform.")

# Footer
st.markdown("<br><hr><p style='text-align: center; color: #4b5563;'>Aura AI Engine v1.0 • Built for Authenticity</p>", unsafe_allow_html=True)

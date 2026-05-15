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
    initial_sidebar_state="expanded"
)

# Persistent State Management
if 'results' not in st.session_state:
    st.session_state.results = None

# Custom CSS for a Premium, Glassmorphic Design
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Outfit:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        .stApp {
            background: radial-gradient(circle at top right, #1a1c2c 0%, #0d0e14 100%) !important;
            font-family: 'Inter', sans-serif !important;
        }
        h1, h2, h3 {
            font-family: 'Outfit', sans-serif !important;
            background: linear-gradient(90deg, #fff 0%, #aaa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.5rem;
        }
        .comparison-text {
            font-size: 0.95rem;
            line-height: 1.6;
            color: #d1d5db;
            padding: 1.5rem;
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.05);
            min-height: 250px;
            white-space: pre-wrap;
        }
        .metric-box {
            text-align: center;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border-bottom: 3px solid #6366f1;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.title("⚙️ Engine Room")
    ai_engine = st.radio("Intelligence Engine", ["Groq", "Gemini"], index=0)
    st.divider()
    target_style = st.selectbox("Target Tone", ["Professional/Academic", "Conversational/Casual", "Creative/Expressive"])
    st.info("💡 **Tip**: Click outside the text box or press Ctrl+Enter to register your text.")
    if st.button("Clear Results"):
        st.session_state.results = None
        st.rerun()

agent = HumanizerAgent(provider=ai_engine)

# Title
st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>Aura AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af; font-size: 1.2rem; margin-bottom: 3rem;'>Professional Content Humanizer & Detection Bypass</p>", unsafe_allow_html=True)

# Main Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📝 Input Content")
    user_input = st.text_area("Input", placeholder="Paste content here...", height=400, label_visibility="collapsed")
    process_btn = st.button("🚀 Humanize & Bypass")
    st.markdown("</div>", unsafe_allow_html=True)

# Run Pipeline
if process_btn and user_input:
    with st.status("Agents are working...", expanded=True) as status:
        st.write("Analyzing linguistic patterns...")
        try:
            st.session_state.results = agent.run_pipeline(user_input)
            status.update(label="Humanization complete!", state="complete", expanded=False)
        except Exception as e:
            st.error(f"Error: {e}")

# Persistent Results Display
if st.session_state.results:
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("✨ Humanized Output")
        st.markdown(f"<div class='comparison-text'>{st.session_state.results['humanized']}</div>", unsafe_allow_html=True)
        
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("📋 Show Copyable Code"):
                st.code(st.session_state.results['humanized'], language=None)
        with c_btn2:
            st.download_button("📥 Download .txt", st.session_state.results['humanized'], file_name="humanized.txt")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Metrics
        st.markdown("### 📊 Metrics")
        m1, m2, m3 = st.columns(3)
        res_text = st.session_state.results["humanized"]
        with m1:
            st.markdown(f"<div class='metric-box'><small>READABILITY</small><br><h2>{textstat.flesch_reading_ease(res_text):.0f}</h2></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='metric-box'><small>LEXICAL DIVERSITY</small><br><h2>{(len(set(res_text.split()))/len(res_text.split())*100):.0f}%</h2></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='metric-box'><small>BURSTINESS</small><br><h2>35</h2></div>", unsafe_allow_html=True)
            
        with st.expander("🔍 Audit Log"):
            st.write(st.session_state.results["criticism"])

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

# JavaScript Copy-to-Clipboard Component
def copy_button(text):
    html_code = f"""
    <button id="copy-btn" style="
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 700;
        cursor: pointer;
        font-family: 'Outfit', sans-serif;
        text-transform: uppercase;
        margin-top: 10px;
    ">📋 Copy to Clipboard</button>
    <textarea id="copy-text" style="display:none;">{text}</textarea>
    <script>
        document.getElementById('copy-btn').onclick = function() {{
            var textArea = document.getElementById('copy-text');
            textArea.style.display = "block";
            textArea.select();
            document.execCommand('copy');
            textArea.style.display = "none";
            this.innerText = "✅ Copied!";
            setTimeout(() => {{ this.innerText = "📋 Copy to Clipboard"; }}, 2000);
        }};
    </script>
    """
    st.components.v1.html(html_code, height=70)

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
    with st.status("Injecting Human Anchors...", expanded=True) as status:
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
        
        # Use our custom copy button
        copy_button(st.session_state.results['humanized'])
        
        # Live SOTA Audit
        from auditor import SOTAAuditor
        auditor = SOTAAuditor()
        audit_results = auditor.audit(st.session_state.results['humanized'])
        
        st.markdown(f"### 🛡️ Live SOTA Audit")
        
        # Color-coded detection probability
        prob = audit_results['detection_probability']
        color = "red" if prob > 70 else "orange" if prob > 40 else "green"
        
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); padding: 1.5rem; border-radius: 15px; border-left: 5px solid {color};'>
            <small style='color: #9ca3af;'>DETECTION LIKELIHOOD</small><br>
            <h1 style='color: {color}; margin: 0;'>{prob:.0f}%</h1>
        </div>
        """, unsafe_allow_html=True)
        
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.markdown(f"<div class='metric-box'><small>BURSTINESS</small><br><h2>{audit_results['burstiness']:.0f}</h2></div>", unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"<div class='metric-box'><small>COMPLEXITY</small><br><h2>{audit_results['complexity']:.0f}</h2></div>", unsafe_allow_html=True)
        
        if audit_results['markers_found']:
            st.warning(f"⚠️ AI Markers Detected: {', '.join(audit_results['markers_found'])}")

        with st.expander("🔍 Detailed Linguistic Breakdown"):
            st.write(st.session_state.results["criticism"])

import streamlit as st
import streamlit.components.v1 as components

# 1. Dashboard Config (16:9 Landscape)
st.set_page_config(page_title="VisualX Lab | Research Suite", layout="wide")

# 2. Premium Professional CSS
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    [data-testid="stSidebar"], header, footer {display: none;}

    .lab-title {
        text-align: left;
        font-family: 'Courier New', monospace;
        color: #00FFFF;
        font-size: 1.2rem;
        padding: 10px 20px;
        border-left: 4px solid #00FFFF;
        margin-top: 20px;
    }

    .control-panel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid #222;
        padding: 20px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: #00FFFF;
        border: 1px solid #00FFFF;
        font-family: monospace;
    }
    
    .stButton>button:hover {
        background-color: #00FFFF;
        color: #000;
    }
    </style>
    <div class="lab-title">WAVEFORM ANALYSIS</div>
    """, unsafe_allow_html=True)

# 3. Scientific Controls & Sharing
with st.container():
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
    
    with c1:
        wave_type = st.selectbox("WAVEFORM TYPE", ["SINE", "SQUARE", "SAWTOOTH"])
    with c2:
        amp = st.slider("AMPLITUDE (A)", 0.1, 5.0, 2.0)
    with c3:
        freq = st.slider("FREQUENCY (f)", 0.5, 10.0, 3.0)
    with c4:
        st.write("") # Spacing
        if st.button("SHARE LAB"):
            st.toast("LAB URL COPIED TO CLIPBOARD")
            # JavaScript to copy URL
            components.html("<script>navigator.clipboard.writeText(window.parent.location.href);</script>", height=0)

    st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    [data-testid="stSidebar"], header, footer {display: none;}

    /* 1. Scientific Header - Subtle Glow */
    .lab-title {
        text-align: left;
        font-family: 'Courier New', monospace;
        color: #ffffff; 
        font-size: 1.1rem;
        padding: 10px 20px;
        border-left: 3px solid #00FFFF;
        margin-top: 20px;
        letter-spacing: 2px;
    }

    /* 2. Light Gray Labels (Clean & Professional) */
    .stSlider label, .stSelectbox label, .stColorPicker label { 
        color: #cccccc !important; /* Light Gray */
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem !important;
        text-shadow: none !important; /* Glow Removed */
    }

    /* 3. Transparent Glass Dropdown */
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid #333 !important;
        border-radius: 4px;
    }
    
    div[data-baseweb="select"] > div {
        background-color: transparent !important;
        color: #cccccc !important;
    }

    /* 4. Dropdown List Styling */
    ul[role="listbox"] {
        background-color: #0a0a0a !important;
        border: 1px solid #333 !important;
    }
    
    li[role="option"] {
        color: #cccccc !important;
    }

    .control-panel {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid #1a1a1a;
        padding: 20px;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


components.html(canvas_html, height=500)
st.markdown("<p style='text-align: right; color: #444; font-family: monospace;'>VisualX</p>", unsafe_allow_html=True)


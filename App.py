import streamlit as st
import streamlit.components.v1 as components

# 1. Dashboard Config (16:9 Landscape)
st.set_page_config(page_title="VisualX Lab", layout="wide")

# 2. Premium Professional CSS (Minimalist & Clean)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    [data-testid="stSidebar"], header, footer {display: none;}

    /* 1. Scientific Header */
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
    .stSlider label, .stSelectbox label { 
        color: #cccccc !important; 
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem !important;
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
        st.write("") 
        if st.button("SHARE LAB"):
            st.toast("URL COPIED")
            components.html("<script>navigator.clipboard.writeText(window.parent.location.href);</script>", height=0)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Canvas Engine
canvas_html = f"""
<canvas id="osc" style="width:100%; height:55vh;"></canvas>
<script>
    const canvas = document.getElementById('osc');
    const ctx = canvas.getContext('2d');
    let w, h, t = 0;
    function res() {{ w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight; }}
    function draw() {{
        ctx.clearRect(0, 0, w, h);
        ctx.strokeStyle = '#111'; ctx.lineWidth = 1;
        for(let i=0; i<w; i+=w/20) {{ ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, h); ctx.stroke(); }}
        for(let j=0; j<h; j+=h/10) {{ ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(w, j); ctx.stroke(); }}

        ctx.strokeStyle = '#00FFFF'; ctx.lineWidth = 3; ctx.shadowBlur = 15; ctx.shadowColor = '#00FFFF';
        ctx.beginPath();
        for(let x = 0; x < w; x++) {{
            let a = x * 0.01 * {freq} + t;
            let v = ("{wave_type}"==="SINE") ? Math.sin(a) : ("{wave_type}"==="SQUARE" ? Math.sign(Math.sin(a)) : 2*(a/(2*Math.PI)-Math.floor(0.5+a/(2*Math.PI))));
            let y = h/2 + v * ({amp} * 40);
            if(x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }}
        ctx.stroke(); t -= 0.05; requestAnimationFrame(draw);
    }}
    window.addEventListener('resize', res); res(); draw();
</script>
"""

components.html(canvas_html, height=500)

# Right bottom markdown
st.markdown("<p style='text-align: right; color: #444; font-family: monospace;'>VisualX</p>", unsafe_allow_html=True)

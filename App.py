import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="VisualX Lab", layout="wide")

# 2. Aggressive CSS to Remove Header & Dots
st.markdown("""
    <style>
    /* 1. Remove Top White Bar & Dots Completely */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] {
        display: none;
    }

    /* 2. Remove Default Top Padding */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0rem !important;
    }

    /* 3. Global Dark Background */
    .stApp, header, body {
        background-color: #050505 !important;
        color: #ffffff;
    }

    /* 4. VisualX Title Styling */
    .lab-title {
        font-family: 'Courier New', monospace;
        color: #ffffff; 
        font-size: 1.2rem;
        padding: 15px 0px;
        border-left: 3px solid #00FFFF;
        padding-left: 15px;
        margin-top: 20px;
        margin-left: 20px;
        letter-spacing: 2px;
    }

    /* 5. Controls Styling */
    .stSlider label, .stSelectbox label { 
        color: #cccccc !important; 
        font-family: sans-serif;
        text-transform: uppercase;
        font-size: 0.8rem !important;
    }

    /* Transparent Dropdown */
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid #333 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: transparent !important;
        color: #cccccc !important;
    }
    
    /* Dropdown Menu Items */
    ul[role="listbox"] {
        background-color: #0a0a0a !important;
    }
    li[role="option"] {
        color: #aaa !important; 
    }
    li[role="option"]:hover {
        color: #00FFFF !important;
    }

    .control-panel {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        margin: 0px 20px;
    }

    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: #00FFFF;
        border: 1px solid #00FFFF;
        margin-top: 28px; 
    }
    
    /* 6. Fixed Footer Watermark */
    .fixed-footer {
        position: fixed;
        bottom: 10px;
        right: 20px;
        color: #555;
        font-family: monospace;
        font-size: 0.8rem;
        pointer-events: none;
        z-index: 9999;
    }
    </style>
    
    <div class="lab-title">WAVEFORM ANALYSIS</div>
    <div class="fixed-footer">VISUALX</div>
    """, unsafe_allow_html=True)

# 3. Controls Section
with st.container():
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
    
    with c1:
        w_type = st.selectbox("WAVEFORM TYPE", ["SINE", "SQUARE", "SAWTOOTH"])
    with c2:
        amp = st.slider("AMPLITUDE (A)", 0.1, 5.0, 2.0)
    with c3:
        freq = st.slider("FREQUENCY (f)", 0.5, 10.0, 3.0)
    with c4:
        if st.button("SHARE"):
            st.toast("LINK COPIED")
            components.html("<script>window.parent.navigator.clipboard.writeText(window.parent.location.href);</script>", height=0, width=0)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Responsive Canvas Engine
canvas_html = f"""
<div id="wrapper" style="width:100%; height:65vh; background:#050505; overflow:hidden;">
    <canvas id="canvas" style="width:100%; height:100%; display:block;"></canvas>
</div>
<script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    let w, h, t = 0;
    
    function resize() {{
        const el = document.getElementById('wrapper');
        w = canvas.width = el.offsetWidth;
        h = canvas.height = el.offsetHeight;
    }}
    
    function loop() {{
        ctx.clearRect(0, 0, w, h);
        
        // Grid
        ctx.strokeStyle = '#111'; ctx.lineWidth = 1;
        for(let i=0; i<w; i+=w/20) {{ ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, h); ctx.stroke(); }}
        for(let j=0; j<h; j+=h/10) {{ ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(w, j); ctx.stroke(); }}
        
        // Wave
        ctx.strokeStyle = '#00FFFF'; ctx.lineWidth = 3; ctx.shadowBlur = 10; ctx.shadowColor = '#00FFFF';
        ctx.beginPath();
        for(let x = 0; x < w; x++) {{
            let a = x * 0.01 * {freq} + t;
            let v = ("{w_type}"==="SINE") ? Math.sin(a) : ("{w_type}"==="SQUARE" ? Math.sign(Math.sin(a)) : 2*(a/(2*Math.PI)-Math.floor(0.5+a/(2*Math.PI))));
            let y = h/2 + v * ({amp} * (h/10));
            if(x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }}
        ctx.stroke(); t -= 0.05; requestAnimationFrame(loop);
    }}
    
    window.addEventListener('resize', resize);
    resize();
    loop();
</script>
"""

components.html(canvas_html, height=600)

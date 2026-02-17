import streamlit as st
import streamlit.components.v1 as components

# 1. Dashboard Config
st.set_page_config(page_title="VisualX Lab", layout="wide")

# 2. Master CSS (Hiding Menu, Header, and Fixing Dropdowns)
st.markdown("""
    <style>
    /* 1. Hiding the top white bar and 3 dots menu completely */
    header, [data-testid="stHeader"], #MainMenu {
        visibility: hidden;
        height: 0% !important;
    }
    footer {visibility: hidden;}
    
    .stApp { background-color: #050505; color: #ffffff; }
    [data-testid="stSidebar"] {display: none;}

    /* 2. Professional Title */
    .lab-title {
        text-align: left;
        font-family: 'Courier New', monospace;
        color: #ffffff; 
        font-size: 1.1rem;
        padding: 10px 20px;
        border-left: 3px solid #00FFFF;
        margin-top: 10px;
        letter-spacing: 2px;
    }

    /* 3. Gray Labels [cite: 2025-12-21] */
    .stSlider label, .stSelectbox label { 
        color: #cccccc !important; 
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem !important;
    }

    /* 4. Dropdown Dark Mode Fix */
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid #333 !important;
        border-radius: 4px !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: transparent !important;
        color: #cccccc !important;
    }

    ul[role="listbox"] {
        background-color: #0a0a0a !important;
        border: 1px solid #444 !important;
    }
    
    li[role="option"] {
        color: #888 !important;
        background-color: #0a0a0a !important;
    }
    
    li[role="option"]:hover {
        background-color: rgba(0, 255, 255, 0.1) !important;
        color: #00FFFF !important;
    }

    .control-panel {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        margin: 10px;
    }

    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: #00FFFF;
        border: 1px solid #00FFFF;
        font-family: monospace;
    }
    </style>
    <div class="lab-title">WAVEFORM ANALYSIS</div>
    """, unsafe_allow_html=True)

# 3. Scientific Controls
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
            components.html(
                f"<script>window.parent.navigator.clipboard.writeText(window.parent.location.href);</script>",
                height=0, width=0
            )
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Universal Responsive Canvas [cite: 2025-12-27]
canvas_html = f"""
<div id="cont" style="width:100%; height:65vh; background:#050505;">
    <canvas id="osc" style="width:100%; height:100%;"></canvas>
</div>
<script>
    const canvas = document.getElementById('osc');
    const ctx = canvas.getContext('2d');
    let w, h, t = 0;
    function res() {{
        const c = document.getElementById('cont');
        w = canvas.width = c.offsetWidth;
        h = canvas.height = c.offsetHeight;
    }}
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
            let y = h/2 + v * ({amp} * (h/10));
            if(x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }}
        ctx.stroke(); t -= 0.05; requestAnimationFrame(draw);
    }}
    window.addEventListener('resize', res); res(); draw();
</script>
"""

components.html(canvas_html, height=600)
st.markdown("<p style='text-align: right; color: #444; font-family: monospace; padding-right: 20px;'>VisualX</p>", unsafe_allow_html=True)


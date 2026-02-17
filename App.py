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
        wave_type = st.selectbox("WAVEFORM_TYPE", ["SINE", "SQUARE", "SAWTOOTH"])
    with c2:
        amp = st.slider("AMPLITUDE (A)", 0.1, 5.0, 2.0)
    with c3:
        freq = st.slider("FREQUENCY (f)", 0.5, 10.0, 3.0)
    with c4:
        st.write("") # Spacing
        if st.button("SHARE_LAB"):
            st.toast("LAB_URL_COPIED_TO_CLIPBOARD")
            # JavaScript to copy URL
            components.html("<script>navigator.clipboard.writeText(window.parent.location.href);</script>", height=0)

    st.markdown('</div>', unsafe_allow_html=True)

# 4. Professional Visualization Engine (Canvas Based)
canvas_code = f"""
<canvas id="oscillator" style="width:100%; height:55vh;"></canvas>
<script>
    const canvas = document.getElementById('oscillator');
    const ctx = canvas.getContext('2d');
    let w, h, t = 0;

    function resize() {{
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }}

    function render() {{
        ctx.clearRect(0, 0, w, h);
        
        // Background Grid
        ctx.strokeStyle = '#111';
        ctx.lineWidth = 1;
        for(let i=0; i<w; i+=w/20) {{ ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, h); ctx.stroke(); }}
        for(let j=0; j<h; j+=h/10) {{ ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(w, j); ctx.stroke(); }}

        // Trace Setup
        ctx.shadowBlur = 15;
        ctx.shadowColor = '#00FFFF';
        ctx.strokeStyle = '#00FFFF';
        ctx.lineWidth = 3;

        ctx.beginPath();
        for(let x = 0; x < w; x++) {{
            let angle = x * 0.01 * {freq} + t;
            let y_val = 0;

            if("{wave_type}" === "SINE") {{
                y_val = Math.sin(angle);
            }} else if("{wave_type}" === "SQUARE") {{
                y_val = Math.sign(Math.sin(angle));
            }} else if("{wave_type}" === "SAWTOOTH") {{
                y_val = 2 * (angle / (2 * Math.PI) - Math.floor(0.5 + angle / (2 * Math.PI)));
            }}

            let y = h/2 + y_val * ({amp} * 40);
            if(x === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }}
        ctx.stroke();

        t -= 0.05;
        requestAnimationFrame(render);
    }}

    window.addEventListener('resize', resize);
    resize();
    render();
</script>
"""

components.html(canvas_code, height=500)
st.markdown("<p style='text-align: right; color: #444; font-family: monospace;'>VisualX</p>", unsafe_allow_html=True)


import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="VisualX Lab | Lissajous", layout="wide")

# 2. Aggressive CSS to REMOVE HEADER & DOTS (Same as Waveform)
st.markdown("""
    <style>
    /* Hiding the menu & header completely */
    [data-testid="stHeader"] { display: none !important; }
    header { display: none !important; }
    footer { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }

    /* Global Styling */
    .stApp, body, html {
        background-color: #050505 !important;
        color: #ffffff;
    }
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0rem !important;
    }

    /* Title Styling */
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

    /* Labels */
    .stSlider label { 
        color: #cccccc !important; 
        font-family: sans-serif;
        text-transform: uppercase;
        font-size: 0.8rem !important;
    }

    /* Control Panel */
    .control-panel {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        margin: 0px 20px;
    }

    /* Share Button */
    .stButton>button {
        width: 100%;
        background-color: transparent;
        color: #00FFFF;
        border: 1px solid #00FFFF;
        margin-top: 28px; 
    }
    
    /* Fixed Footer Watermark */
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
    
    <div class="lab-title">LISSAJOUS KINEMATICS</div>
    <div class="fixed-footer">VISUALX</div>
    """, unsafe_allow_html=True)

# 3. Controls Section (A and B Frequencies)
with st.container():
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 1])
    
    with c1:
        freq_x = st.slider("FREQUENCY X (a)", 1, 10, 3)
    with c2:
        freq_y = st.slider("FREQUENCY Y (b)", 1, 10, 2)
    with c3:
        if st.button("SHARE LAB"):
            st.toast("LINK COPIED")
            components.html("<script>window.parent.navigator.clipboard.writeText(window.parent.location.href);</script>", height=0, width=0)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Lissajous Canvas Engine
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
        
        // Background Grid
        ctx.strokeStyle = '#111'; ctx.lineWidth = 1;
        for(let i=0; i<w; i+=w/20) {{ ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, h); ctx.stroke(); }}
        for(let j=0; j<h; j+=h/10) {{ ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(w, j); ctx.stroke(); }}
        
        // Lissajous Curve (Cyan Glow)
        ctx.strokeStyle = '#00FFFF'; ctx.lineWidth = 3; ctx.shadowBlur = 15; ctx.shadowColor = '#00FFFF';
        ctx.beginPath();
        
        const a = {freq_x};
        const b = {freq_y};
        const scale = Math.min(w, h) * 0.4; // Responsive scaling
        const cx = w / 2;
        const cy = h / 2;
        
        // Draw the full curve for the current phase (t)
        for(let theta = 0; theta <= Math.PI * 2; theta += 0.01) {{
            let x = cx + Math.sin(a * theta + t) * scale;
            let y = cy + Math.sin(b * theta) * scale;
            if(theta === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }}
        ctx.stroke(); 
        
        // Tracer Point (Magenta)
        let tx = cx + Math.sin(t * a + t) * scale;
        let ty = cy + Math.sin(t * b) * scale;
        ctx.beginPath();
        ctx.arc(tx, ty, 6, 0, 2 * Math.PI);
        ctx.fillStyle = '#FF007F';
        ctx.shadowColor = '#FF007F';
        ctx.fill();

        t -= 0.03; // Controls the speed of the 3D rotation illusion
        requestAnimationFrame(loop);
    }}
    
    window.addEventListener('resize', resize);
    resize();
    loop();
</script>
"""

components.html(canvas_html, height=600)

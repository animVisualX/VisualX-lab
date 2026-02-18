import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="VisualX Lab | Lissajous", layout="wide")

# 2. Aggressive CSS to REMOVE HEADER & DOTS
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none !important; }
    header { display: none !important; }
    footer { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }

    .stApp, body, html {
        background-color: #050505 !important;
        color: #ffffff;
    }
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: 0rem !important;
    }

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

    .stSlider label { 
        color: #cccccc !important; 
        font-family: sans-serif;
        text-transform: uppercase;
        font-size: 0.8rem !important;
    }

    .control-panel {
        background: rgba(255, 255, 255, 0.01);
        border: 1px solid #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        margin: 0px 20px;
    }
    
    /* BRANDING: Fixed Footer Watermark */
    .fixed-footer {
        position: fixed;
        bottom: 12px;
        right: 25px;
        color: #666666; 
        font-family: monospace;
        font-size: 0.9rem;
        pointer-events: none;
        z-index: 9999;
        letter-spacing: 1px;
    }
    </style>
    
    <div class="lab-title">LISSAJOUS KINEMATICS</div>
    <div class="fixed-footer">@anim.VisualX</div>
    """, unsafe_allow_html=True)

# 3. Controls Section (Only Sliders, No Button)
with st.container():
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    
    # Sirf 2 columns banaye hain barabar size ke
    c1, c2 = st.columns(2)
    
    with c1:
        freq_x = st.slider("FREQUENCY X (a)", 1, 10, 3)
    with c2:
        freq_y = st.slider("FREQUENCY Y (b)", 1, 10, 2)
        
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Perfectly Closed Canvas Engine (Slow & Cinematic)
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
        
        // Lissajous Curve
        ctx.strokeStyle = '#00FFFF'; ctx.lineWidth = 3; ctx.shadowBlur = 15; ctx.shadowColor = '#00FFFF';
        ctx.beginPath();
        
        const a = {freq_x};
        const b = {freq_y};
        const scale = Math.min(w, h) * 0.4;
        const cx = w / 2;
        const cy = h / 2;
        
        // Loop stopping exactly before mathematically exceeding 2*PI
        for(let theta = 0; theta <= Math.PI * 2; theta += 0.01) {{
            let x = cx + Math.sin(a * theta + t) * scale;
            let y = cy + Math.sin(b * theta) * scale;
            if(theta === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }}
        
        // Force the exact final point to bridge the tiny gap
        let exactEndX = cx + Math.sin(a * Math.PI * 2 + t) * scale;
        let exactEndY = cy + Math.sin(b * Math.PI * 2) * scale;
        ctx.lineTo(exactEndX, exactEndY);
        
        ctx.closePath(); 
        ctx.stroke(); 
        
        // Tracer Point (Magenta)
        let tx = cx + Math.sin(t * a + t) * scale;
        let ty = cy + Math.sin(t * b) * scale;
        ctx.beginPath();
        ctx.arc(tx, ty, 6, 0, 2 * Math.PI);
        ctx.fillStyle = '#FF007F';
        ctx.shadowColor = '#FF007F';
        ctx.fill();

        // Cinematic Slow Speed
        t -= 0.006; 
        requestAnimationFrame(loop);
    }}
    
    window.addEventListener('resize', resize);
    resize();
    loop();
</script>
"""

components.html(canvas_html, height=600)

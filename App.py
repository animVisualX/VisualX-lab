import streamlit as st
import streamlit.components.v1 as components

# 1. Dashboard Configuration (16:9 Landscape)
st.set_page_config(page_title="VisualX Lab | Wave Analysis", layout="wide")

# 2. Premium Professional CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #050505; /* Deep Black for VisualX theme */
        color: #ffffff;
    }
    
    /* UI Cleanup */
    [data-testid="stSidebar"], header, footer {display: none;}

    /* Professional Title Styling */
    .lab-title {
        text-align: left;
        font-family: 'Courier New', monospace;
        color: #00FFFF;
        font-size: 1.2rem;
        padding: 10px 20px;
        border-left: 4px solid #00FFFF;
        margin: 20px 0;
    }

    /* Main Interface Control Deck */
    .control-panel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid #222;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .stSlider label { color: #888 !important; font-family: monospace; }
    </style>
    <div class="lab-title">VISUALX_LAB // SINE_WAVE_OSCILLATOR_v2.0</div>
    """, unsafe_allow_html=True)

# 3. Scientific Controls (On-Page)
with st.container():
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        amp = st.slider("AMPLITUDE (A)", 0.1, 5.0, 2.5, step=0.1)
    with c2:
        freq = st.slider("FREQUENCY (f)", 0.5, 10.0, 3.0, step=0.1)
    with c3:
        neon = st.color_picker("TRACE_COLOR", "#00FFFF")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Professional Visualization Engine (Canvas Based)
# Physics: y = A * sin(2 * PI * f * x + t)
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
        
        // Grid Lines (Scientific Feel)
        ctx.strokeStyle = '#111';
        ctx.lineWidth = 1;
        for(let i=0; i<w; i+=w/20) {{
            ctx.beginPath(); ctx.moveTo(i, 0); ctx.lineTo(i, h); ctx.stroke();
        }}
        for(let j=0; j<h; j+=h/10) {{
            ctx.beginPath(); ctx.moveTo(0, j); ctx.lineTo(w, j); ctx.stroke();
        }}

        // The Sine Wave
        ctx.shadowBlur = 15;
        ctx.shadowColor = '{neon}';
        ctx.strokeStyle = '{neon}';
        ctx.lineWidth = 3;

        ctx.beginPath();
        for(let x = 0; x < w; x++) {{
            // Real Physics Equation
            let y = h/2 + Math.sin(x * 0.01 * {freq} + t) * ({amp} * 40);
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

st.markdown("<p style='text-align: right; color: #444; font-family: monospace;'>ASPECT_RATIO: 16:9 // RENDER_STABLE</p>", unsafe_allow_html=True)

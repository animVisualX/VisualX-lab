import streamlit as st
import streamlit.components.v1 as components

# VisualX Global Configuration
st.set_page_config(page_title="VisualX | Double Pendulum Chaos", layout="wide")

# CSS Injection for VisualX Standard UI
st.markdown("""
    <style>
    header, footer, .stDeployButton, [data-testid="stToolbar"], [data-testid="stSidebar"] {
        display: none !important;
    }
    
    body, [data-testid="stAppViewContainer"] {
        background-color: #050505 !important;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    .title-container {
        border-left: 3px solid #00FFFF;
        padding-left: 20px;
        margin: 20px 0 40px 0;
    }
    
    .main-title {
        font-family: 'Courier New', monospace;
        font-size: 2.2rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #ffffff;
    }

    .stSlider label {
        color: #cccccc !important;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        font-size: 0.8rem;
    }

    .watermark {
        position: fixed;
        bottom: 20px;
        right: 20px;
        font-family: 'Courier New', monospace;
        color: #666666;
        font-size: 0.9rem;
        z-index: 9999;
        pointer-events: none;
    }
    </style>
    
    <div class="watermark">@anim.VisualX</div>
    <div class="title-container">
        <h1 class="main-title">Double Pendulum Chaos Theory</h1>
    </div>
""", unsafe_allow_html=True)

# Parameter Controls
col1, col2, col3 = st.columns(3)
with col1:
    m1 = st.slider("Mass 1", 5.0, 50.0, 20.0, 1.0)
    m2 = st.slider("Mass 2", 5.0, 50.0, 20.0, 1.0)
with col2:
    l1 = st.slider("Length 1", 50.0, 200.0, 150.0, 1.0)
    l2 = st.slider("Length 2", 50.0, 200.0, 150.0, 1.0)
with col3:
    g = st.slider("Gravity", 0.1, 2.0, 0.98, 0.01)
    trace_len = st.slider("Trace Length", 100, 2000, 1000, 10)

# Animation Engine (HTML5 Canvas + JS)
canvas_html = f"""
<div id="canvas-container" style="width: 100%; height: 80vh; overflow: hidden; position: relative; background: #050505;">
    <canvas id="pendulumCanvas"></canvas>
</div>

<script>
const canvas = document.getElementById('pendulumCanvas');
const ctx = canvas.getContext('2d');
let width, height;

let r1 = {l1}, r2 = {l2}, m1 = {m1}, m2 = {m2}, g = {g};
let a1 = Math.PI / 2, a2 = Math.PI / 2;
let a1_v = 0, a2_v = 0;

let path = [];
const maxPath = {trace_len};

function resize() {{
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}}

window.addEventListener('resize', resize);
resize();

function animate() {{
    // Physics - Run 2 steps per frame for stability
    for(let i=0; i<2; i++) {{
        let num1 = -g * (2 * m1 + m2) * Math.sin(a1);
        let num2 = -m2 * g * Math.sin(a1 - 2 * a2);
        let num3 = -2 * Math.sin(a1 - a2) * m2;
        let num4 = a2_v * a2_v * r2 + a1_v * a1_v * r1 * Math.cos(a1 - a2);
        let den = r1 * (2 * m1 + m2 - m2 * Math.cos(2 * a1 - 2 * a2));
        let a1_a = (num1 + num2 + num3 * num4) / den;

        num1 = 2 * Math.sin(a1 - a2);
        num2 = (a1_v * a1_v * r1 * (m1 + m2));
        num3 = g * (m1 + m2) * Math.cos(a1);
        num4 = a2_v * a2_v * r2 * m2 * Math.cos(a1 - a2);
        den = r2 * (2 * m1 + m2 - m2 * Math.cos(2 * a1 - 2 * a2));
        let a2_a = (num1 * (num2 + num3 + num4)) / den;

        a1_v += a1_a;
        a2_v += a2_a;
        a1 += a1_v;
        a2 += a2_v;
        
        // Dampening for cinematic feel
        a1_v *= 0.9999;
        a2_v *= 0.9999;
    }}

    let x1 = r1 * Math.sin(a1);
    let y1 = r1 * Math.cos(a1);
    let x2 = x1 + r2 * Math.sin(a2);
    let y2 = y1 + r2 * Math.cos(a2);

    path.push({{x: x2, y: y2}});
    if (path.length > maxPath) path.shift();

    // Drawing
    ctx.fillStyle = '#050505';
    ctx.fillRect(0, 0, width, height);

    ctx.translate(width/2, height/3);

    // Draw Tracer Path
    ctx.beginPath();
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = '#00FFFF';
    ctx.shadowBlur = 10;
    ctx.shadowColor = '#00FFFF';
    for(let i=1; i<path.length; i++) {{
        ctx.moveTo(path[i-1].x, path[i-1].y);
        ctx.lineTo(path[i].x, path[i].y);
    }}
    ctx.stroke();

    // Draw Pendulum Arms
    ctx.shadowBlur = 0;
    ctx.strokeStyle = '#ffffff33';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    // Draw Bobs
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#FF007F';
    ctx.fillStyle = '#FF007F';
    
    ctx.beginPath();
    ctx.arc(x1, y1, 6, 0, Math.PI*2);
    ctx.fill();
    
    ctx.beginPath();
    ctx.arc(x2, y2, 8, 0, Math.PI*2);
    ctx.fill();

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    requestAnimationFrame(animate);
}}

animate();
</script>
<style>
body {{ margin: 0; overflow: hidden; }}
</style>
"""

components.html(canvas_html, height=750)

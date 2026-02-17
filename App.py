import streamlit as st
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="VisualX: Anti-Gravity", layout="wide")

# 2. The Premium UI Styling (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Floating Control Panel */
    .css-1d391kg { 
        background: rgba(20, 20, 20, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid #222;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Modifiers
st.sidebar.title("PHASE CONTROLS")
glow_color = st.sidebar.color_picker("Energy Color", "#00FFFF")
wave_speed = st.sidebar.slider("Flow Speed", 0.01, 0.1, 0.03)
wave_amp = st.sidebar.slider("Gravity Pull", 10, 100, 50)

# 4. The "Anti-Gravity" Engine (HTML5 Canvas + JS)
# Isme hum Matplotlib use nahi kar rahe, ye seedha browser par render hoga.
canvas_html = f"""
<canvas id="canvas" style="width:100%; height:80vh;"></canvas>
<script>
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    
    let w, h, particles = [];
    let tick = 0;

    function init() {{
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }}

    function draw() {{
        ctx.clearRect(0, 0, w, h);
        
        // Asli Neon Glow Logic
        ctx.shadowBlur = 25;
        ctx.shadowColor = '{glow_color}';
        ctx.strokeStyle = '{glow_color}';
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        ctx.beginPath();
        for(let i = 0; i < w; i++) {{
            // Multi-Layered Sine Wave for "Anti-Gravity" feel
            let y = h/2 + Math.sin(i * 0.01 + tick) * {wave_amp} 
                        + Math.cos(i * 0.005 - tick * 0.5) * ({wave_amp}/2);
            if(i === 0) ctx.moveTo(i, y);
            else ctx.lineTo(i, y);
        }}
        ctx.stroke();

        // Adding Subtle Floating Particles (Anti-Gravity)
        ctx.shadowBlur = 0;
        ctx.fillStyle = '{glow_color}33'; // Faint particles
        for(let j = 0; j < 5; j++) {{
             ctx.beginPath();
             ctx.arc(Math.random()*w, Math.random()*h, 1, 0, Math.PI*2);
             ctx.fill();
        }}

        tick += {wave_speed};
        requestAnimationFrame(draw);
    }}

    window.addEventListener('resize', init);
    init();
    draw();
</script>
"""

# Render the dynamic engine
components.html(canvas_html, height=600)

st.markdown("<h1 style='text-align: center; color: white; font-family: monospace; letter-spacing: 10px;'>VISUALX</h1>", unsafe_allow_html=True)

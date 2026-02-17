import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# VisualX Setup
st.set_page_config(page_title="VisualX Kinetic Lab", layout="centered")

# Full Screen Dynamic Background CSS
st.markdown("""
    <style>
    /* Targeting the entire app container */
    .stApp {
        background: linear-gradient(-45deg, #0d0d0d, #162121, #1a0d1a, #0d0d0d);
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        color: #ffffff;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Making the main container clean */
    .main {
        background: transparent;
    }

    h1 { 
        color: #00FFFF; 
        text-align: center; 
        font-family: 'Courier New', monospace;
        letter-spacing: 4px;
        text-shadow: 0 0 15px #00FFFF;
        margin-bottom: 50px;
    }

    /* Styling Sidebar for dark aesthetic */
    section[data-testid="stSidebar"] {
        background-color: rgba(13, 13, 13, 0.8);
        border-right: 1px solid #00FFFF;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("VISUALX: KINETIC WAVE")

# Sidebar Controls
st.sidebar.header("Modifiers")
speed = st.sidebar.slider("Flow Speed", 0.0, 1.0, 0.2, step=0.05)
amp = st.sidebar.slider("Amplitude", 0.1, 5.0, 2.0, step=0.1)
freq = st.sidebar.slider("Frequency", 0.5, 5.0, 1.0, step=0.1)
neon_color = st.sidebar.color_picker("Glow Color", "#00FFFF")

# Placeholder for the Plot
plot_spot = st.empty()

# Persistent state for time
if 't' not in st.session_state:
    st.session_state.t = 0

# Animation Loop
while True:
    x = np.linspace(0, 10, 500)
    y = amp * np.sin(freq * x - st.session_state.t)
    
    # Figure setup with alpha for transparency
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_alpha(0) # Makes the figure background transparent
    ax.set_facecolor((0, 0, 0, 0)) # Makes the axes background transparent
    
    # Cinematic Glow Effect
    ax.plot(x, y, color=neon_color, linewidth=6, alpha=0.2) 
    ax.plot(x, y, color=neon_color, linewidth=2)           
    
    # Fixing the camera view
    ax.set_ylim(-6, 6)
    ax.axis('off')
    
    # Display the plot
    plot_spot.pyplot(fig)
    plt.close(fig)
    
    # Physics Update
    st.session_state.t += speed
    time.sleep(0.01)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(page_title="VisualX Lab", layout="centered")

# 2. App Title and Description
st.title("VisualX: Wave Master")
st.write("Interactive Sine Wave Simulator. Adjust the sliders to visualize mathematical concepts in real-time.")

# 3. Sidebar Controls
st.sidebar.header("Control Panel")
freq = st.sidebar.slider("Frequency (Hz)", min_value=1.0, max_value=10.0, value=3.0, step=0.1)
amp = st.sidebar.slider("Amplitude (Units)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
color = st.sidebar.color_picker("Graph Color", "#00FFFF") # Default is Cyan

# 4. Mathematical Logic
x = np.linspace(0, 10, 500)
y = amp * np.sin(freq * x)

# 5. Visualization
fig, ax = plt.subplots(figsize=(8, 4))

# Dark Mode Styling
fig.patch.set_facecolor('#0d0d0d')
ax.set_facecolor('#0d0d0d')
ax.set_ylim(-5,5)
# Plotting
ax.plot(x, y, color=color, linewidth=3)

# Hiding axes for cleaner look
ax.axis('off')

# Displaying the Graph
st.pyplot(fig)

# 6. Engagement / Call to Action
st.markdown("---")
st.info("💡 **Challenge:** Can you make the wave completely flat? Take a screenshot and tag @VisualX!")

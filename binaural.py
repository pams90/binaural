import streamlit as st
import numpy as np
from io import BytesIO
from scipy.io.wavfile import write

# Configure Streamlit page
st.set_page_config(page_title="Binaural Beat Generator", page_icon="🎧")

# Brainwave mapping with purposes
PURPOSE_MAPPING = {
    "Deep Sleep & Healing": {
        "type": "delta",
        "frequency": "0.5-4 Hz",
        "benefits": "Promotes deep sleep, physical recovery, and immune function"
    },
    "Meditation & Creativity": {
        "type": "theta",
        "frequency": "4-8 Hz",
        "benefits": "Enhances meditation, intuition, and creative thinking"
    },
    "Relaxation & Stress Relief": {
        "type": "alpha",
        "frequency": "8-14 Hz",
        "benefits": "Reduces anxiety, induces calm focus, and mindfulness"
    },
    "Focus & Productivity": {
        "type": "beta",
        "frequency": "14-30 Hz",
        "benefits": "Improves concentration, alertness, and logical thinking"
    },
    "Peak Performance": {
        "type": "gamma",
        "frequency": "30-100 Hz",
        "benefits": "Boosts memory, cognitive processing, and problem-solving"
    }
}

BRAINWAVE_FREQUENCIES = {
    "delta": 2.0,
    "theta": 6.0,
    "alpha": 10.0,
    "beta": 18.0,
    "gamma": 40.0
}

def generate_binaural_beat(purpose, duration_sec, base_freq=220.0):
    beat_type = PURPOSE_MAPPING[purpose]["type"]
    beat_freq = BRAINWAVE_FREQUENCIES[beat_type]
    sample_rate = 44100
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    
    # Generate tones
    left = np.sin(2 * np.pi * base_freq * t)
    right = np.sin(2 * np.pi * (base_freq + beat_freq) * t)
    stereo_audio = np.column_stack((left, right))
    
    # Normalize and convert to 16-bit
    stereo_audio = (stereo_audio * 32767).astype(np.int16)
    
    # Save to WAV
    buffer = BytesIO()
    write(buffer, sample_rate, stereo_audio)
    return buffer.getvalue()

# Streamlit UI
st.title("🎧 Purpose-Based Binaural Beat Generator")
st.markdown("""
Select your desired mental state or purpose below to generate customized binaural beats!
""")

# Purpose selection
selected_purpose = st.selectbox(
    "Choose Your Purpose",
    options=list(PURPOSE_MAPPING.keys()),
    index=2  # Default to Relaxation
)

# Display purpose details
purpose_details = PURPOSE_MAPPING[selected_purpose]
st.markdown(f"""
**{selected_purpose}**  
- **Frequency Range**: {purpose_details['frequency']}  
- **Key Benefits**: {purpose_details['benefits']}
""")

# Duration input
duration = st.slider("Session Duration (minutes)", 1, 60, 15)

if st.button("Generate Binaural Beat"):
    with st.spinner(f"Creating {selected_purpose} Beat..."):
        audio_bytes = generate_binaural_beat(selected_purpose, duration * 60)
        st.audio(audio_bytes, format='audio/wav')
        
        # Download button
        st.download_button(
            label="Download Audio File",
            data=audio_bytes,
            file_name=f"{selected_purpose.replace(' ', '_')}_beat.wav",
            mime="audio/wav"
        )

# Instructions
st.markdown("---")
st.markdown("""
**Usage Tips:**
1. Use headphones for best results
2. Find a quiet environment
3. Start with 10-15 minute sessions
4. Combine with related activities (e.g., meditation for theta waves)
""")

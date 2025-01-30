import streamlit as st
import numpy as np
from io import BytesIO
import soundfile as sf

# Configure Streamlit page
st.set_page_config(page_title="Binaural Beat Generator", page_icon="🎧")

# Brainwave frequency mapping
BRAINWAVE_FREQUENCIES = {
    "delta": 2.0,
    "theta": 6.0,
    "alpha": 10.0,
    "beta": 18.0,
    "gamma": 40.0
}

def generate_binaural_beat(beat_type, duration_sec, base_freq=220.0):
    beat_freq = BRAINWAVE_FREQUENCIES.get(beat_type.lower(), 10.0)
    sample_rate = 44100
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    
    # Generate tones
    left = np.sin(2 * np.pi * base_freq * t)
    right = np.sin(2 * np.pi * (base_freq + beat_freq) * t)
    stereo_audio = np.column_stack((left, right))
    
    # Normalize and convert to WAV bytes
    buffer = BytesIO()
    sf.write(buffer, stereo_audio, samplerate=sample_rate, format='WAV')
    return buffer.getvalue()

# Streamlit UI
st.title("🎧 Binaural Beat Generator")
st.markdown("Generate binaural beats for focus, sleep, or meditation!")

# User inputs
beat_type = st.selectbox(
    "Select Beat Type",
    options=list(BRAINWAVE_FREQUENCIES.keys()),
    index=2  # Default to Alpha
)
duration = st.slider("Duration (minutes)", 1, 60, 10)

if st.button("Generate Beat"):
    with st.spinner("Generating..."):
        # Create audio and display
        audio_bytes = generate_binaural_beat(beat_type, duration * 60)
        st.audio(audio_bytes, format='audio/wav')
        
        # Add download button
        st.download_button(
            label="Download WAV File",
            data=audio_bytes,
            file_name=f"{beat_type}_binaural.wav",
            mime="audio/wav"
        )

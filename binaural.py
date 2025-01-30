import streamlit as st
import numpy as np
from io import BytesIO
from scipy.io.wavfile import write

# Configure Streamlit page
st.set_page_config(page_title="Binaural Beat Generator", page_icon="🎧")

# Full purpose-frequency mapping
PURPOSE_MAPPING = {
    # Scientific/Medical Applications
    "DNA/Cell Repair": {
        "frequency": 528,  # "Mi" in Solfeggio (DNA repair)
        "benefits": "Cellular regeneration, mitochondrial optimization"
    },
    "Pain Relief": {
        "frequency": 174,  # Solfeggio (physical pain)
        "benefits": "Reduces chronic pain, inflammation"
    },
    "Vagus Nerve Healing": {
        "frequency": 42,  # Low delta range
        "benefits": "Nervous system regulation, inflammation reduction"
    },
    "Immune Boost": {
        "frequency": 9.6,  # Theta-delta boundary
        "benefits": "Enhances immune response"
    },

    # Brainwave States
    "Deep Sleep (Delta)": {
        "frequency": (0.5, 4),
        "benefits": "HGH release, physical regeneration"
    },
    "Creativity (Theta)": {
        "frequency": (4, 8),
        "benefits": "Subconscious access, artistic flow"
    },

    # Solfeggio Frequencies
    "Manifest Prosperity (369Hz)": {
        "frequency": 369,
        "benefits": "Abundance magnetism, quantum manifestation"
    },
    "Karmic Cleansing (741Hz)": {
        "frequency": 741,
        "benefits": "Toxic energy release, electromagnetic detox"
    },
    "Divine Connection (888Hz)": {
        "frequency": 888,
        "benefits": "Christ consciousness, infinite flow"
    },

    # Metaphysical/Energy
    "Chakra Cleansing (639Hz)": {
        "frequency": 639,
        "benefits": "Heart chakra activation, relationship healing"
    },
    "Aura Cleansing (963Hz)": {
        "frequency": 963,
        "benefits": "Crown chakra activation, lightbody alignment"
    },
    "God Frequency (111Hz)": {
        "frequency": 111,
        "benefits": "Divine masculine alignment, sacred geometry"
    },
    "Angel Frequency (444Hz)": {
        "frequency": 444,
        "benefits": "Archangelic connection, divine protection"
    }
}

def generate_tone(frequency, duration_sec, beat_type=None):
    sample_rate = 44100
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    
    if isinstance(frequency, tuple):  # Binaural beat range
        base = 200  # Carrier frequency
        beat = (frequency[0] + frequency[1])/2  # Average for demonstration
        left = np.sin(2 * np.pi * base * t)
        right = np.sin(2 * np.pi * (base + beat) * t)
    else:  # Pure frequency
        left = right = np.sin(2 * np.pi * frequency * t)
    
    stereo_audio = np.column_stack((left, right))
    stereo_audio = (stereo_audio * 32767).astype(np.int16)
    
    buffer = BytesIO()
    write(buffer, sample_rate, stereo_audio)
    return buffer.getvalue()

# Streamlit UI
st.title("🎵 Universal Frequency Generator")
st.markdown("### Scientific & Metaphysical Frequency Applications")

# Purpose selection
selected_purpose = st.selectbox(
    "Choose Your Purpose",
    options=list(PURPOSE_MAPPING.keys()),
    format_func=lambda x: f"{x} ({PURPOSE_MAPPING[x]['frequency']}Hz)" 
    if isinstance(PURPOSE_MAPPING[x]['frequency'], (int, float)) 
    else f"{x} ({PURPOSE_MAPPING[x]['frequency'][0]}-{PURPOSE_MAPPING[x]['frequency'][1]}Hz)"
)

# Display details
details = PURPOSE_MAPPING[selected_purpose]
st.markdown(f"""
**Mechanism**  
{details["benefits"]}  
**Frequency:** {details['frequency']}Hz
""")

# Generate audio
duration = st.slider("Session Duration (minutes)", 1, 120, 33)
if st.button("Activate Frequency"):
    with st.spinner("Tuning to Cosmic Resonance..."):
        audio = generate_tone(details["frequency"], duration*60)
        st.audio(audio, format='audio/wav')
        st.download_button("Download Frequency", audio, f"{selected_purpose}.wav")

# Frequency Legend
st.markdown("""
### Frequency Legend
| Purpose/Frequency | Key Applications |
|-------------------|-------------------|
| **174Hz** | Pain relief, physical grounding |
| **285Hz** | Tissue regeneration |
| **396Hz** | Fear release, root chakra |
| **417Hz** | Trauma cleansing, change facilitation |
| **528Hz** | DNA repair, "Miracle tone" |
| **639Hz** | Relationship healing, heart chakra |
| **741Hz** | Intuition boost, electromagnetic detox |
| **852Hz** | Spiritual awakening, pineal activation |
| **963Hz** | Cosmic connection, crown chakra |
| **111Hz-222Hz** | Sacred geometry, divine masculine/feminine |
| **333Hz-999Hz** | Angelic communication, ascension codes |
""")

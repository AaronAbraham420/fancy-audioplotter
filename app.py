import streamlit as st
import librosa
import librosa.display
import numpy as np
import plotly.graph_objects as go
import soundfile as sf
import io

st.set_page_config(page_title="🎧 Fancy-Audioplotter", layout="wide")
st.title("🎧 Fancy-Audioplotter")
st.markdown("Upload a `.wav` file and explore its waveform interactively.")

uploaded_file = st.file_uploader("Choose a .wav file", type=["wav"])

if uploaded_file is not None:
    with st.spinner("Processing audio file..."):
        # Load the audio from the uploaded file
        y, sr = sf.read(io.BytesIO(uploaded_file.read()))

        # If stereo, convert to mono
        if y.ndim > 1:
            y = y.mean(axis=1)

        duration = len(y) / sr
        time = np.linspace(0, duration, num=len(y))

        # Create the Plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time,
            y=y,
            mode="lines",
            line=dict(color="deeppink", width=1),
            name="Waveform"
        ))

        fig.update_layout(
            title="Interactive Waveform",
            xaxis_title="Time (s)",
            yaxis_title="Amplitude",
            hovermode="x unified",
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(color="white"),
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        st.success(f"Loaded audio — Duration: {duration:.2f} seconds @ {sr} Hz")
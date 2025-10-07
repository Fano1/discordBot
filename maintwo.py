from bark import generate_audio, preload_models
import soundfile as sf

# preload models once (slow, do it at start)
preload_models()

text = "*laughs* Hello, Fano~ you naughty coder."

# Generate audio with bark
audio_array = generate_audio(text)

# Save to file
sf.write("output.wav", audio_array, 24000)

print("Generated speech with laughter!")

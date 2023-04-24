from whisper_jax import FlaxWhisperPipline
import jax.numpy as jnp

# instantiate pipeline in bfloat16
pipeline = FlaxWhisperPipline("openai/whisper-large-v2")

# instantiate pipeline
#pipeline = FlaxWhisperPipline("openai/whisper-large-v2")

# JIT compile the forward call - slow, but we only do once
text = pipeline("audio.mp3")

# used cached function thereafter - super fast!!
text = pipeline("audio.mp3")

# print the text
print(text)
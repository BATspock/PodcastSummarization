# import required modules
# import subprocess
  
# # convert mp3 to wav file
# subprocess.call(['ffmpeg', '-i', 'audio/WW2 vs War in Ukraine.mp3',
#                  'converted_to_wav_file.wav'])

from pyAudioAnalysis import audioBasicIO, audioSegmentation
from pyAudioAnalysis import ShortTermFeatures
from sklearn.cluster import KMeans
import numpy as np

# Specify the path to your audio file
audio_file = "audio_wav/audio_clip.wav"

# Load the audio file
[signal, sample_rate] = audioBasicIO.read_audio_file(audio_file)

# Specify the short-term analysis parameters
st_win = 0.05  # Window size in seconds
st_step = 0.025  # Step size in seconds

# Perform voice activity detection (VAD)
segments = audioSegmentation.silence_removal(signal, sample_rate, st_win, st_step)

# Specify the desired features
feature_type = ShortTermFeatures.MFCC

# Extract features for each segment
features = []
for segment in segments:
    start_time, end_time = segment
    segment_signal = signal[int(start_time * sample_rate):int(end_time * sample_rate)]
    segment_features, _ = ShortTermFeatures.feature_extraction(segment_signal, sample_rate, feature_type)
    features.append(segment_features.T)  # Transpose the feature matrix

# Combine feature matrices into a single numpy array
all_features = np.concatenate(features)

# Specify the desired number of speakers
num_speakers = 2

# Perform clustering on the feature vectors
kmeans = KMeans(n_clusters=num_speakers)
cluster_labels = kmeans.fit_predict(all_features)

# Print the speaker segments and corresponding labels
for i, segment in enumerate(segments):
    start_time, end_time = segment
    label = cluster_labels[i]
    print(f"Segment: {i+1} - Speaker: {label} - Start: {start_time:.2f}s, End: {end_time:.2f}s")






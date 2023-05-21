# import required modules
# import subprocess
  
# # convert mp3 to wav file
# subprocess.call(['ffmpeg', '-i', 'audio/WW2 vs War in Ukraine.mp3',
#                  'converted_to_wav_file.wav'])

# import whisperx
# import gc 

# device = "cuda" 
# audio_file = "audio_wav/audio_clip.wav"
# batch_size = 16 # reduce if low on GPU mem
# compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

# # 1. Transcribe with original whisper (batched)
# model = whisperx.load_model("base.en", device, compute_type=compute_type)

# audio = whisperx.load_audio(audio_file)
# result = model.transcribe(audio, batch_size=batch_size)
# print(result["segments"]) # before alignment

# # delete model if low on GPU resources
# # import gc; gc.collect(); torch.cuda.empty_cache(); del model

# # 2. Align whisper output
# model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
# result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

# print(result["segments"]) # after alignment

# # delete model if low on GPU resources
# # import gc; gc.collect(); torch.cuda.empty_cache(); del model_a

# # 3. Assign speaker labels
# diarize_model = whisperx.DiarizationPipeline(use_auth_token="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", device=device)

# # add min/max number of speakers if known
# diarize_segments = diarize_model(audio_file)
# # diarize_model(audio_file, min_speakers=min_speakers, max_speakers=max_speakers)

# result = whisperx.assign_word_speakers(diarize_segments, result)
# print(diarize_segments)
# print(result["segments"]) # segments are now assigned speaker IDs

from pyAudioAnalysis import audioBasicIO, audioSegmentation
from pyAudioAnalysis import ShortTermFeatures
from sklearn.cluster import KMeans
import numpy as np

# Specify the path to your huge audio file
audio_file = "audio_wav/audio_clip.wav"

# Specify the segment duration and overlap
segment_duration = 30  # Duration of each segment in seconds
overlap = 10  # Overlap duration between segments in seconds

# Load the audio file
[signal, sample_rate] = audioBasicIO.read_audio_file(audio_file)

# Calculate the number of samples per segment and overlap
segment_samples = int(segment_duration * sample_rate)
overlap_samples = int(overlap * sample_rate)

# Iterate over the audio file in segments
start = 0
end = segment_samples
segments = []
while end < len(signal):
    segment = signal[start:end]
    segments.append(segment)
    start += segment_samples - overlap_samples
    end += segment_samples - overlap_samples

# Specify the desired features
feature_type = ShortTermFeatures.MFCC

# Extract features for each segment
features = []
for i, segment in enumerate(segments):
    segment_features, _ = ShortTermFeatures.feature_extraction(segment, sample_rate, feature_type)
    features.append(segment_features.T)  # Transpose the feature matrix

    # Print progress
    print(f"Processed segment {i+1}/{len(segments)}")

# Combine feature matrices into a single numpy array
all_features = np.concatenate(features)

# Specify the desired number of speakers
num_speakers = 2

# Perform clustering on the feature vectors
kmeans = KMeans(n_clusters=num_speakers)
cluster_labels = kmeans.fit_predict(all_features)

# Calculate the start and end times for each segment
total_duration = len(signal) / sample_rate
duration_per_segment = (segment_duration - overlap) * len(segments) + overlap
time_per_segment = total_duration / duration_per_segment

# Print the speaker segments and corresponding labels
for i, segment in enumerate(segments):
    start_time = i * time_per_segment
    end_time = start_time + segment_duration
    label = cluster_labels[i]
    print(f"Segment: {i+1} - Speaker: {label} - Start: {start_time:.2f}s, End: {end_time:.2f}s")

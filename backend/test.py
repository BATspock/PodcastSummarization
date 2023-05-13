# import required modules
# import subprocess
  
# # convert mp3 to wav file
# subprocess.call(['ffmpeg', '-i', 'audio/WW2 vs War in Ukraine.mp3',
#                  'converted_to_wav_file.wav'])

from pyAudioAnalysis import audioSegmentation

# Specify the path to your audio file
audio_file = "audio_wav/audio_clip.wav"

# Perform speaker diarization
result = audioSegmentation.speaker_diarization(audio_file,2)

# Print the speaker segments and corresponding labels
for segment in result:
    start_time = segment[0]
    end_time = segment[1]
    label = segment[2]
    print(f"Speaker: {label} - Start: {start_time:.2f}s, End: {end_time:.2f}s")

# import required modules
# import subprocess
  
# # convert mp3 to wav file
# subprocess.call(['ffmpeg', '-i', 'audio/WW2 vs War in Ukraine.mp3',
#                  'converted_to_wav_file.wav'])

import whisperx
import gc 

device = "cuda" 
audio_file = "audio_wav/audio_clip.wav"
batch_size = 16 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

# 1. Transcribe with original whisper (batched)
model = whisperx.load_model("base.en", device, compute_type=compute_type)

audio = whisperx.load_audio(audio_file)
result = model.transcribe(audio, batch_size=batch_size)
print(result["segments"]) # before alignment

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model

# 2. Align whisper output
model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

print(result["segments"]) # after alignment

# delete model if low on GPU resources
# import gc; gc.collect(); torch.cuda.empty_cache(); del model_a

# 3. Assign speaker labels
diarize_model = whisperx.DiarizationPipeline(use_auth_token="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", device=device)

# add min/max number of speakers if known
diarize_segments = diarize_model(audio_file)
# diarize_model(audio_file, min_speakers=min_speakers, max_speakers=max_speakers)

result = whisperx.assign_word_speakers(diarize_segments, result)
print(diarize_segments)
print(result["segments"]) # segments are now assigned speaker IDs






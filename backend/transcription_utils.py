import whisper
import os


def transcribe(audio, model="base")->any:
    # get file name
    # example: audio = "audio/audio_clip.mp3"
    if audio != "portion.mp3":
        file_name = audio.split("/")[-1].split(".")[0]
    else:
        file_name = "portion.mp3"
    # create transcription folder if it doesn't exist
    if not os.path.exists('transcriptions'):
        os.makedirs('transcriptions')
    # load the model
    model = whisper.load_model(model)
    transcription_text =  model.transcribe(audio)["text"]
    # write the transcription_text to a file in transcriptions folder
    with open("transcriptions/"+file_name.split(".")[0]+".txt", "w") as f:
        f.write(transcription_text)
    return transcription_text
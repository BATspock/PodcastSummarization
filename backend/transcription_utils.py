import whisper


def transcribe(audio, model="base"):
    model = whisper.load_model(model)
    return model.transcribe(audio)["text"]
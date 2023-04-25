from flask import Flask, render_template, request, redirect, url_for, flash
from download_utils import download_audio_youtube
from transcription_utils import transcribe
from diarization import diarization_function
import os

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return "<H1>Hello World</H1>"

@app.route('/download', methods=["GET","POST"])
def download():
    # get url from request
    #print("Request method: ", request.method)
    if request.method == "GET":
        #print(request.args.get("url"))
        url = request.args.get("url")
        
        download_audio_youtube(url)
        
        # transcribe the audio in audio folder
        file = os.listdir("audio")[0]
        transcription = transcribe("audio/"+file)

        # save transcription in a text file in transcrtiptions folder
        # check if transcription folder exists
        if not os.path.exists("transcriptions"):
            os.mkdir("transcriptions")

        # save the transcription in a text file
        # remove the extension from the file name
        file = file.split(".")[0]
        with open("transcriptions/"+file+".txt", "w") as f:
            f.write(transcription)
        
        # diarize the audio file
        diarization_function("audio/"+file+".mp3")

    return "<H1>Downloading</H1>"


if __name__ == '__main__':
    app.run(debug=True)

# create a Flask app to download audio files from url and convert to mp3, 
# then upload to S3 bucket (In Future)
# add them to a queue to be processed by a worker
# worker transcribes the audio file and saves the transcription to a database
# worker sends a notification 
# second worker reads the transcription and summarizes it
# the summary is sent to the user

import os 
import youtube_dl
from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient
import whisper

app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return "<H1>Hello World</H1>"

@app.route('/download', methods=["GET","POST"])

def download():
    # get url from request
    print("Request method: ", request.method)
    if request.method == "GET":
        # print(request.args.get("url"))
        url = request.args.get("url")
        ydl_opts = {
        "outtmpl": "file.mp3",
        "format": "bestaudio/best",
        # "postprocessors": [{
        #     "key": "FFmpegExtractAudio",
        #     "preferredcodec": "mp3",
        #     "preferredquality": "192",
        #     }],
        }
        print("Downloading audio now\n")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed!")
        # upload to S3 bucket
        # or upload to MongoDB
        # add to queue
        # for implemenation later

        print("Transcribing audio now\n")
        model = whisper.load_model("tiny.en")
        result = model.transcribe("file.mp3")
        print(result["text"])
        # save trascrtiption to a text file
        with open("transcription.txt", "w") as f:
            f.write(result["text"])
        print("Transcription completed!")
    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run(debug=True)
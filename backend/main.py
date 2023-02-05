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
from transformers import pipeline

app = Flask(__name__)
summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
model = whisper.load_model("tiny.en")

@app.route('/', methods=["GET"])
def index():
    return "<H1>Hello World</H1>"

@app.route('/download', methods=["GET","POST"])

def download():
    # get url from request
    #print("Request method: ", request.method)
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
        print("########################## Downloading audio now #####################\n")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("########################## Download completed! #####################\n")
        # upload to S3 bucket
        # or upload to MongoDB
        # add to queue
        # for implemenation later

        print("######################### Transcribing audio now #####################\n")
        
        result = model.transcribe("file.mp3", fp16=False)
        #print(result["text"])
        # save trascrtiption to a text file
        with open("transcription.txt", "w") as f:
            f.write(result["text"])
        print("######################### Transcription completed! #####################\n")

        # summarize the transcription
        print("###################### Summarizing transcription now ###################\n")
        summary = summarizer(result["text"], max_length=2000, min_length=100, do_sample=False)
        print(summary[0]["summary_text"])
        print("######################### Summarization completed! #####################\n")
        # save summary to a text file
        with open("summary.txt", "w") as f:
            f.write(summary[0]["summary_text"])

    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run(debug=True)
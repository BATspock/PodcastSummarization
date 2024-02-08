# http://127.0.0.1:5000/diarize?url=https://www.youtube.com/watch?v=cjwpxzXlpC8&ab_channel=LexClips
# http://127.0.0.1:5000/transcribe?url=https://www.youtube.com/watch?v=cjwpxzXlpC8&ab_channel=LexClips

from flask import Flask, render_template, request, jsonify
from download_utils import download_audio_youtube
from transcription_utils import transcribe
from diarization import diarization_function, tsv_to_json
import os
import timeit
from pymongo import MongoClient
import gridfs

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['transcriptions_db']  # Use or create a database for transcriptions
transcriptions_collection = db['transcriptions']  # Use or create a collection for storing transcriptions


@app.route('/', methods=["GET"])
def index():
    return "<H1>Hello World</H1>"

@app.route('/transcribe', methods=["GET","POST"])
def transcribe_audio():
    # get url from request
    #print("Request method: ", request.method)
    if request.method == "GET":
        #print(request.args.get("url"))
        url = request.args.get("url")
        start_time  = timeit.default_timer()
        download_audio_youtube(url)
        
        print("Starting transcription..........")
        # transcribe the audio in audio folder
        file_name = os.listdir("audio")[0]
        transription = transcribe("audio/"+file_name)
        
        print("Transcription completed..........")
        print("Time taken to process the audio file:", timeit.default_timer()-start_time)
    return jsonify({"transcription":transription})

@app.route('/diarize', methods=["GET","POST"])
def diarize_audio():
    # get url from request
    #print("Request method: ", request.method)
    if request.method == "GET":
        #print(request.args.get("url"))
        url = request.args.get("url")
        start_time  = timeit.default_timer()
        download_audio_youtube(url)
        
        print("Starting transcription..........")
        # transcribe the audio in audio folder
        file_name = os.listdir("audio")[0]
        _ = transcribe("audio/"+file_name)
        print("Transcription completed..........")
        print("Starting diarization..........")
        # diarize the audio file
        diarization_function("audio/"+file_name)
        print("Diarization completed..........")
        print("Time taken to process the audio file:", timeit.default_timer()-start_time)

        data = tsv_to_json("Final_tsv/"+file_name.split(".")[0]+".tsv")
        print("Time taken to process the audio file: "+str(timeit.default_timer()-start_time))
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

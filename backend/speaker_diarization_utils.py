# 1. visit hf.co/pyannote/speaker-diarization and accept user conditions
# 2. visit hf.co/pyannote/segmentation and accept user conditions
# 3. visit hf.co/settings/tokens to create an access token
# 4. instantiate pretrained speaker diarization pipeline
import torch
from pyannote.audio import Pipeline
import timeit
import os
# from pydub import AudioSegment
import sys
import pandas as pd
import subprocess


pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="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")


def convert_rttm_to_csv(file):
    """
    Inputs:
    file: str
        file path of the rttm file to be converted

    Outputs:
    df: dataframe
        Dataframe containing the extracted information from the rttm file
    """
    # read the file
    df = pd.read_csv(file, delimiter=" ", header=None)
    df = df[[3, 4, 7]]
    df.columns = ['start_time', 'duration', 'speaker_name']
    # compute the end time
    df['end_time'] = df['start_time'] + df['duration']
    # convert time to miliseconds
    df['start_time'] *= 1000
    df['end_time'] *= 1000
    # sort the df based on the start_time
    df.sort_values(by=['start_time'], inplace=True)
    # return
    return df


def convertmp3towav(src, dst):
    # sound = AudioSegment.from_mp3(src)
    # sound.export(dst, format="wav")
    subprocess.call(['ffmpeg', '-i', src, dst])


def diarize_audio(audio_file_path, min_speakers=2, max_speakers=5):
    #diarize the audio file
    print("Diarizing the audio file")
    start_time = timeit.default_timer()
    diarization = pipeline(audio_file_path)
    print("Time Taken to diarize the audio file:",timeit.default_timer()-start_time)
    return diarization
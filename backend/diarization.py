from speaker_diarization_utils import convert_rttm_to_csv, convertmp3towav, diarize_audio
from pydub import AudioSegment

from transcription_utils import transcribe


def diarization_function(audio)->any:
    """
    Inputs:
    audio: str
        Path to the audio file

    Outputs:
    None
    """
    print("Path of the file:", audio)
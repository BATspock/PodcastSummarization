# from pytube import YouTube
import os
import yt_dlp as youtube_dl

def download_audio_youtube(video_url)->None:
    # create the directory if it doesn't exist
    if not os.path.exists('audio'):
        os.makedirs('audio')

    # set options for the downloader
    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': 'audio/audio_clip.mp3',
        'noplaylist': True,
        'verbose': True
    }

    # create a downloader instance
    with youtube_dl.YoutubeDL(options) as downloader:
        try:
            downloader.extract_info(video_url)
        except youtube_dl.utils.ExtractorError as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    download_audio_youtube("https://www.youtube.com/watch?v=bNNGaqe9VzU&list=PLrAXtmErZgOeciFP3CBCIEElOJeitOr41")
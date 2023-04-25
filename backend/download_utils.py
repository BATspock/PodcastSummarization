from pytube import YouTube
import os


def download_audio_youtube(url)->None:
    yt = YouTube(url)
    audio = yt.streams.filter(only_audio=True).first()
    destination = os.path.join(os.getcwd(), "audio")
    out_file = audio.download(output_path=destination)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    print("Downloaded: ", new_file)
# Example usage: download_audio("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


if __name__ == '__main__':
    download_audio_youtube("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
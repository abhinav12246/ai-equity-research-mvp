import whisper
import yt_dlp
import os

def get_transcript_from_youtube(url):
    model = whisper.load_model("base")
    ydl_opts = {'format': 'bestaudio', 'outtmpl': 'temp_audio.%(ext)s'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    transcript = model.transcribe("temp_audio.webm")
    os.remove("temp_audio.webm")
    return transcript['text']

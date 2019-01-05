import moviepy.editor as mp
from pytube import YouTube

class CustomYouTube(object):

    def save_clip(self, url):
        yt = YouTube(url)
        path = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
        clip = mp.VideoFileClip(path)
        clip.audio.write_audiofile('youtube.mp3')

from pytube import Playlist, YouTube
from pydub import AudioSegment
import os

def download_playlist_as_mp3(playlist_url, download_path):
    # Set paths to ffmpeg and ffprobe if they are not in PATH
    AudioSegment.converter = "/usr/local/bin/ffmpeg"
    AudioSegment.ffprobe = "/usr/local/bin/ffprobe"

    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Load the playlist
    playlist = Playlist(playlist_url)
    print(f"Downloading playlist: {playlist.title}")

    for video_url in playlist.video_urls:
        try:
            # Load the YouTube video
            yt = YouTube(video_url)
            print(f"Downloading video: {yt.title}")

            # Get the highest quality audio stream available
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_file_path = audio_stream.download(output_path=download_path)

            # Convert to MP3
            base, ext = os.path.splitext(audio_file_path)
            mp3_file_path = f"{base}.mp3"
            audio = AudioSegment.from_file(audio_file_path)
            audio.export(mp3_file_path, format="mp3")

            # Remove the original audio file
            os.remove(audio_file_path)
            print(f"Converted and saved as MP3: {mp3_file_path}")

        except Exception as e:
            print(f"Failed to download or convert video: {video_url}")
            print(f"Error: {e}")

if __name__ == "__main__":
    playlist_url = input("Enter the YouTube playlist URL: ")
    download_path = input("Enter the download path: ")
    download_playlist_as_mp3(playlist_url, download_path)

from module.utils import my_function
from moviepy.editor import VideoFileClip

video_path=my_function()

def extract_audio():

    try:
        video = VideoFileClip(video_path)  # Load the video file
        audio_path = "aud.wav"  # Specify the output audio file name
        video.audio.write_audiofile(audio_path)  # Extract and save the audio
        print(f"Audio has been successfully extracted and saved as '{audio_path}'.")
        return audio_path
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")
        return None


extract_audio()
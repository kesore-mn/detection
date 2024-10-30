from module.utils import my_function
from moviepy.editor import VideoFileClip

def extract_audio():
    video_path = my_function()  # Get the video path from the utility function
    if not video_path:
        print("No video file selected.")
        return  # Exit if no video path is returned

    try:
        video = VideoFileClip(video_path)  # Load the video file
        audio_path = "extracted_audio.wav"  # Specify the output audio file name
        file=video.audio  # Extract and save the audio
        print(f"Audio has been successfully extracted and saved as '{audio_path}'.")
        return file
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")

# Call the function to extract audio
extract_audio()




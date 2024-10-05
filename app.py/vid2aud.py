import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip


root = tk.Tk()
root.withdraw() 


video_path = filedialog.askopenfilename(title="Select video file", filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")])

if video_path:
    try:
        # Load the video file
        video = VideoFileClip(video_path)

        # Extract and save the audio
        audio = video.audio.write_audiofile("audio.mp3")
        print("Audio has been successfully extracted and saved as 'audio.mp3'.")
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("No file selected.")
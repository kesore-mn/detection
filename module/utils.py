import tkinter as tk
from tkinter import filedialog

def my_function():
    root = tk.Tk()
    root.withdraw()  

# Open a file dialog and ask for video input
    video_path = filedialog.askopenfilename(title="Select video file", filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov")])
    root.destroy()
    return video_path

my_function()

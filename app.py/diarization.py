import assemblyai as aai
from module.utils import my_function
from moviepy.editor import VideoFileClip

def extract_audio():
    video_path = my_function()  # Get the video path from the utility function
    if not video_path:
        print("No video file selected.")
        return # Exit if no video path is returned

    try:
        video = VideoFileClip(video_path)  # Load the video file
        audio_path = "aud.wav"  # Specify the output audio file name
        video.audio.write_audiofile("aud.wav")  # Extract and save the audio
        print(f"Audio has been successfully extracted and saved as '{audio_path}'.")
        return audio_path
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")



aai.settings.api_key = "5fa049bf61b947c58048af6e93dd6b8e" 

audio_path=extract_audio()
n=int(input("enter the number of speakers:"))


config = aai.TranscriptionConfig(
  speaker_labels=True,
)

transcript = aai.Transcriber().transcribe(audio_path, config)

speaker_counts={}
for utterance in transcript.utterances:
  print(f"Speaker {utterance.speaker}: {utterance.text}")

for utterance in transcript.utterances:
    speaker=utterance.speaker
    if speaker in speaker_counts:
        speaker_counts[speaker] += 1
    else:
        speaker_counts[speaker] = 1
    

# Get the count of unique speakers
number_of_speakers = len(speaker_counts)

print(f"Number of unique speakers: {number_of_speakers}")
print("Occurrences of each speaker:")
for speaker, count in speaker_counts.items():
    print(f"Speaker {speaker}: {count} occurrences")
    
if number_of_speakers>n and count > 10:
    print("more than")
else:
    print("no suspect")

 # Delete the extracted audio file after processing

   

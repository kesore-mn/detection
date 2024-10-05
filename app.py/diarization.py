import assemblyai as aai


aai.settings.api_key = "5fa049bf61b947c58048af6e93dd6b8e" 

# You can use a local filepath:
# audio_file = "./example.mp3"

# Or use a publicly-accessible URL:
n=int(input("enter the number of speakers:"))
audio_file = ("sample videos/TCS Campus Interview I Campus Placements I Gauri Shrimali I Arvind Singh Pemawat.mp3")

config = aai.TranscriptionConfig(
  speaker_labels=True,
)

transcript = aai.Transcriber().transcribe(audio_file, config)

speaker_counts={}

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
    print("suspected")
else:
    print("no suspect")



   
import pvfalcon
import pvleopard
from module.utils2 import extract_audio
from difflib import SequenceMatcher
def text_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()

# Function to check if the candidate (Speaker 2) gets help from others
def check_for_help(
    speaker_labelled_transcription, 
    interviewer_speaker=1, 
    candidate_speaker=2, 
    similarity_threshold=0.7
):
    help_info = []
    no_helper_phrases = []
    helper_phrases_cache = set()  

    # Iterate through all entries in the transcription
    for i, entry in enumerate(speaker_labelled_transcription):
        if entry['speaker_tag'] == candidate_speaker:
            for j in range(i):
                prev_entry = speaker_labelled_transcription[j]
                if prev_entry['speaker_tag'] not in [candidate_speaker, interviewer_speaker]:
                    explicit_help = any(phrase in prev_entry['transcription'].lower() for phrase in [
                        "mention", "talk about", "don't forget", "please tell us", "highlight", 
                        "you should", "try to include", "make sure to", "consider mentioning", 
                        "add details about", "it would be good to", "remember to", "focus on", 
                        "elaborate on", "touch on", "say something about", "you might want to", 
                        "bring up", "it's important to mention", "discuss", "you could talk about"
                    ])
                    implicit_help = False
                    if not explicit_help:
                        similarity = text_similarity(entry['transcription'], prev_entry['transcription'])
                        implicit_help = similarity >= similarity_threshold
                    
                    single_word_help = any(word in entry['transcription'].lower() for word in prev_entry['transcription'].split())
                    if explicit_help or implicit_help or single_word_help:
                        if prev_entry['transcription'] not in helper_phrases_cache:
                            helper_phrases_cache.add(prev_entry['transcription'])
                            help_info.append({
                                'helper_speaker': prev_entry['speaker_tag'],
                                'help_type': 'explicit' if explicit_help else 'implicit' if implicit_help else 'single-word',
                                'help_given': prev_entry['transcription'],
                                'candidate_speaker': candidate_speaker,
                                'candidate_answer': entry['transcription']
                            })
            if not any(
                h['candidate_answer'] == entry['transcription'] for h in help_info
            ):
                no_helper_phrases.append(entry)

    return help_info, no_helper_phrases


# Picovoice initialization
access_key = 'acC/HjZ9MUMMAvEo+HWFwACUrMIc0d36j3BeKKpFSiNHS/HAijXx9g=='  # Replace with your key
audio_path = extract_audio()
leopard = pvleopard.create(access_key)
falcon = pvfalcon.create(access_key)
transcript, words = leopard.process_file(audio_path)
segments = falcon.process_file(audio_path)
speaker_labelled_transcription = []
word_index = 0

last_speaker_tag = None
last_speaker_start_time = None
last_speaker_end_time = None
current_transcript = []

for segment in segments:
    start_time = segment.start_sec
    end_time = segment.end_sec
    speaker_tag = segment.speaker_tag
    if last_speaker_tag != speaker_tag:
        if current_transcript:
            speaker_labelled_transcription.append({
                'speaker_tag': last_speaker_tag,
                'start_time': last_speaker_start_time,
                'end_time': last_speaker_end_time,
                'transcription': " ".join(current_transcript)
            })

        last_speaker_tag = speaker_tag
        last_speaker_start_time = start_time
        last_speaker_end_time = end_time
        current_transcript = []

    while word_index < len(words):
        word = words[word_index]

        if word.start_sec >= start_time and word.start_sec <= end_time:
            current_transcript.append(word.word)

        if word.end_sec > end_time:
            break

        word_index += 1

    last_speaker_end_time = end_time

if current_transcript:
    speaker_labelled_transcription.append({
        'speaker_tag': last_speaker_tag,
        'start_time': last_speaker_start_time,
        'end_time': last_speaker_end_time,
        'transcription': " ".join(current_transcript)
    })
print("--- Transcription with Speaker Labels ---")
for entry in speaker_labelled_transcription:
    print(
        "Speaker %d [%.2f - %.2f]: %s"
        % (entry['speaker_tag'], entry['start_time'], entry['end_time'], entry['transcription'])
    )
help_info, no_helper_phrases = check_for_help(speaker_labelled_transcription)

if help_info:
    print("\n--- Helpers Detected ---")
    for help_entry in help_info:
        print(f"Helper Speaker {help_entry['helper_speaker']} helps Candidate Speaker {help_entry['candidate_speaker']}")
        print(f"Help Type: {help_entry['help_type']}")
        print(f"Help Given: {help_entry['help_given']}")
        print(f"Candidate Answer: {help_entry['candidate_answer']}")
        print()
else:
    print("\nNo helpers detected.")

if no_helper_phrases:
    print("\nDirect answers from Candidate Speaker 2 (no helper detected):")
    for entry in no_helper_phrases:
        print(f"Speaker {entry['speaker_tag']} [{entry['start_time']:.2f} - {entry['end_time']:.2f}]: {entry['transcription']}")

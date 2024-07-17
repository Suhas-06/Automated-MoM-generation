transcript_file = 'C:\\Users\\SuhasGowda\\Desktop\\Code\\meeting_summary\\temporary\\transcripts.txt'
speaker_label_file = "C:\\Users\\SuhasGowda\\Desktop\\Code\\meeting_summary\\temporary\\speaker.txt"
output_sentence_file = "C:\\Users\\SuhasGowda\\Desktop\\Code\\meeting_summary\\temporary\\preprocessed.txt"

transcript_lines = []
speaker_label_lines = []

# Read transcript file
with open(transcript_file, 'r') as file:
    transcript_lines = file.readlines()

# Read speaker label file
with open(speaker_label_file, 'r') as file:
    speaker_label_lines = file.readlines()

# Initialize variables
current_speaker_label = None
current_speaker_start = None
current_speaker_end = None

# Initialize variables for sentence processing
current_speaker = None
current_sentence = []
sentence_start_time = None
sentence_end_time = None

# Function to convert seconds to MM:SS format
def convert_seconds_to_mmss(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes}:{seconds:02d}"  # Format seconds with leading zero if less than 10

# Open output sentence file
with open(output_sentence_file, 'w') as sentence_file:
    # Iterate through transcript lines
    for line in transcript_lines:
        if line.strip():  # Check if line is not empty
            # Extract word, start time, and end time from transcript line
            if line.startswith("Word:"):
                word = line.split("Word:")[1].strip().split(",")[0].strip()
                start_time = float(line.split("Start:")[1].strip().split(",")[0].strip())
                end_time = float(line.split("End:")[1].strip().split(",")[0].strip())

                # Find corresponding speaker label
                for label_line in speaker_label_lines:
                    if label_line.strip():  # Check if line is not empty
                        speaker = int(label_line.split("Speaker:")[1].strip().split(",")[0].strip())
                        label_start = float(label_line.split("Start:")[1].strip().split(",")[0].strip())
                        label_end = float(label_line.split("End:")[1].strip().split(",")[0].strip())
                        
                        # Check if the word's start time falls within the speaker's segment
                        if label_start <= start_time <= label_end:
                            current_speaker_label = speaker
                            current_speaker_start = label_start
                            current_speaker_end = label_end
                            break

                # Process sentence grouping
                if current_speaker_label is not None:
                    if current_speaker is None:
                        # Initialize for the first speaker
                        current_speaker = current_speaker_label
                        current_sentence.append(word)
                        sentence_start_time = start_time
                        sentence_end_time = end_time
                    elif current_speaker == current_speaker_label:
                        # Continue adding to the current sentence
                        current_sentence.append(word)
                        sentence_end_time = end_time
                    else:
                        # Write the current sentence to file
                        if current_sentence:
                            sentence_text = ' '.join(current_sentence)
                            formatted_start_time = convert_seconds_to_mmss(sentence_start_time)
                            formatted_end_time = convert_seconds_to_mmss(sentence_end_time)
                            sentence_file.write(f"Speaker {current_speaker}: {sentence_text}, Start: {formatted_start_time}, End: {formatted_end_time}\n")
                        
                        # Reset for the new speaker
                        current_speaker = current_speaker_label
                        current_sentence = [word]
                        sentence_start_time = start_time
                        sentence_end_time = end_time

    # Write the last sentence to file
    if current_sentence:
        sentence_text = ' '.join(current_sentence)
        formatted_start_time = convert_seconds_to_mmss(sentence_start_time)
        formatted_end_time = convert_seconds_to_mmss(sentence_end_time)
        sentence_file.write(f"Speaker {current_speaker}: {sentence_text}, Start: {formatted_start_time}, End: {formatted_end_time}\n")

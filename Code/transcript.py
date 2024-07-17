from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

api_key = 'YOUR API KEY'
service_url = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/YOUR INSTANCE ID"

authenticator = IAMAuthenticator(api_key)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(service_url)

def transcribe_audio(file_path, transcript_output_file, speaker_output_file, timeout=600):
    with open(file_path, 'rb') as audio_file:
        response = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/mp3',
            model='en-US_Multimedia',  # Use the multimedia model
            timestamps=True,
            speaker_labels=True,
            inactivity_timeout=timeout  # Set the timeout
        ).get_result()

    with open(transcript_output_file, 'w') as transcript_file:
        for result in response['results']:
            for alternative in result['alternatives']:
                print(f"Transcript: {alternative['transcript']}\n")
                for word in alternative['timestamps']:
                    transcript_file.write(f"Word: {word[0]}, Start: {word[1]}, End: {word[2]}\n")
                transcript_file.write("\n")
        
    if 'speaker_labels' in response:
        with open(speaker_output_file, 'w') as speaker_file:
            speaker_labels = response['speaker_labels']
            for speaker_label in speaker_labels:
                speaker_file.write(f"Speaker: {speaker_label['speaker']}, Start: {speaker_label['from']}, End: {speaker_label['to']}\n")

input_file_path = '\\temporary\\audio.mp3'
transcript_output_file = '\\temporary\\transcripts.txt'
speaker_output_file = '\\temporary\\speaker.txt'
transcribe_audio(input_file_path, transcript_output_file, speaker_output_file)

from moviepy.editor import VideoFileClip
import os

def convert_mp4_to_mp3(mp4_file, output_folder):
    mp3_file = os.path.join(output_folder, "audio.mp3")
    
    # If the output file already exists, delete it
    if os.path.exists(mp3_file):
        os.remove(mp3_file)
    
    video = VideoFileClip(mp4_file)
    audio = video.audio
    audio.write_audiofile(mp3_file)
    audio.close()
    return mp3_file

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python converter.py input_mp4_file output_folder")
        sys.exit(1)
    
    mp4_file = sys.argv[1]
    output_folder = sys.argv[2]
    
    # Check if the input MP4 file exists
    if not os.path.isfile(mp4_file):
        print(f"Error: {mp4_file} does not exist.")
        sys.exit(1)
    
    # Ensure the output folder exists; create it if it doesn't
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Convert MP4 to MP3
    mp3_file_path = convert_mp4_to_mp3(mp4_file, output_folder)
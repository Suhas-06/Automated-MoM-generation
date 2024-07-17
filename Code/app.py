import subprocess
from flask import Flask, render_template, request, jsonify, send_file
import os

app = Flask(__name__)

# Define paths
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4'}
OUTPUT_FOLDER = 'C:\\Users\\SuhasGowda\\Desktop\\Code\\meeting_summary\\temporary'
OUTPUT_FILE = 'MoM_Document.doc'  # Adjust this for your output format

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'mp4File' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['mp4File']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        # Save uploaded file to uploads folder
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

    return jsonify({'error': 'Invalid file type'})

@app.route('/upload_transcript', methods=['POST'])
def upload_transcript():
    file = request.files['transcriptFile']
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)
    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

# Route to run MoM document generation workflow
@app.route('/run_workflow', methods=['POST'])
def run_workflow_route():
    data = request.get_json()
    filename = data.get('filename')

    if filename:
        mp4_file = os.path.join(UPLOAD_FOLDER, filename)
        try:
            # Execute workflow with the uploaded file
            mom_generation_result = run_workflow(mp4_file)
            return jsonify({'message': 'MoM document generation started for ' + filename, 'result': mom_generation_result})
        except Exception as e:
            return jsonify({'error': 'Failed to start MoM document generation', 'details': str(e)})
    else:
        return jsonify({'error': 'No filename provided'})

@app.route('/run_workflow_from_transcript', methods=['POST'])
def run_workflow_from_transcript():
    # Handle generating MoM document from transcript file
    data = request.get_json()
    filename = data['filename']
    mom_content = generate_mom_from_transcript(filename)
    return jsonify({'message': 'MoM document generation started for ' + filename, 'result': mom_content})

def generate_mom_from_transcript(filename):
    subprocess.run(['python', 'MoM.py', filename], check=True)
    print("Generated MoM document")
    # Read the generated MoM document and return its content
    with open(os.path.join(OUTPUT_FOLDER, OUTPUT_FILE), 'r') as file:
        return file.read()

# Function to run workflow and generate MoM document
def run_workflow(mp4_file):
    try:
        # Execute converter.py
        subprocess.run(['python', 'converter.py', mp4_file, OUTPUT_FOLDER], check=True)
        print("Converted to mp3")
        
        # Execute transcription.py (generates transcription.txt and speaker.txt)
        subprocess.run(['python', 'transcript.py'], check=True)
        print("Converted audio to transcript")
        
        # Execute pre.py (processes transcription.txt and speaker.txt)
        subprocess.run(['python', 'pre.py'], check=True)
        print("Processed the transcript")
        
        # Execute MoM.py (generates MoM document)
        file_path = "C:\\Users\\SuhasGowda\\Desktop\\Code\\meeting_summary\\temporary\\preprocessed.txt"
        subprocess.run(['python', 'MoM.py' ,file_path], check=True)
        print("Generated MoM document")

        # Read the generated MoM document and return its content
        with open(os.path.join(OUTPUT_FOLDER, OUTPUT_FILE), 'r') as file:
            return file.read()

    except subprocess.CalledProcessError as e:
        print(f"Error during subprocess execution: {e}")
        raise

# Route to download MoM document
@app.route('/download_mom')
def download_mom_document():
    mom_file_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    return send_file(mom_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False,use_reloader=False)

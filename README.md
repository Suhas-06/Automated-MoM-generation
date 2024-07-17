# Meeting Summarizer & MoM Generator

## Overview

This project streamlines meeting management through a user-friendly web interface. Users can upload MP4 files containing audio content or transcripts directly, enabling automated processing and generation of Minutes of Meeting (MoM) documents. It also allows users to download the generated MoM document as a Word document.

## Workflow

1. **converter.py**: Converts MP4 files to MP3 format using MoviePy.
2. **transcript.py**: Sends the MP3 file to IBM Watson Speech to Text, returning speaker labels and transcripts with timestamps.
3. **pre.py**: Combines speaker labels and transcripts to create a unified transcript file with timestamps.
4. **app.py**: Runs the frontend, allowing users to upload MP4 files or transcripts directly, making the previous scripts optional.
5. **MoM.py**: Generates comprehensive Minutes of Meeting (MoM) documents from the transcript, displayed on the web interface via app.py.

## Features

- **Upload Options**: Upload MP4 files for automatic processing or directly upload transcript files.
- **Downloadable MoM Document**: Allows users to download MoM documents as Word files for easy access and sharing.

## Use Cases

1. **📋 Meeting Documentation**: Automatically generate minutes of meetings for accurate records.
2. **✅ Action Item Tracking**: Outline action items and owners for accountability.
3. **🎓 Education**: Summarize lecture recordings and provide transcripts for students.
4. **🏢 Corporate Communication**: Summarize corporate meetings for better communication and maintain detailed meeting records for auditing and compliance.
5. **♿ Accessibility**: Provide transcripts to support participants with hearing impairments.

## Technologies Used

- **MoviePy**: For converting MP4 files to MP3 format.
- **IBM Watson Speech-to-Text**: Converts audio content into transcripts and speaker labels.
- **LLAMA-3-70b-instruct Model**: Generates Minutes of Meeting documents, including summaries and action items.
- **Flask and HTML API**: Facilitates backend communication and frontend rendering for user interactions.

## Prerequisites

Before running the project, ensure you have the following:

- An IBM API key for using IBM models.
- File paths for any local files you need to reference.

## Setup

- Replace API Keys and URLs.
- Update File Paths: Replace all placeholder file paths in the scripts with your actual file paths.
- Install Dependencies: Install the necessary Python packages using pip.

## Usage

### Run the Flask Application:
- To start the application, run:
```bash
python app.py
```
### Access the Application:
- Open a web browser and navigate to http://127.0.0.1:5000 to use the application locally

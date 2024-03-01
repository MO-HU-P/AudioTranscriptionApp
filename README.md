# Audio Transcription App

This repository contains an audio transcription application implemented using Streamlit. The app provides functionality to transcribe audio files using either the OpenAI API or a custom Whisper model.

## Features

- **Upload Audio File:** Users can upload audio files in formats such as m4a, mp3, webm, mp4, mpga, or wav.

- **Transcription Methods:**
  - **OpenAI API:** Utilizes the OpenAI API for transcription.
  - **Whisper Model:** Uses a custom Whisper Model for transcription.
  
- **Transcription Execution:**
  - Upon selecting the transcription method and uploading an audio file, users can execute the transcription process.
  - The file size processed by the OpenAI API is limited to 25 MB. If the file size is within the limit of 25 MB, the transcription process begins immediately.
  - For larger files exceeding the size limit, users have the option to split the file into smaller chunks. This effectively splits files so that they do not exceed 25 MB. A new folder is created in the same directory as the uploaded audio file to contain the split file. Replace the currently uploaded file with one of the split files and submit it separately to the API.

- **Transcription Display:**
  - The app displays the transcription results once the process is complete.
  - Results are shown directly on the app interface for easy access.

- **Download Transcription:**
  - Users can download the transcription results as a CSV file for further analysis or reference. Note that the result display on the interface will be cleared as it is transcribed to a CSV file.

## Usage

1. Clone the repository to your local machine.
2. Install the necessary dependencies listed in the `requirements.txt` file.
3. Set up the environment variables, including the OpenAI API key, if using the OpenAI API for transcription.
4. Run the `main.py` file.
5. Select the desired transcription method and upload an audio file.
6. Execute the transcription process and view/download the results.

## Dependencies

- streamlit
- openai
- torch
- pathlib
- dotenv
- faster_whisper

## Note

- Ensure that you have proper access and permissions for utilizing the OpenAI API, including providing the required API key.
- When using OpenAI's API, audio files up to 25 MB are supported. Files larger than that must be split for transcription.
- The Whisper model uses whisper-large-v3 from OpenAI. For efficient transcription using this model, please consider using a CUDA-enabled device for faster processing; if CUDA is not available, transcription will run on the CPU.

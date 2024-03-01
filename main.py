import streamlit as st
import os
import openai
import torch
from pathlib import Path
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()  # Loading environment variables

# Function to split audio file into smaller chunks
def split_audio_file(audio_file, max_size=25000000):
    # Calculate the number of chunks required based on maximum size
    num_chunks = -(-audio_file.size // max_size)
    # Create a directory to store split files if it doesn't exist
    split_dir = Path("split_files")
    split_dir.mkdir(exist_ok=True)

    # Split the file into chunks
    with audio_file as f:
        for i in range(num_chunks):
            # Read chunk_size bytes from the audio file
            chunk_data = f.read(max_size)
            # Create a new file for the chunk
            with open(split_dir / f"split_{i}.wav", "wb") as chunk_file:
                chunk_file.write(chunk_data)

    st.info('Completed splitting of files. Please replace the currently uploaded file with one of the split files and proceed to send it individually to the API.')


# Main function to run the Streamlit app
def main():

    st.title("Audio Transcription App") 

    # File uploader to upload audio files
    audio_file = st.file_uploader("Please upload audio file", type=["m4a", "mp3", "webm", "mp4", "mpeg", "mpga", "wav"])

    # Displaying the audio file if uploaded
    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")

    # Radio button to choose the transcription method
    transcription_method = st.radio("Choose transcription method", ("OpenAI API", "Whisper Model"))

    # Setting the OpenAI API key from environment variables
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Warning message if API key is not provided
    if not openai.api_key and transcription_method == "OpenAI API":
        st.warning("API key not provided.")  
    
    # Initializing variable to store CSV data
    csv_data = ""
    
    # Button to execute transcription
    if st.button("Execute transcription") and audio_file is not None and audio_file.size <= 25000000:
       
        # Displaying spinner while transcription is in progress
        with st.spinner("Transcribing..."):    
            
            # Transcribing using OpenAI API
            if transcription_method == "OpenAI API":
                transcript = openai.Audio.transcribe("whisper-1", audio_file)["text"]
                st.success("Transcription complete!") # Success message for successful transcription
                st.write(transcript)   # Displaying the transcription
                csv_data = transcript + "\n"   # Storing transcription data for CSV
            
            # Transcribing using Whisper Model
            elif transcription_method == "Whisper Model":
                model_size = "large-v3"
                device = "cuda" if torch.cuda.is_available() else "cpu"
                compute_type = "float16" if torch.cuda.is_available() else "int8"
                model = WhisperModel(model_size, device=device, compute_type=compute_type)
                segments, _ = model.transcribe(audio_file, beam_size=5)
                st.success("Transcription complete!")
                for segment in segments:
                    st.write(segment.text)
                    csv_data += segment.text + "\n"

        # Download button for downloading transcription as CSV
        st.download_button(
            label="Download Transcription as CSV",
            data=csv_data.encode('utf-8'),
            file_name='transcription.csv',
            mime='text/csv',
        )

    # Handling the case where file size exceeds 25 MB
    elif transcription_method == "OpenAI API" and audio_file is not None and audio_file.size > 25000000:
        # Warning message if file size exceeds the limit
        st.warning('File exceeds the limit size of 25 MB. Do you want to split the file?')

        # Button to split the file
        if st.button("Yes"):
            split_audio_file(audio_file) # Calling function to split the file

        # Button to cancel the operation
        if st.button("Cancel"):
           st.info("Please reload your browser for a fresh start!")  # Prompting the user to reload the browser if they choose to cancel. 

if __name__ == "__main__":
    main()

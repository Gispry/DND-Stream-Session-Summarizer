import time
from openai import OpenAI
import os
import creds
import logging
import re

# Your existing sanitize_text function
def sanitize_text(text):
    sanitized_text = re.sub(r'[^\w\s,.!?-]', '', text)
    return sanitized_text

# Configure logging
logging.basicConfig(filename='deletion_log.txt', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s:%(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

client = OpenAI(
    api_key=creds.OPENAI_API_KEY
)

def transcribe_audio(file_path):
    # Load audio file
    with open(file_path, "rb") as audio_file:
        # Transcribe
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    # Return the sanitized transcribed text
    transcribed_text = sanitize_text(transcription.text)
    print(transcribed_text)  # This print is now safe
    return transcribed_text

def transcribe_and_summarize(file_path):
    transcription_text = transcribe_audio(file_path)
    # No need to open 'Transcription.txt' just to clear it (if that's the intention)
    if transcription_text:
        # Safely append sanitized text to 'History.txt'
        with open('History.txt', 'a', encoding='utf-8') as f:
            f.write(transcription_text + '\n')
    else:
        print("Transcription is empty or not meaningful.")

if __name__ == "__main__":
    try:
        while True:
            print("Starting the transcription and summarization loop...")
            for i in range(1, 7):
                audio_file = f'audio{i}.wav'
                while not os.path.exists(audio_file):
                    print(f"Waiting for {audio_file} to be available...")
                    time.sleep(5)
                transcribe_and_summarize(audio_file)
                
                logging.info(f'Attempting to delete file: {audio_file}')
                try:
                    os.remove(audio_file)
                    logging.info(f'Successfully deleted file: {audio_file}')
                except Exception as e:
                    # Ensure error message is also sanitized before printing/logging
                    sanitized_error = sanitize_text(str(e))
                    print(f"An error occurred: {sanitized_error}")
                    logging.error(f'Error deleting file: {audio_file}. Exception: {sanitized_error}')
    except KeyboardInterrupt:
        print("Stopped by user")
    except Exception as e:
        sanitized_error = sanitize_text(str(e))
        print(f"An error occurred: {sanitized_error}")
        logging.error(f'Unhandled exception: {sanitized_error}')

import os
from huggingface_hub import InferenceClient

def transcribe_audio(audio_file):
    client = InferenceClient(token=os.getenv("HF_TOKEN"))
    audio_data = audio_file.read()
    transcription = client.automatic_speech_recognition(audio_data)
    return transcription["text"]
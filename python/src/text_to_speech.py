import csv
import re
import os
from pathlib import Path
from pydub import AudioSegment
from openai import OpenAI

client = OpenAI()
AUDIO_OUTPUT_DIR = Path(__file__).parent.parent / "output" / "audio"
MODEL = "tts-1"
HOST1_VOICE = "echo"
HOST2_VOICE = "onyx"
print(f"Audio output dir: {AUDIO_OUTPUT_DIR}")

# Read a csv file and for each row, generate a text-to-speech audio file
# using the OpenAI API. The audio files are saved in a directory called output/audio.
def text_to_speech():
    with open("dialogue_1.2.1.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            role = row["role"]
            if role == "system":
                continue

            speech = row["speech"]
            id = row["id"]

            file_name = Path(AUDIO_OUTPUT_DIR) / f"{role}-{id}.mp3"
            print(f"Generating audio for {role} with id {id}...")
            response = client.audio.speech.create(
                model=MODEL,
                voice=HOST1_VOICE if role == "Zabba" else HOST2_VOICE,
                input=speech
            )

            print(f"Saving audio to {file_name}...")
            response.stream_to_file(file_name)

def extract_file_number(file_name):
    pattern = re.compile(r"(?:\d+)")
    return int(re.search(pattern, file_name).group())

def combine_audio_files():
    files = os.listdir(AUDIO_OUTPUT_DIR)
    files.sort(key=lambda x: extract_file_number(x))
    combined = AudioSegment.empty()
    for file_name in files:
        audio = AudioSegment.from_file(AUDIO_OUTPUT_DIR / file_name)
        combined += audio
        print(f"Combined {file_name} tp combined.mp3...")
    
    combined.export(AUDIO_OUTPUT_DIR / "combined.mp3", format="mp3")


if __name__ == "__main__":
    text_to_speech()
    combine_audio_files()

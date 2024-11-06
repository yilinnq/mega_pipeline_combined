# combines each component of the mega-pipeline

import subprocess

def transcribe_audio():
    # from Tutorial:
    #  Should download all the required data from GCS bucket
    subprocess.run(["python", "transcribe_audio/transcribe_audio_cli.py", "-d"])
    # Should transcribe audio to text and save it locally
    subprocess.run(["python", "transcribe_audio/transcribe_audio_cli.py", "-t"])
    # Should upload the transcribed text to the remote GCS bucket
    subprocess.run(["python", "transcribe_audio/transcribe_audio_cli.py", "-u"])

def generate_text():
    # from Tutorial:
    # Should download all the required data from GCS bucket
    subprocess.run(["python", "generate_text/generate_text_cli.py", "-d"])
    # Should generate text using GPT2 or OpenAI API and save it locally
    subprocess.run(["python", "generate_text/generate_text_cli.py", "-g"])
    # Should upload the generated text to the remote GCS bucket
    subprocess.run(["python", "generate_text/generate_text_cli.py", "-u"])

def synthesis_audio_en():
    # from Tutorial:
    # Should download all the required data from GCS bucket
    subprocess.run(["python", "synthesis_audio_en/synthesis_audio_en_cli.py", "-d"])
    # Should synthesize audio from text and save it locally
    subprocess.run(["python", "synthesis_audio_en/synthesis_audio_en_cli.py", "-s"])
    # Should upload the audio files to the remote GCS bucket
    subprocess.run(["python", "synthesis_audio_en/synthesis_audio_en_cli.py", "-u"])

def translate_text():
    # from Tutorial:
    # Should download all the required data from the GCS bucket
    subprocess.run(["python", "translate_text/translate_text_cli.py", "-d"])
    # Should translate text from English to French and save it locally
    subprocess.run(["python", "translate_text/translate_text_cli.py", "-t"])
    # Should upload the French text to the remote GCS bucket
    subprocess.run(["python", "translate_text/translate_text_cli.py", "-u"])

def synthesis_audio():
    # Should download all the required data from GCS bucket
    subprocess.run(["python", "synthesis_audio/synthesis_audio_cli.py", "-d"])
    # Should synthesize audio from text and save it locally
    subprocess.run(["python", "synthesis_audio/synthesis_audio_cli.py", "-s"])
    # Should upload the audio files to the remote GCS bucket
    subprocess.run(["python", "synthesis_audio/synthesis_audio_cli.py", "-u"])

def main():
    transcribe_audio()
    generate_text()
    synthesis_audio_en()
    translate_text()
    synthesis_audio()

if __name__ == "__main__":
    main()
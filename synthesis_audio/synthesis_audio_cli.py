"""
Module that contains the command line app.
"""
import os
import argparse
import shutil
import glob
from google.cloud import storage
from google.cloud import texttospeech

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
output_audios = "output_audios"
text_translated = "text_translated"
group_name = "yilinqi" # This needs to be your Group name e.g: group-01, group-02, group-03, group-04, group-05, ...

# Instantiates a client
client = texttospeech.TextToSpeechLongAudioSynthesizeClient()


def makedirs():
    os.makedirs(os.path.join(text_translated,group_name), exist_ok=True)
    os.makedirs(os.path.join(output_audios,group_name), exist_ok=True)


def download():
    print("download")

    # Clear
    shutil.rmtree(text_translated, ignore_errors=True, onerror=None)
    makedirs()

    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(match_glob=f"{text_translated}/{group_name}/input-*.txt")
    for blob in blobs:
        blob.download_to_filename(blob.name)


def synthesis():
    print("synthesis")
    makedirs()

    language_code = "fr-FR" # https://cloud.google.com/text-to-speech/docs/voices
    language_name = "fr-FR-Standard-C" # https://cloud.google.com/text-to-speech/docs/voices

    # Get the list of text file
    text_files = glob.glob(os.path.join(text_translated, group_name, "input-*.txt"))
    for text_file in text_files:
        uuid = os.path.basename(text_file).replace(".txt", "")
        audio_file = os.path.join(output_audios, group_name, uuid + ".mp3")

        if os.path.exists(audio_file):
            continue

        with open(text_file) as f:
            input_text = f.read()
        
        # Check if audio file already exists
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        audio_blob_name = f"{output_audios}/{group_name}/{uuid}.mp3"
        blob = bucket.blob(audio_blob_name)

        if not blob.exists():
            # Set the text input to be synthesized
            input = texttospeech.SynthesisInput(text=input_text)
            # Build audio config / Select the type of audio file you want returned
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
            # voice config
            voice = texttospeech.VoiceSelectionParams(language_code=language_code, name=language_name)

            parent = f"projects/{gcp_project}/locations/us-central1"
            output_gcs_uri = f"gs://{bucket_name}/{audio_blob_name}"

            request = texttospeech.SynthesizeLongAudioRequest(
                parent=parent,
                input=input,
                audio_config=audio_config,
                voice=voice,
                output_gcs_uri=output_gcs_uri,
            )

            operation = client.synthesize_long_audio(request=request)
            # Set a deadline for your LRO to finish. 300 seconds is reasonable, but can be adjusted depending on the length of the input.
            result = operation.result(timeout=300)
            print("Audio file will be saved to GCS bucket automatically.")


def main(args=None):
    print("Args:", args)

    if args.download:
        download()
    if args.synthesis:
        synthesis()


if __name__ == "__main__":
    print("***********SYNTHESIZING AUDIO***********")
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Transcribe audio file to text")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download translated text from GCS bucket",
    )

    parser.add_argument(
        "-s", "--synthesis", action="store_true", help="Synthesis audio"
    )

    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="Upload synthesized audio to GCS bucket",
    )

    args = parser.parse_args()

    main(args)

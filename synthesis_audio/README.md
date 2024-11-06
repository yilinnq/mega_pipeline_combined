# Synthesis Audio

🇫🇷 &rightarrow; 🔊

In this container you will implement the following:
* Read the translated text from the GCS bucket `mega-pipeline-bucket` and folder `text_translated`
* Use Cloud Text-to-Speech API to generate an audio file in French or any other language 
* Save the audio mp3 file in bucket `mega-pipeline-bucket` and folder `output_audios` (use the same file name and change the extension to .mp3)


### Project Setup

* Create a folder `synthesis_audio` or clone this repo

### GCP Credentials File
* Download the `mega-pipeline.json` and save it inside a folder called `secrets` inside `synthesis_audio`
<a href="https://static.us.edusercontent.com/files/mlca0YEYdvkWPNEowJ0o4hOd" download>mega-pipeline.json</a>


### Create Pipfile & Pipfile.lock files
* Add `Pipfile` with the following contents:
```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]

[requires]
python_version = "3.8"
```

* Add `Pipfile.lock` with the following contents:
```
{
    "_meta": {
        "hash": {
            "sha256": "7f7606f08e0544d8d012ef4d097dabdd6df6843a28793eb6551245d4b2db4242"
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.8"
        },
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {},
    "develop": {}
}
```

### Create Dockerfile
* Create a `Dockerfile` and base it from `python:3.8-slim-buster` the official Debian-hosted Python 3.8 image
* Set the following environment variables:
```
ENV PYENV_SHELL=/bin/bash
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json
```

* Ensure we have an up-to-date baseline, and install dependencies by running
```
apt-get update
apt-get upgrade -y
apt-get install -y --no-install-recommends build-essential
```

* Install pipenv
```
pip install --no-cache-dir --upgrade pip
pip install pipenv
```

* Create a `app` folder by running `mkdir -p /app`

* Set the working directory as `/app`
* Add `Pipfile`, `Pipfile.lock` to the `/app` folder
* Run `pipenv sync`

* Add the rest of your files to the `/app` folder
* Add Entry point to `/bin/bash`
* Add a command to get into the `pipenv shell`

* Example dockerfile can be found [here](https://github.com/dlops-io/mega-pipeline#sample-dockerfile)

### Docker Build & Run
* Build your docker image and give your image the name `synthesis_audio`

* You should be able to run your docker image by using:
```
docker run --rm -ti -v "$(pwd)":/app synthesis_audio
```

* The `-v "(pwd)":/app` option mounts your current working directory into the `/app` directory inside the container as a volume. This helps us during app development, so when you change a source code file using VSCode from your host machine, the files are automatically changed inside the container.

### Python packages required
* `pipenv install` the following:
  - `google-cloud-storage`
  - `google-cloud-texttospeech`

* If you exit your container at this point, in order to get the latest environment from the pipenv file, make sure to re-build your docker image again.

### CLI to interact with your code
* Use the given python file [`cli.py`](https://github.com/dlops-io/mega-pipeline/blob/main/synthesis_audio/cli.py)
* Assign your group-number to the `group_name` variable in `cli.py`
* The CLI should have the following command line argument options
```
python cli.py --help
usage: cli.py [-h] [-d] [-s] [-u]

Synthesis audio from text

optional arguments:
  -h, --help       show this help message and exit
  -d, --download   Download paragraph of text from GCS bucket
  -s, --synthesis  Synthesis audio
  -u, --upload     Upload audio file to GCS bucket

```

### Testing your code locally
* Inside your docker shell, make sure you run the following commands:
* `python cli.py -d` - Should download all the required data from GCS bucket
* `python cli.py -s` - Should synthesize audio from text and save it locally
* `python cli.py -u` - Should upload the audio files to the remote GCS bucket
* Verify that your uploaded data shows up in the [Mega Pipeline App](https://ac215-mega-pipeline.dlops.io/)

### OPTIONAL: You can use the cli_11.py script to synthesize audio with Eleven Labs. Eleven Labs allows you to train voice models.
For the cheese app, we have a Pavlos voice model available, which you can use by creating an API key from Eleven Labs. 
To do so, add a file named 11lab_api_key.txt to the secrets folder with the following content: 
XI_API_KEY=<API_KEY>





### OPTIONAL: Push Container to Docker Hub
* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag synthesis_audio <USER NAME>/synthesis_audio`
* Push to Docker Hub: `docker push <USER NAME>/synthesis_audio`

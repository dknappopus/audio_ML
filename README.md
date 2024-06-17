# Getting Started:

## Create a Freesound Account

Go to https://freesound.org and click "Join"

## Request a freesound API key

Go to https://freesound.org/help/developers/ and select "Get API Key". After filling out a form, you should receive a Client id and a Client Secret/API Key. These 2 values will be needed later

## Fork the repo
Fork the repo into your local machine

## Set up local environment

1) Create the freesound folder 
This folder will be used to store audio files on your local machine

Open a terminal window, navigate to your repo and run the following 
~~~
mkdir ./freesound
~~~

2)  Create python virtual environment
~~~
python -m venv aml_venv
~~~

3)   Activate the environment
~~~
./aml_venv/Scripts/activate
~~~

4) Install Packages
~~~
pip install -r requirements.txt
~~~

5) Modify your fs_config.py file in the config folder.
   First, run the following:
   ~~~
   git update-index --skip-worktree config/fs_config.py
   ~~~
   This ensures that when you update the config file, the passwords don't get tracked and uploaded to github on commits.
   Change the fs_cid variable to your client_id you got when you requested your freesound API key
   Change the fs_client_secret variable to your client secret you got when you requested your freesound API key

You're ready to begin!

# Getting Data
freesound_API.ipynb is a python notebook for downloading audio from freesound.org. It is set up to download short audio clips uploaded by the Music Technology Group of the Universitat Pompeu Fabra in Barcelona. These clips are typically simple sounds from single orchestral instruments and make for good demonstrations on audio signal processing. 

# Building and training the model
The audio_ml_nn.ipynb notebook demonstrates how to build a neural network for audio classification. In the future this will be extended to other applications

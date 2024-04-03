# DND-Stream-Session-Summarizer
Listens to your microphone then transcribes what you are saying into text and then when someone in your twitch chat types the command it summarizes everything that has been transcribed into a bullet point summery of what has happened in this session.

# Setup Instructions

To get this bot working, you will need to follow the steps outlined below. Please ensure each step is completed to avoid any issues.

## Prerequisites

1. **Extract the Zip File**: Confirm you have extracted the zip file. This program will not work in its compressed form.

2. **Download Python**: Visit [Python Downloads](https://www.python.org/downloads/release/python-3118/) to download Python. This program was coded in Python 3.11.8, so if you encounter any issues, make sure to use this specific version. 
PLEASE MAKE SURE TO TICK ON THE OPTION TO ADD TO PATH WHEN INSTALLING. 

## Installation Steps

1. **Open Command Prompt as Administrator**: This is necessary for the commands to run properly.

2. **Navigate to the Folder**: Use the `cd` command to go to the folder location in the command prompt. Replace the example path with the path to your downloaded folder. Here's an example command (assume the folder is located in the F Drive):
    ```
    cd /d F:\Ai\Junk\Summeriser
    ```

3. **Install Requirements**: While in the correct folder, run the following command to install the program's requirements:
    ```
    pip install -r requirements.txt
    ```

## Configuration

1. **Open `creds.py`**: Use an editor like VS Code (or Notepad for a simpler option, though it's less readable).

2. **Configure Tokens**:
    - **BOT_TWITCH_TOKEN**: Enter the token of the Twitch account for sending messages within the quotes of `BOT_TWITCH_TOKEN`. You can obtain the token by visiting [Twitch Token Generator](https://twitchtokengenerator.com/), clicking "Bot Chat Token", and copying the Access Token.
    - **USER_TWITCH_TOKEN**: Enter your Twitch channel's token within the quotes of `USER_TWITCH_TOKEN`. This is required for the program to read messages from your channel. You can use the same account for both `BOT_TWITCH_TOKEN` and `USER_TWITCH_TOKEN` if desired.
    - **TWITCH_CHANNEL**: Enter the name of your Twitch channel within the quotes of `TWITCH_CHANNEL`. For example, `TWITCH_CHANNEL = "gispry"`.

3. **OPENAI_API_KEY**: Insert your OpenAI API key in the `OPENAI_API_KEY` section. Obtain the key by signing up or logging in at [OpenAI](https://openai.com/api/) and creating a new secret key.

4. **Customize Duration**: Optionally, adjust the duration for the recording. It's recommended to keep it under 2 minutes due to the token limit of GPT-3.5.

5. **Choose GPT Model**: Change between using gpt3 and gpt4 by adjusting the `GPT_MODEL` setting.

6. **Save and Close**: After configuring, save the `creds.py` file and close the editor.

## Starting the Program

- To start the program, double-click the `start.bat` file. 
- Select what Microphone you want to use from the dropdown
- Select the option to start recording

## Stopping the Program

- Please close the GUI that you are able to use to select your microphone before closing the shell

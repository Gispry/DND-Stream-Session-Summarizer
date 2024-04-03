# DND Stream Session Summarizer

Listens to your microphone, transcribes your words into text, and then summarizes the session into bullet points when a command is issued in your Twitch chat.

# Setup Instructions

Follow these steps to ensure a smooth setup:

## Prerequisites

1. **Extract the Zip File**: Make sure you've extracted the zip file. The program won't work in its compressed form.

2. **Download Python**: Download Python 3.11.8 from the [official Python website](https://www.python.org/downloads/release/python-3118/). This version is recommended for compatibility. **Ensure the 'Add to PATH' option is selected during installation.**

## Installation Steps

1. **Open Command Prompt as Administrator**: Necessary for the proper execution of commands.

2. **Navigate to Your Folder**: Use the `cd` command to navigate to the program's folder. Example:
    ```
    cd /d F:\Ai\Junk\Summeriser
    ```

3. **Install Requirements**: Execute the following to install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Configuration

1. **Edit `creds.py`**: Open this file in a text editor like VS Code or Notepad.

2. **Configure Tokens and Channels**:
    - **BOT_TWITCH_TOKEN**: Insert the bot's Twitch token within quotes.
    - **USER_TWITCH_TOKEN**: Your Twitch channel's token goes here.
    - **TWITCH_CHANNEL**: Your Twitch channel name.
    
    Visit [Twitch Token Generator](https://twitchtokengenerator.com/) for tokens.

3. **OPENAI_API_KEY**: Your OpenAI API key goes here. Obtain it from [OpenAI](https://openai.com/api/).

4. **Customize Duration**: The recording duration can be adjusted. Note the token limit of GPT models.

5. **Choose GPT Model**: Toggle between GPT-3 and GPT-4 in the `GPT_MODEL` setting.

6. **Optional Settings**:
    - **Edit Command Names**: Change the default commands (!history and !recent) in `RECENT` and `HISTORY`.
    - **Adjust 'Recent' Duration**: Modify `LAST_WORDS_COUNT` to change the timeframe considered 'recent'.
    - **Startup Checks**: You can disable startup checks (`CHECK_PERMISSIONS`, `CHECK_AUDIO_FILES`, `CHECK_HISTORY`) by setting them to 'NO'. First-time users should leave these enabled.

7. **Save Changes**: After making your adjustments, save and close `creds.py`.

## Starting the Program

- Run `start.bat` by double-clicking it.
- Choose your microphone and start recording.

## Stopping the Program

- Close the microphone selection GUI before closing the command prompt window.

## Troubleshooting File Permissions

If the program fails to progress after transcribing six audio files, it's likely due to insufficient permissions to modify files. To resolve this:

1. Create a shortcut of `start.bat`.
2. Access shortcut properties > Advanced > Check 'Run as administrator'.
3. Use this shortcut to launch the program with the necessary permissions.

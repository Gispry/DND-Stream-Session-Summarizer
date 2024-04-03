gpt3 = "gpt-3.5-turbo"
gpt4 = "gpt-4-turbo-preview"

# The bot's Twitch Access Token 
BOT_TWITCH_TOKEN = ""

# Your Twitch Access Token
USER_TWITCH_TOKEN = ""

# Your TWITCH Channel Name
TWITCH_CHANNEL = ""

# Your OpenAI API Key
OPENAI_API_KEY = ""

#The duration of time that the program records your audio for. The longer this is the bigger the prompt will be that is sent to GPT
Duration = 20 #in seconds

# The sample rate your microphoen will use. Likely should leave it as is unless you know what you are doing. 
SAMPLERATE = 44100 #Hz

#The Version of ChatGPT that you want to use. gpt3 is cheaper with less tokens and gpt4 is more expensive with a lot more tokens
GPT_MODEL = gpt3

#COMMANDS ARE SET HERE.
#This is what people will type in chat after a ! to get a summery. The default is !recent and !history

#Command for the recent summery. Default is set to 10 minutes or 1500 words but that can be changed with LAST_WORDS_COUNT
RECENT = "recent"
#Command for the summery of the whole history.txt file
HISTORY = "history"

#When someone wants the RECENT summery how many words should be used to summerise what happened recently?
#If you are using gpt3 you cannot go above 7000
LAST_WORDS_COUNT = 1500  

# Enable or disable checks
CHECK_PERMISSIONS = 'YES'  # Set to 'NO' to disable the permission check
CHECK_AUDIO_FILES = 'YES'  # Set to 'NO' to disable the audio file check
CHECK_HISTORY = 'YES'  # Set to 'NO' to disable the history file check

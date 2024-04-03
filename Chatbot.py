import creds
import asyncio
from openai import OpenAI
from twitchio.ext import commands
import os

client = OpenAI(
    api_key=creds.OPENAI_API_KEY
)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()

def gpt_history(engine=creds.GPT_MODEL, temp=0.9, tokens=400, freq_pen=2.0, pres_pen=2.0, stop=None):  
    transcription_content = read_file("history.txt")  # Read the content of the file
    words = transcription_content.split()
    
    # Segment the content into chunks of up to 100,000 words
    word_limit = 100000
    segments = [' '.join(words[i:i+word_limit]) for i in range(0, len(words), word_limit)]
    segment_summaries = []

    # Initialize a counter to track segment numbers
    segment_counter = 1
    
    # Summarize each segment
    for segment in segments:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following story in bullet points and YOU MUST KEEP SUMMERIES UNDER 200 WORDS: " + segment,
                }
            ],
            model=creds.GPT_MODEL,
        )
        segment_summary = chat_completion.choices[0].message.content
        segment_summaries.append(segment_summary.strip())

        # Print a message to the console after summarizing each segment
        print(f'Segment {segment_counter} summarized successfully.')
        
        # Increment the segment counter
        segment_counter += 1
    
    # Combine the segment summaries into a single string
    combined_summary_content = " ".join(segment_summaries)
    
    # Summarize the combined summaries to produce a final summary
    final_summary_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Summarize the following story in bullet points and YOU MUST KEEP SUMMERIES UNDER 200 WORDS: " + combined_summary_content,
            }
        ],
        model=creds.GPT_MODEL,
    )
    final_summary = final_summary_completion.choices[0].message.content
    return final_summary


def gpt_recent(engine=creds.GPT_MODEL, temp=0.9, tokens=400, freq_pen=2.0, pres_pen=2.0, stop=None):
    content = read_file('history.txt')
    words = content.split()
    # Use the LAST_WORDS_COUNT variable from creds.py
    last_words_count = creds.LAST_WORDS_COUNT
    last_words = " ".join(words[-last_words_count:])
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Summarize the following story in bullet points and YOU MUST KEEP SUMMERIES UNDER 200 WORDS: {last_words}",
            }
        ],
        model=engine,
    )
    response_message = chat_completion.choices[0].message.content
    print(response_message)
    return response_message

def gpt3_summery(content, word_limit=7000):
    words = content.split()
    segments = [' '.join(words[i:i+word_limit]) for i in range(0, len(words), word_limit)]
    segment_summaries = []
    
    for segment in segments:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"Summarize the following story in bullet points and YOU MUST KEEP SUMMERIES UNDER 200 WORDS: {segment}",
                }
            ],
            model=creds.GPT_MODEL,
        )
        segment_summary = chat_completion.choices[0].message.content
        segment_summaries.append(segment_summary.strip())
    
    # Summarize the segment summaries
    final_summary_content = " ".join(segment_summaries)
    final_summary_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Summerise these points into a new bullet list: {final_summary_content}",
            }
        ],
        model=creds.GPT_MODEL,
    )
    final_summary = final_summary_completion.choices[0].message.content
    return final_summary

# Function to check and potentially re-summarize content
async def ensure_summary_length(original_summary):
    word_count = len(original_summary.split())
    if word_count > 300:
        print('Content is too long, re-summerizing')  # Console message for re-summarization
        # If the summary exceeds 500 words, request a shorter summary
        shorter_summary_request = "This summary was too long. Please summarize again under 300 words: " + original_summary
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": shorter_summary_request,
                }
            ],
            model=creds.GPT_MODEL,
        )
        return chat_completion.choices[0].message.content
    else:
        return original_summary

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=creds.BOT_TWITCH_TOKEN, prefix='!', initial_channels=[creds.TWITCH_CHANNEL])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        await self.handle_commands(message)

    @commands.command(name=creds.HISTORY)
    async def history_command(self, ctx):
        await ctx.send("Generating the history summary... Please wait.")
        
        history_text = read_file('history.txt')  # Renamed variable for clarity
        if creds.GPT_MODEL == creds.gpt3:
            initial_summary = gpt3_summery(history_text)  # Adjusted variable name for clarity
        else:
            initial_summary = gpt_history()  # Adjusted variable name for clarity

        # Ensure the summary is within the desired word limit
        final_summary = await ensure_summary_length(initial_summary)
        print(final_summary)
        
        bullet_points = final_summary.split('\n')
        for point in bullet_points:
            if point.strip():  # Skip empty lines
                # Split the point into chunks of 500 characters or less
                for chunk in [point[i:i+500] for i in range(0, len(point), 500)]:
                    await ctx.send(chunk)
                    await asyncio.sleep(2)  # Respect Twitch rate limits and avoid spamming


    @commands.command(name=creds.RECENT)
    async def recent_command(self, ctx):
        # Notify chat that a summary of the recent history is being generated
        await ctx.send("Generating a summary of the recent history... Please wait.")
        
        # Assuming gpt_recent() would be the function to generate the summary for recent content
        initial_summary = gpt_recent()  # Use gpt_recent() for recent summaries

        # Ensure the summary is within the desired word limit
        final_summary = await ensure_summary_length(initial_summary)

        bullet_points = final_summary.split('\n')  # Corrected to use final_summary
        for point in bullet_points:
            if point.strip():
                await ctx.send(point)
                await asyncio.sleep(2)

bot = Bot()
bot.run()

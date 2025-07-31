# ========== Imports ==========
import discord
from discord.ext import commands
from discord import app_commands
import os
import requests
import json
import lxml
import random
from flask import Flask
from threading import Thread
import google.generativeai as genai
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Create a basic Flask app instance
app = Flask('')


# Define a simple route to confirm the bot is alive
@app.route('/')
def home():
    return "Here we go again!"


# Function to run the Flask app on host 0.0.0.0 and port 8080
def run():
    app.run(host='0.0.0.0', port=8080)


# Starts the Flask app in a separate thread so it doesn’t block the bot
def keep_alive():
    t = Thread(target=run)
    t.start()


# ========== Arabic Poem Fetcher ==========
# Scrapes a random Arabic poem from aldiwan.net.
def get_ar_poem():
    """
    Scrapes a random Arabic poem from aldiwan.net and returns the title and content.
    """
    for i in range(25):
        random_poet_id = random.randint(1, 136746)
        url = f"https://www.aldiwan.net/poem{random_poet_id}.html"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        poem_header = soup.find('h2', class_='h3')
        poem_ar = soup.find('div', id='poem_content')

        if not poem_header or not poem_ar:
            continue

        poem_header_text = poem_header.get_text(separator=' ', strip=True).replace('»', ' - ')
        full_ar_poem = poem_ar.get_text(separator='\n').strip()

        if i == 24:
            return "عذرًا، لم أتمكن من العثور على قصيدة لك. يرجى المحاولة مرة أخرى"
        if len(full_ar_poem) > 1500:
            continue
        return poem_header_text + '\n\n' + full_ar_poem


# ========== English Poem ==========
# Fetches a random English poem using the poetrydb API.
def get_en_poem():
    """
    Fetches a random English poem from the PoetryDB API.
    """
    for i in range(25):
        url = "https://poetrydb.org/random/1"
        response = requests.get(url)
        data = response.json()[0]

        title = data.get("title", "Untitled")
        author = data.get("author", "Unknown Author")
        poem_text = "\n".join(data.get("lines", []))
        full_en_poem = f"{title} - {author} \n\n{poem_text}\n"

        if i == 24:
            return "Sorry, I couldn't find a poem for you. Please try again."
        if len(full_en_poem) > 1200:
            continue
        return full_en_poem


# ========== Gemini AI Setup ==========
# Configures the Gemini AI model with your API key.
genai.configure(api_key=os.getenv("TOKEN2"))

# ========== Discord Client Setup ==========
# Sets up the Discord bot client using commands.Bot for slash commands.
# The command_prefix is required but not used for slash commands.
intents = discord.Intents.default()
intents.message_content = True  # Required for message-related intents
bot = commands.Bot(command_prefix='!', intents=intents)


# ========== Bot Ready Event ==========
# Notifies when the bot is connected and ready.
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


# ========== AI Poem Generator ==========
# Generates a creative poem using Gemini based on the given topic.
async def generate_ai_poem(topic):
    """
    Generates a creative poem using Gemini based on the given topic.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            f"You are a polite helpful poet. Your only task is to write a short, creative poem "
            f"about the following topic in the language of the topic text. "
            f"Do not write anything else. Topic: {topic}"
        )
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return "Sorry, the AI is a bit busy right now. Please try again in a moment."


# ========== Slash Commands ==========
# Registers slash commands using the @bot.tree.command() decorator.
@bot.tree.command(name="qafiyah", description="Get a random Arabic poem")
async def qafiyah(interaction: discord.Interaction):
    """
    A slash command that sends a random Arabic poem.
    """
    await interaction.response.send_message(get_ar_poem())


@bot.tree.command(name="poem", description="Get a random English poem")
async def poem(interaction: discord.Interaction):
    """
    A slash command that sends a random English poem.
    """
    await interaction.response.send_message(get_en_poem())


@bot.tree.command(name="aipoem", description="Get a creative poem from the AI on a specific topic.")
@app_commands.describe(topic="The topic for the AI to write a poem about.")
async def aipoem(interaction: discord.Interaction, topic: str):
    """
    A slash command that uses Gemini AI to generate a poem based on a topic.
    """
    # Defer the response to let the user know the bot is thinking
    await interaction.response.defer()

    # Generate the poem asynchronously
    poem = await generate_ai_poem(topic)

    # Send the final poem as a follow-up message
    await interaction.followup.send(poem)


# ========== Keep the Bot Alive ==========
keep_alive()

# ========== Bot Token ==========
# Runs the bot with the provided token
bot.run(os.getenv('TOKEN'))

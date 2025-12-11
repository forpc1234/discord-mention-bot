import discord
import requests
import os
from dotenv import load_dotenv
from webserver import keep_alive
# Load .env file
load_dotenv()
keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Trigger only when bot is mentioned
    if client.user in message.mentions:
        attachments = []
        for a in message.attachments:
            attachments.append({
                "filename": a.filename,
                "url": a.url
            })

        data = {
            "username": str(message.author),
            "content": message.content,
            "attachments": attachments
        }

        try:
            requests.post(WEBHOOK_URL, json=data)
            print("Sent to n8n:", data)
        except Exception as e:
            print("Error sending:", e)

client.run(TOKEN)

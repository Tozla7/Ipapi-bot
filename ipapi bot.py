import discord
from discord.ext import commands
import requests

# Define intents
intents = discord.Intents.all()

# Create a bot instance with intents
bot = commands.Bot(command_prefix="!", intents=intents)

def get_ip_info(api_key, ip_address):
    url = f"http://api.ipapi.com/{ip_address}?access_key={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        if 'ip' in data:
            return f"IP Information:\nIP Address: {data['ip']}\nCountry: {data['country_name']}\nRegion: {data['region_name']}\nCity: {data['city']}\nLatitude: {data['latitude']}\nLongitude: {data['longitude']}"
        else:
            return f"Error: {data['error']['info']}"

    except requests.RequestException as e:
        return f"Error: {e}"

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!ip'):
        # Split the message content into words
        words = message.content.split()

        # Check if there are enough words in the message
        if len(words) >= 2:
            # Extract the IP address from the second word
            ip_address = words[1]
            api_key = 'YOUR IPAPI API KEY'

            ip_info = get_ip_info(api_key, ip_address)

            embed = discord.Embed(title="IP Lookup", color=0x00ff00)
            embed.add_field(name="Result", value=ip_info, inline=False)

            await message.channel.send(embed=embed)
        else:
            # Inform the user that the command is incomplete
            await message.channel.send("Please provide an IP address for lookup.")

bot.run("YOUR BOT TOKEN")

# bot.py
import os
import random
from dotenv import load_dotenv
import requests
import json

# 1
import discord
from discord.ext import commands
import io
import aiohttp





load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!')

def get_cat():
    # just printing response gives me response[200] which is the whole response object. 
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    json_data = json.loads(response.text)
    cat_url = json_data[0]['url']
    return cat_url

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord to the following guilds:')
    for guild in bot.guilds:
        print(f'- {guild}')

@bot.command(name='cat', help='Gets an image of a cat.')
async def get_one_cat(ctx):

    cat_url = get_cat()
   
    async with aiohttp.ClientSession() as session: # creates session
        async with session.get(cat_url) as resp: # gets image from url
            img = await resp.read() # reads image from response
            with io.BytesIO(img) as file: # converts to file-like object
                await ctx.send(file=discord.File(file, "testimage.png"))

        



bot.run(TOKEN)

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
CAT_KEY =os.getenv('CAT_KEY')


bot = commands.Bot(command_prefix='!')

def get_cat():
    # just printing response gives me response[200] which is the whole response object. 
    response = requests.get(f'https://api.thecatapi.com/v1/images/search?api_key={CAT_KEY}')
    json_data = json.loads(response.text)
    return json_data

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = f"{json_data[0]['q']} - {json_data[0]['a'].split(' ')[0]}" # quote and first name of author 
    return quote 


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord to the following guilds:')
    for guild in bot.guilds:
        print(f'- {guild}')

@bot.command(name='cat', help='Gets an image of a cat from TheCatApi.')
async def cat(ctx):

    cat_url = get_cat()[0]['url']
   
    async with aiohttp.ClientSession() as session: # creates session
        async with session.get(cat_url) as resp: # gets image from url
            img = await resp.read() # reads image from response
            with io.BytesIO(img) as file: # converts to file-like object
                await ctx.send(file=discord.File(file, "testimage.png"))

@bot.command(name='quote', help='Gets an inspirational quote from https://zenquotes.io/ api')
async def quote(ctx):
    await ctx.send(get_quote())

@bot.command(name='cat_quote', help='Gets an image of a cat with a quote')
async def cat_quote(ctx):
    await cat(ctx)
    await quote(ctx)

@bot.command(name='cat_quote_otd', help='Gets the cat quote of the day')
async def cat_quote_otd(ctx):
    json_cat = get_cat()
    cat_id = json_cat[0]['id']
    print(cat_id)
    cat_data = {
        'image_id' : cat_id,
        'sub_id' : 'MASTER'
    }

    url = f'https://api.thecatapi.com/v1/favourites?api_key={CAT_KEY}'
    x = requests.post(url, json=cat_data)
    print(x)





        



bot.run(TOKEN)

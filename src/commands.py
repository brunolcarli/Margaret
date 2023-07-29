import discord
from discord.ext import commands
from margaret.settings import __version__


client = commands.Bot(command_prefix='m:', intents=discord.Intents.all())


@client.event
async def on_ready():
    print('Margaret bot ready!')


@client.command(aliases=['v'])
async def version(ctx):
    """
    Bot version
    """
    response = f'''
    Margaret version: {__version__}
    '''
    await ctx.send(response)

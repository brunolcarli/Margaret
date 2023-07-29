import discord
from discord.ext import commands
from margaret.settings import __version__
from src.database import DbHandler
from src.models import User


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


@client.command(aliases=['create', 'rg'])
async def register(ctx):
    """
    Register a new user on database.
    Must mention a member to register!

    Usage:
        m:register @Username
    """
    mentions = ctx.message.mentions
    if not mentions:
        return await ctx.send('You must mention someone @Username')

    member = mentions[0]

    # Check if user already exists first
    exists = DbHandler.get_user(member.id)
    if exists:
        return await ctx.send('Member already registered!')

    DbHandler.create_user(member.id, member.name)

    # Query created user to return its data
    user_data = DbHandler.get_user(member.id)
    if not user_data:
        return await ctx.send('Something wrong happened')
    
    user = User(*user_data)
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.set_thumbnail(url=member.avatar)

    embed.add_field(name='Name', value=user.name, inline=False)
    embed.add_field(name='Challenges', value=user.challenges, inline=False)
    embed.add_field(name='Score', value=user.score, inline=False)
    embed.add_field(name='Last update', value=user.last_update, inline=False)

    return await ctx.send('New user registered:', embed=embed)

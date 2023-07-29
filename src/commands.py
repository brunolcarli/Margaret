import pandas as pd
import discord
from discord.ext import commands
from margaret.settings import __version__
from src.database import DbHandler
from src.models import User
from src.util import authorized


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


@client.command(aliases=['usr', 'u', 'view'])
async def user(ctx):
    """
    View a user data.
    Must mention a member!

    Usage:
        m:user @Username
    """
    mentions = ctx.message.mentions
    if not mentions:
        return await ctx.send('You must mention someone @Username')

    member = mentions[0]

    user_data = DbHandler.get_user(member.id)
    if not user_data:
        return await ctx.send('User not found')
    
    user = User(*user_data)
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.set_thumbnail(url=member.avatar)

    embed.add_field(name='Name', value=user.name, inline=False)
    embed.add_field(name='Challenges', value=user.challenges, inline=False)
    embed.add_field(name='Score', value=user.score, inline=False)
    embed.add_field(name='Last update', value=user.last_update, inline=False)

    return await ctx.send('', embed=embed)


@client.command(aliases=['adds', 's+'])
async def add_score(ctx, value=None):
    """
    Increase user score.
    Must mention a member!
    Must specify a score value!

    Usage:
        m:add_score 10 @Username
    """
    if not authorized(ctx.message.author.id):
        return await ctx.send('Not authorized!')

    mentions = ctx.message.mentions
    if not mentions:
        return await ctx.send('You must mention someone @Username')

    if value is None:
        return await ctx.send('Score value not specified')

    if not value.isdigit():
        return await ctx.send('Score value must be a number')

    member = mentions[0]

    user_data = DbHandler.get_user(member.id)
    if not user_data:
        return await ctx.send('User not found')

    DbHandler.increase_score(member.id, value)

    user_data = DbHandler.get_user(member.id)
    
    user = User(*user_data)
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.set_thumbnail(url=member.avatar)

    embed.add_field(name='Name', value=user.name, inline=False)
    embed.add_field(name='Challenges', value=user.challenges, inline=False)
    embed.add_field(name='Score', value=user.score, inline=False)
    embed.add_field(name='Last update', value=user.last_update, inline=False)

    return await ctx.send('', embed=embed)


@client.command(aliases=['addc', 'c+'])
async def add_challenge(ctx):
    """
    Increase user challenge.
    Must mention a member!

    Usage:
        m:add_challenge @Username
    """
    if not authorized(ctx.message.author.id):
        return await ctx.send('Not authorized!')

    mentions = ctx.message.mentions
    if not mentions:
        return await ctx.send('You must mention someone @Username')

    member = mentions[0]

    user_data = DbHandler.get_user(member.id)
    if not user_data:
        return await ctx.send('User not found')

    DbHandler.increase_challenge(member.id)

    user_data = DbHandler.get_user(member.id)
    
    user = User(*user_data)
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.set_thumbnail(url=member.avatar)

    embed.add_field(name='Name', value=user.name, inline=False)
    embed.add_field(name='Challenges', value=user.challenges, inline=False)
    embed.add_field(name='Score', value=user.score, inline=False)
    embed.add_field(name='Last update', value=user.last_update, inline=False)

    return await ctx.send('', embed=embed)


@client.command(aliases=['top'])
async def top10(ctx):
    """
    Return the Top 10 users ranking.

    Usage:
        m:top10
    """
    users = DbHandler.get_users()
    
    df = pd.DataFrame(users, columns=['ID', 'MEMBER_ID', 'NAME', 'CHALLENGES', 'SCORE', 'LAST_UPDATE'])
    df.sort_values(by='SCORE', ascending=False, inplace=True)

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    for i, row in enumerate(df[['NAME', 'SCORE', 'CHALLENGES']].values[:10]):
        name, score, challenges = row
        embed.add_field(name=f'{i+1}: {name}', value=f'Challenges: {challenges} | Score: {score}', inline=False)        

    return await ctx.send('Top 10 Ranking', embed=embed)

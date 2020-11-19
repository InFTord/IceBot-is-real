import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound

client = commands.Bot(command_prefix=">", case_insensitive=True, intents = discord.Intents(messages=True,members=True,guilds=True))

@client.event
async def on_ready():
    print('Запущен!')
    await client.change_presence(activity=discord.Game(name='>help'))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('Данная команда в данный момент не работает, пожалуйста попробуйте позже!')
        print(error)
    if isinstance(error, CommandNotFound):
        await ctx.message.add_reaction('❌')

@client.command(name='пинг', aliases=['ping'])
async def ping(ctx):
    await ctx.send('Понг!')

@client.command(name='очистка', aliases=['clear', 'c', 'очистить'])
@commands.has_guild_permissions(manage_messages = True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit = amount)
    await ctx.send('✅')


@client.command(name='кик', aliases=['kick', 'выгнать', 'k'])
@commands.has_guild_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason="Причины не дано"):
    await member.kick(reason=reason)
    await ctx.message.add_reaction('✅')
    await member.send(f'Вы были кикнуты с {ctx.guild} по причине {reason}')


client.run('NzA0NTk3NzM1MjYwODE1Mzgw.Xqfdxg.UlB7_nJzdGOiL7XtY14H3EnaIcc')
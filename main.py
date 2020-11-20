# Стандартные импорты, даже говорить ничего о не хочу.

import discord
from discord.ext import commands
from typing import Optional
from discord.ext.commands.errors import CommandNotFound
from discord.member import Member
from config import bot_token, prefix

client = commands.Bot(command_prefix=prefix, case_insensitive=True,
                      intents=discord.Intents(messages=True, members=True, guilds=True))


# Ивенты

@client.event
async def on_ready():
	print(f'{client.user.name} в сети')
	await client.change_presence(activity=discord.Game(name='i!help'))


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.UserInputError):
		await ctx.send(f'Используйте следующие аргументы для данной команды: {ctx.command.usage}')

	if isinstance(error, commands.CommandInvokeError):
		await ctx.send('Данная команда в данный момент не работает, пожалуйста попробуйте позже!')
		print(error)
	if isinstance(error, CommandNotFound):
		await ctx.message.add_reaction('❌')


# Команды

@client.command(name='пинг', aliases=['ping'])
async def ping(ctx):
	await ctx.send('Понг!')


@client.command(name='очистка', aliases=['clear', 'c', 'очистить'], usage='[Количество]')
@commands.has_guild_permissions(manage_messages=True)
async def clear(ctx, amount=2):
	await ctx.channel.purge(limit=amount)
	await ctx.send('✅')


@client.command(name='кик', aliases=['kick', 'выгнать', 'k'], usage='[участник] {причина}')
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="причины не дано"):
	await member.kick(reason=reason)
	await ctx.message.add_reaction('✅')
	embed = discord.Embed(title='Вы были кикнуты!', color=discord.Color.red(), timestamp=ctx.message.created_at)
	embed.add_field(name='Причина:', value=f'```{reason}```', inline=False)
	embed.add_field(name='Кто кикнул:', value=ctx.message.author, inline=False)
	embed.set_footer(text=f'ИД сообщения: {ctx.message.id}')
	await member.send(embed=embed)


@client.command(name='юзеринфо', aliases=['user', 'userinfo', 'профиль', 'u', 'profile'], usage='{пользователь}')
async def user(ctx, member: Optional[Member]):
	member = member or ctx.author
	embed = discord.Embed(description=f'Имя юзера: {member.display_name}\nИД: {member.id}\n', color=member.color)
	await ctx.send(embed=embed)


# Логин бота

client.run(bot_token)

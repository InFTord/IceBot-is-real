# Стандартные импорты, даже говорить ничего о не хочу.

import asyncio
import os
from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound
from discord.member import Member

bot_token = os.getenv("bot_token")
prefix = os.getenv("prefix")

client = commands.Bot(command_prefix=prefix, case_insensitive=True,
                      intents=discord.Intents(messages=True, members=True, guilds=True))


async def status_task():
	while True:
		await client.change_presence(activity=discord.Game(name='i!help'))
		await asyncio.sleep(10)
		await client.change_presence(
			activity=discord.Game(name='Замораживаю {} людей'.format((len(set(client.get_all_members()))))))
		await asyncio.sleep(10)


# Ивенты

@client.event
async def on_ready():
	print(
		'{}#{} в сети\nИД бота: {}\nКоличество юзеров: {}\nВерсия бота: {}'.format(client.user.name),
		client.user.discriminator, client.user.id, (len(set(client.get_all_members()))), discord.__version__)
	await client.change_presence(activity=discord.Game(name='i!help'))
	client.loop.create_task(status_task())


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.UserInputError):
		await ctx.send(f'Используйте следующие аргументы для данной команды: {ctx.command.usage}')

	if isinstance(error, commands.CommandInvokeError):
		await ctx.send('Данная команда в данный момент не работает, пожалуйста попробуйте позже!')
		print(error)
	if isinstance(error, CommandNotFound):
		await ctx.message.add_reaction('❌')
	if isinstance(error, commands.MissingPermissions):
		member = ctx.author
		await member.send("У вас недостаточно прав!")


@client.event
async def on_command_completion(ctx):
	print(f'Была выполнена команда {ctx.command} юзером {ctx.author} на сервере {ctx.guild}')


# Команды

@client.command(name='пинг', aliases=['ping'])
async def ping(ctx):
	await ctx.send(f'Понг!')


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
	embed.add_field(name='Кто кикнул:', value=ctx.message.author.mention, inline=False)
	embed.set_footer(text=f'ИД сообщения: {ctx.message.id}')
	await member.send(embed=embed)


@client.command(name='юзеринфо', aliases=['user', 'userinfo', 'профиль', 'u', 'profile'], usage='{пользователь}')
async def user(ctx, member: Optional[Member]):
	member = member or ctx.author
	embed = discord.Embed(color=member.color, timestamp=member.created_at)
	embed.set_author(name='Информация | Юзеринфо')
	embed.add_field(name='Имя юзера', value=f'{member.display_name}({member.mention})', inline=False)
	embed.add_field(name='ID юзера', value=member.id, inline=False)
	embed.set_thumbnail(url=member.avatar_url)
	embed.set_footer(text=f'Запрос профиля был совершен: {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)


# Логин бота

client.run(bot_token)

# Стандартные импорты, даже говорить ничего о не хочу.

import asyncio
import os
from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound
from discord.member import Member

# Получение переменных в Хероку

bot_token = os.getenv("bot_token")
prefix = os.getenv("prefix")

#  Переменная клиент, без неё нихуя не работает дада

client = commands.Bot(command_prefix=prefix, case_insensitive=True,
                      intents=discord.Intents(messages=True, members=True, guilds=True))
# Удаление стандартного хелпа из бота
client.remove_command('help')


async def status_task():
	while True:
		await client.change_presence(activity=discord.Game(name='i!help'))
		await asyncio.sleep(10)
		await client.change_presence(
			activity=discord.Game(name='заморозку {} людей'.format((len(set(client.get_all_members()))))))
		await asyncio.sleep(10)


# Ивенты

@client.event
async def on_ready():
	print(
		f"{client.user.name}#{client.user.discriminator} в сети\nИД бота: {client.user.id}\nВерсия бота: {discord.__version__}\nКоличество серверов:",
		len(client.guilds), "\nКоличество участников:", len(set(client.get_all_members()))),
	client.loop.create_task(status_task())


# Хандлер ошибок

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.UserInputError):
		embed = discord.Embed(title='Неправильные аргументы | Ошибка', color=discord.Color.red(),
		                      timestamp=ctx.message.created_at)
		embed.add_field(name='Используйте следующие аргументы для данной команды:', value=f'```{ctx.command.usage}```')
		embed.set_footer(text='Я думаю вам надо читать хелп', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	
	if isinstance(error, commands.CommandInvokeError):
		embed = discord.Embed(title='Команда не работает | Ошибка', color=discord.Color.red(),
		                      timestamp=ctx.message.created_at)
		embed.add_field(name='Данная команда в данный момент не работает!',
		                value='Сообщите разработчику бота о данной ошибке!')
		embed.set_footer(text='Пока что юзайте другие команды бота :3', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	
	if isinstance(error, CommandNotFound):
		await ctx.message.add_reaction('❌')
	if isinstance(error, commands.MissingPermissions):
		member = ctx.author
		embed = discord.Embed(title='Недостаточно прав | Ошибка', color=discord.Color.red(),
		                      timestamp=ctx.message.created_at)
		embed.add_field(name='У вас недостаточно прав для использования этой команды!',
		                value='Вы думаете я допущу взлом сервера? А вот и нет.')
		embed.set_footer(text='Получите необходимые права для данной команды :3', icon_url=ctx.author.avatar_url)
		await member.send(embed=embed)
	
	if isinstance(error, commands.BotMissingPermissions):
		embed = discord.Embed(title='Неправильные аргументы | Ошибка', color=discord.Color.red(),
		                      timestamp=ctx.message.created_at)
		embed.add_field(name='У бота недостаточно прав для выполнения данной команды!',
		                value='Выдайте необходимые права для бота')
		embed.set_footer(text='Как мне работать без необходимых прав? :(', icon_url=ctx.author.avatar_url)


@client.event
async def on_command_completion(ctx):
	print(f'Была выполнена команда {ctx.command} юзером {ctx.author} на сервере {ctx.guild}')


# Команды

@client.command(name='пинг', aliases=['ping'])
async def ping(ctx):
	await ctx.send('Понг!')


@client.command(name='очистка', aliases=['clear', 'очистить'], usage='[Количество]')
@commands.has_guild_permissions(manage_messages=True)
async def clear(ctx, amount=2):
	await ctx.channel.purge(limit=amount)


@client.command(name='кик', aliases=['kick', 'выгнать', 'k'], usage='[участник] {причина}')
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="причины не дано"):
	await member.kick(reason=reason)
	await ctx.message.add_reaction('✅')
	embed = discord.Embed(title='Вы были кикнуты!', color=discord.Color.red(), timestamp=ctx.message.created_at)
	embed.add_field(name='Причина:', value=f'```{reason}```', inline=False)
	embed.add_field(name='Кто кикнул:', value=ctx.message.author.mention, inline=False)
	embed.set_footer(text=f'ИД сообщения: {ctx.message.id}', icon_url=ctx.author.avatar_url)
	await member.send(embed=embed)


@client.command(name='юзеринфо', aliases=['user', 'userinfo', 'профиль', 'u', 'profile'], usage='{пользователь}')
async def user(ctx, member: Optional[Member]):
	if not ctx.guild:
		member = member or ctx.author
		embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
		embed.set_author(name='Информация | Юзеринфо')
		embed.add_field(name='Имя юзера', value=f'{member.display_name}({member.mention})', inline=False)
		embed.add_field(name='Дата создания аккаунта юзера:', value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"),
		                inline=False)
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f'Запрос профиля был совершен: {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)
	
	else:
		member = member or ctx.author
		embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
		embed.set_author(name='Информация | Юзеринфо')
		embed.add_field(name='Имя юзера', value=f'{member.display_name}({member.mention})', inline=False)
		embed.add_field(name='Дата создания аккаунта юзера:', value=member.created_at.strftime("%d/%m/%Y %H:%M:%S"),
		                inline=False)
		embed.add_field(name='Дата захода юзера на сервер:', value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"),
		                inline=False)
		embed.set_thumbnail(url=member.avatar_url)
		embed.set_footer(text=f'Запрос профиля был совершен: {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
		await ctx.send(embed=embed)


# Напоминание - доработать хелп

@client.command(name='хелп', aliases=['помощь', 'commands', 'команды', 'c', 'help'])
async def help(ctx):
	embed = discord.Embed(color=discord.Color.green(), timestamp=ctx.message.created_at)
	embed.set_author(name='Информация | Помощь по командам')
	embed.add_field(name='i!профиль', value='Можно просмотреть чей то профиль')
	embed.add_field(name='i!кик', value='Кто то нарушает правила? Дайте ему кик, что бы перестал!')
	embed.add_field(name='i!очистить',
	                value='Можно убирать чей то флуд за секунды!',
	                inline=False)
	embed.add_field(name='i!пинг', value='Просто пинг.', inline=True)
	embed.set_footer(text='Данный хелп еще в разработке, так что а)', icon_url=ctx.author.avatar_url)
	await ctx.send(embed=embed)


# Логин бота

if __name__ == '__main__':
	# When running this file, if it is the 'main' file
	# I.E its not being imported from another python file run this
	for file in os.listdir("./cogs"):
		if file.endswith(".py") and not file.startswith("_"):
			client.load_extension(f"cogs.{file[:-3]}")

client.run(bot_token)

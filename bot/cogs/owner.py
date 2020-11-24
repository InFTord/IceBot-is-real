import asyncio
import os
import traceback

import discord
from discord.ext import commands


class Owner(commands.Cog):
	
	def __init__(self, client):
		self.client = client
	
	@commands.command(name='load', aliases=['загрузить', 'лоад'], description='Позволяет загружать коги')
	@commands.is_owner()
	async def loading(self, ctx, cog):
		embed = discord.Embed(сolor=discord.Color.green(),
		                      timestamp=ctx.message.created_at)
		ext = f"{cog.lower()}.py"
		if not os.path.exists(f"./cogs/{ext}"):
			# if the file does not exist
			embed.add_field(
				name=f"Невозможно загрузить ког: `{ext}`",
				value="Этого кога не существует.",
				inline=False
			)
		
		elif ext.endswith(".py") and not ext.startswith("_"):
			try:
				self.client.load_extension(f"cogs.{ext[:-3]}")
				embed.add_field(
					name=f"Загружен ког: `{ext}`",
					value='\uFEFF',
					inline=False
				)
			except Exception:
				desired_trace = traceback.format_exc()
				embed.add_field(
					name=f"Ошибка в загрузке: `{ext}`",
					value=desired_trace,
					inline=False
				)
		await ctx.send(embed=embed)
	
	@commands.command(name='unload', aliases=['отгрузить', 'онлоад'], description='Отгрузка когов.')
	@commands.is_owner()
	async def unloading(self, ctx, cog):
		embed = discord.Embed(color=discord.Color.green(),
		                      timestamp=ctx.message.created_at)
		ext = f"{cog.lower()}.py"
		if not os.path.exists(f"./cogs/{ext}"):
			# if the file does not exist
			embed.add_field(
				name=f"Невозможно отгрузить: `{ext}`",
				value="Этого кога не существует.",
				inline=False
			)
		
		elif ext.endswith(".py") and not ext.startswith("_"):
			try:
				self.client.unload_extension(f"cogs.{ext[:-3]}")
				embed.add_field(
					name=f"Отгружен ког: `{ext}`",
					value='\uFEFF',
					inline=False
				)
			except Exception:
				desired_trace = traceback.format_exc()
				embed.add_field(
					name=f"Ошибка в отгрузке: `{ext}`",
					value=desired_trace,
					inline=False
				)
		await ctx.send(embed=embed)
	
	@commands.command(name='перезагрузить',
	                  aliases=['reload'],
	                  description="Овнер бота может перезагружать коги, используя эту команду",
	                  usage="[ког (можно без упоминания кога, тогда все коги перезагрузятся)]"
	                  )
	@commands.is_owner()
	async def reload(self, ctx, cog=None):
		if not cog:
			async with ctx.typing():
				embed = discord.Embed(
					title="Перезагрузка всех когов!",
					color=discord.Color.green(),
					timestamp=ctx.message.created_at
				)
				for ext in os.listdir("./cogs/"):
					if ext.endswith(".py") and not ext.startswith("_"):
						try:
							self.client.unload_extension(f"cogs.{ext[:-3]}")
							self.client.load_extension(f"cogs.{ext[:-3]}")
							embed.add_field(
								name=f"Перезагружено: `{ext}`",
								value='\uFEFF',
								inline=False
							)
						except Exception as e:
							embed.add_field(
								name=f"Невозможно перезагрузить `{ext}`",
								value=e,
								inline=False
							)
						await asyncio.sleep(0.5)
				await ctx.send(embed=embed)
		else:
			# reload the specific cog
			async with ctx.typing():
				embed = discord.Embed(
					title="Перезагружаю определенный ког",
					color=0x808080,
					timestamp=ctx.message.created_at
				)
				ext = f"{cog.lower()}.py"
				if not os.path.exists(f"./cogs/{ext}"):
					# if the file does not exist
					embed.add_field(
						name=f"Невозможно перезагрузить: `{ext}`",
						value="Этого кога не существует.",
						inline=False
					)
				
				elif ext.endswith(".py") and not ext.startswith("_"):
					try:
						self.client.unload_extension(f"cogs.{ext[:-3]}")
						self.client.load_extension(f"cogs.{ext[:-3]}")
						embed.add_field(
							name=f"Перезагружено: `{ext}`",
							value='\uFEFF',
							inline=False
						)
					except Exception:
						desired_trace = traceback.format_exc()
						embed.add_field(
							name=f"Ошибка в перезагрузке: `{ext}`",
							value=desired_trace,
							inline=False
						)
				await ctx.send(embed=embed)


def setup(client):
	client.add_cog(Owner(client))

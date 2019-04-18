import discord
from discord.ext import commands

import sys, traceback, os
import asyncio, aiohttp

TOKEN = "NDc1MTExNzI3NDMyODU5Njg0.XLgVTg.uIBM9lw5XgRPJH38DNP9kgnS6XE" #DizyBot

PREFIXES = [',,']

EXTENSIONS = ['jishaku',
			'cogs.admin']


class Main(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=self.get_prefix, description='Welcome', case_insensitive=True)
	
	
		self.session= aiohttp.ClientSession(loop=self.loop)
		

	async def get_prefix(self, message):
		return commands.when_mentioned_or(*PREFIXES)(self, message)


	async def on_ready(self):   
		print(f'''\n\nLogged in as:
{self.user.name}
ID: {self.user.id}\nVersion: {discord.__version__}\n''')
		await self.change_presence(
			activity=discord.Streaming(
				name='Rick Astley - Never Gonna Give You Up', 
				url='https://twitch.tv/xouranl')
			)
	    
		print(f'Successfully logged in and booted...!''')
	
	
	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)
			
			
	def run(self):
		for extension in EXTENSIONS:
			try:
				self.load_extension(extension)
			except Exception as e:
				print(f'Failed to load extension {extension}.', file=sys.stderr)
				traceback.print_exc()
		super().run(TOKEN, reconnect=True)
		
		
	
if __name__=="__main__":
	Main().run()
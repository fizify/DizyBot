import discord
from discord.ext import commands

import sys, traceback, os
import asyncio, aiohttp
from utils import vars,custom




initial_extensions = [
					'jishaku',
					'utils.handler',
					'cogs.Admin',
					'cogs.Apps'
					]


class Main(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=self.get_prefix, description='Welcome', case_insensitive=True)
	
		self.session= aiohttp.ClientSession(loop=self.loop)
		self.usage={}
		
	


	async def get_prefix(self, message):
		prefixes = vars.prefixes
		return commands.when_mentioned_or(*prefixes)(self, message)
	
	
	

	async def on_ready(self):   
		print(f'''\n\nLogged in as:
{self.user.name}
ID: {self.user.id}\nVersion: {discord.__version__}\n''')
		await self.change_presence(
			activity=discord.Streaming(
				name='everything.', 
				url='https://twitch.tv/xouranl')
			)
	    
		print(f'Successfully logged in and booted...!''')
	
	
	async def on_message(self, message):
		await custom.on_message(self, message)
		if not message.author.bot:
			await self.process_commands(message)
			
			
	async def on_message_edit(self, before, after):
		await custom.on_message_edit(self, before, after)
	
	
	async def on_message_delete(self, message):
		await custom.on_message_delete(self, message)
		
	
	async def on_command(self, ctx):
		await custom.on_command(self, ctx)
	
	
	def run(self):
		for extension in initial_extensions:
			try:
				self.load_extension(extension)
			except Exception as e:
				print(f'Failed to load extension {extension}.', file=sys.stderr)
				traceback.print_exc()
		super().run(vars.token, reconnect=True)
		
		
	
if __name__=="__main__":
	Main().run()
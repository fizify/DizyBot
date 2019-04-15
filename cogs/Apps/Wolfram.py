import discord
from discord.ext import commands

from utils import *

from utils.paginator import paginate




QUERY= "http://api.wolframalpha.com/v2/"

embed= discord.Embed(color=vars.Wolfram[2])
embed.set_author(name='WolframAlpha', icon_url=vars.Wolfram[1])

@commands.command(aliases=['wolf','wr'], invoke_without_subcommand=True)
@commands.cooldown(1,10, commands.BucketType.guild)
async def wolfram(self, ctx, *,query):
	"""Requests all answers on a single image."""
	
	request='simple'
	params={'i':query ,
		'appid': vars.wolfram_key
		}
	
	url= QUERY+request
	
	async with ctx.channel.typing(), self.bot.session.get(url, params=params) as resp:
		if not resp.status == 200: raise HTTPError(resp.status)
		buffer=await resp.read()
		
	file=discord.File(buffer, filename='wolf.png')
	
	m = await self.bot.get_channel(vars.dump_channel).send(file=file)
	img= m.attachments[0].url
	
	embed.set_image(url= img)
	embed.description= query.capitalize()
	await paginate(ctx, [embed])
	await m.delete()
	
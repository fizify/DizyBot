import discord, json
from discord.ext import commands

from utils import *

from utils.paginator import paginate


from bs4 import BeautifulSoup


@commands.command(aliases=['search','g'])
@commands.cooldown(1,7, commands.BucketType.user)
async def google(self, ctx, *, query):
	"""Does the obvious."""
	
	embeds=[]
	params={'q':query.replace(' ','+'), 'key':vars.google_key, 'cx':vars.google_engine_id, 'safe':'off' if ctx.channel.is_nsfw() else 'active'}
	async with ctx.channel.typing(), self.bot.session.get('https://www.googleapis.com/customsearch/v1', params=params) as resp:
		if not resp.status == 200: raise HTTPError(resp.status)
		r= await resp.json()
	
	if not r.get('items'): raise NoResultsFound(query)
	
	for item in r['items']:
		title= item['title'].capitalize()
		link= item['link']
		description= f'{vars.Link} [Link]({link})' +'\n'+ item['snippet']
		try:
			img= item['pagemap']['cse_image'][0]['src']
			if img.startswith('x-raw-image'):img= item['pagemap']['cse_thumbnail'][0]['src']
		except:img=''
		
		embed= discord.Embed(color=vars.Google[2])
		embed.set_author(name='Google Search', icon_url=vars.Google[1])
		
		embed.description= f'**[{title}]({link})**'+'\n'+description
		embed.set_image(url= img)

		embeds.append(embed)

	await paginate(ctx, embeds)


@commands.command(aliases=['i','picture','pic'])
@commands.cooldown(1,7, commands.BucketType.user)
async def image(self, ctx, *, query):
	"""Search for Images."""
	
	embeds=[]
	params={'q':query.replace(' ','+'), 'key':vars.google_key, 'searchType':'image', 'cx':vars.image_engine_id, 'safe':'off' if ctx.channel.is_nsfw() else 'active'}
	async with ctx.channel.typing(), self.bot.session.get('https://www.googleapis.com/customsearch/v1', params=params) as resp:
		if not resp.status == 200: raise HTTPError(resp.status)
		r= await resp.json()

	if not r.get('items'): raise NoResultsFound(query)
		
	for item in r['items']:
		title= item['title'].capitalize()
		img= item['link']


		embed= discord.Embed(color=vars.Google[2])
		embed.set_author(name='Google Image Search', icon_url=vars.Google[1])
		
		embed.description=  f'**[{title}]({img})**'+ '\n'+ f'{vars.Link} [Link]({img})'
		embed.set_image(url= img)
	
		embeds.append(embed)
	await paginate (ctx, embeds)



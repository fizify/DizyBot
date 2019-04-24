import discord
from discord.ext import commands

from utils import *

from utils.paginator import paginate




@commands.command(aliases=['ud'])
@commands.cooldown(1,7,commands.BucketType.user)
async def urban(self, ctx, *,query):
	
	embeds=[]
	
	url='http://urbanscraper.herokuapp.com/search/'+query.replace(' ','+')
	async with ctx.channel.typing(), self.bot.session.get(url) as resp:
		if not resp.status == 200: raise HTTPError(resp.status)
		searches=(await resp.json())
		
	for desc in searches:
		
		embed=discord.Embed(color=values.Urban[2])
		embed.set_author(name='UrbanDict Search', icon_url=values.Urban[1])
		
		try:
			term       = desc['term'].replace('+',' ').capitalize()
			link       = desc['url']
			definition = desc['definition'].replace('\r','\n')
			example    = '*'+ desc['example'].replace('\r','*\n\t*') +'*'
		except: raise NoResultsFound(query)
		
		embed.description= (f'**[{term}]({link})**'+ '\n'+
							f'{values.Link} [Link]({link})'+'\n'+
							f'**{definition}**'+'\n'+
							f'\t{example}')
		embeds.append(embed)
	await paginate(ctx, embeds)
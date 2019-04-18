import discord
from discord.ext import commands

from utils import *

from utils.paginator import paginate


from bs4 import BeautifulSoup as bs


@commands.command(aliases=['ly','lyric','song','songinfo'])
@commands.cooldown(1,5, commands.BucketType.user)
async def lyrics(self, ctx, *,query):
	"""Fetches song Lyrics"""
	
	embeds=[]
	
	def make_embed(text):
		embed= discord.Embed(color=vars.Genius[2])
		embed.set_author(name= 'Genius Lyrics Search', icon_url= vars.Genius[1])
		
		embed.description= f"**[{result['full_title']}]({result['url']})** \n{vars.Link} [Link]({result['url']})"
		embed.set_image(url= result['header_image_url'])
		embed.description+= '```' + text + '```'
		
		embeds.append(embed)
	
	song=query.replace(' ','%20')
	header={"Authorization":vars.genius_key ,"User-Agent":"Mozila/5.0"}
	
	async with ctx.channel.typing():
		async with self.bot.session.get(f"https://api.genius.com/search?q={song}", headers=header) as resp:
			if not resp.status == 200: raise HTTPError(resp.status)
			json_obj=await resp.json()
			song_list=json_obj['response']['hits']
		if len(song_list)==0:
			raise NoResultsFound(query)
	
		item = song_list[0]
			
		result=item['result']
		async with ctx.channel.typing(), self.bot.session.get(result['url'], headers={'User-Agent':'Mozilla-5.0'}) as page:
			html=bs(await page.text(), 'html.parser')
		lyrics=html.find('div', class_='lyrics').get_text()
		
		while(lyrics != ''):
			lylist= lyrics[:1024].split('\n')
			make_embed( '\n'.join(lylist[:-1]) )
			lyrics= lylist[-1] + lyrics[1024:]
				
	await paginate(ctx, embeds)

import discord
from discord.ext import commands

from utils import *

from utils.paginator import paginate




@commands.command(aliases=['yt','video','vid'])
@commands.cooldown(1,7, commands.BucketType.user)
async def youtube(self, ctx, query):
	"""What do I say about this?"""
	
	embeds=[]
	params={'part':'snippet', 'maxResults':15, 'q':query, 'key':values.youtube_key, 'safeSearch':'none' if ctx.channel.is_nsfw() else 'strict'}
	async with ctx.channel.typing(), self.bot.session.get('https://www.googleapis.com/youtube/v3/search', params=params) as resp:
		if not resp.status == 200: raise HTTPError(resp.status)
		r=await resp.json()
	
	if not r.get('items'): raise NoResultsFound(query)
		
	for item in r['items']:
		title= item['snippet']['title']
		description= ''
		img= item['snippet']['thumbnails']['high']['url']
		
		type= item['id']['kind']; url= ''
		if type == 'youtube#video':
			link= f"https://youtu.be/{item['id']['videoId']}"
			description= '`Video`\n'
		if type == 'youtube#playlist':
			link= f"https://www.youtube.com/playlist?list={item['id']['playlistId']}"
			description= '`Playlist`\n'
		if type == 'youtube#channel':
			link=  f"https://www.youtube.com/channel/{item['id']['channelId']}"
			description= '`Channel`\n'
		
		description+= item['snippet']['description']
		
		embed= discord.Embed(color=values.Youtube[2])
		embed.set_author(name='Youtube Search', icon_url=values.Youtube[1])
		
		embed.description= f'**[{title}]({link})**' +'\n'+  f'{values.Link} [Link]({link})' +'\n'+description
		embed.set_image(url=img)
		
		embeds.append(embed)
	await paginate(ctx, embeds)
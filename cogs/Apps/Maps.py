import discord , io
from discord.ext import commands

from utils import *

from utils.paginator import paginate




@commands.command(name='map',aliases=['maps'])
@commands.cooldown(1,7, commands.BucketType.user)
async def _map(self, ctx, *,place):
	"""Fetches a static map of any place from Google Maps"""
	
	params= { 'center': place,
			'size'    :'800x800',
			'maptype' :'roadmap',
			'key'     :vars.gmaps_key,
			'format'  :'png32'
			}
	
	async with ctx.channel.typing(), self.bot.session.get('https://maps.googleapis.com/maps/api/staticmap', params=params) as resp:
		if not resp.status == 200: raise HTTPError(resp.status)
		buffer =io.BytesIO(await resp.read())
		
	dump= self.bot.get_channel(vars.dump_channel)
	link="http://maps.google.com/?q="+place.replace(' ','+')
	f= discord.File(buffer, filename= place.replace(' ','_')+'.png')
	e= discord.Embed(color= vars.Maps[2])
	e.description= f"{vars.Link} [Link]({link}) \n"
	e.description+= f"**[{place.capitalize()}]({link})**"
	e.set_author(name= 'Maps Search', icon_url= vars.Maps[1])
	
	m= await dump.send(file= f)
	img= m.attachments[0].url
	e.set_image(url= img)
	
	await paginate(ctx, [e])
	await m.delete()
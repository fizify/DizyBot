import discord, time, io, json
from discord.ext import commands

from utils import *

from utils.paginator import paginate




@commands.command(aliases=['ss'])
@commands.cooldown(1.0, 10.0, commands.BucketType.user)
async def screenshot(self, ctx, site):
	"""Screenshot! type in domain names and get screenshots."""
	
	
	user=ctx.message.author
	start= time.perf_counter()
	
	if site.startswith(('http://','https://','fullpage/http://','fullpage/https://')):
		pass
	else:
		site= "http://"+site
		
	
	base= 'https://image.thum.io/get/width/2400/'
	async with ctx.channel.typing():
		
		#check if site is valid
		is_img=False; err=False
		try:
			async with self.bot.session.get( site) as resp:
				if resp.status== 404: err=True
				if resp.content_type.startswith('image'): is_img=True
		except: err=True
		if err: raise NoResultsFound(site)
		
		#check if nsfw in non nsfw channel
		if not ctx.channel.is_nsfw():
			purify= 'https://www.picpurify.com/analyse.php'
			data= {'API_KEY': vars.picpurify_key,
				'url_image': site if is_img else base+site,
				'task'     : 'porn_detection,suggestive_nudity_detection'
				}
			async with self.bot.session.post(purify, data=data) as puresp:
				pjson= json.loads(await puresp.text())
				if pjson['porn_detection']['confidence_score']<0.73 or pjson['suggestive_nudity_detection']['confidence_score']<0.73:
					return await ctx.send('No way im sending that here. go do that in an NSFW channel.')
	


		async with self.bot.session.get( base+site) as resp:
			if not resp.status == 200: raise HTTPError(resp.status)
			io.BytesIO(await resp.read())
		async with self.bot.session.get( base+site) as resp:
			buffer = io.BytesIO(await resp.read())


		f= discord.File(buffer,  filename="file.png")
		m= await self.bot.get_channel(vars.dump_channel).send(file=f)
		
		
	e=discord.Embed(color=vars.Chrome[2])
	e.set_author(name='Chrome screenshot',icon_url=vars.Chrome[2])
	e.description= site
	e.set_image(url= m.attachments[0].url)
	
	end= time.perf_counter()
	diff=  '{:.2f}s'.format(end-start)
	#e.set_footer(text=f"{user} | {diff}", icon_url=user.avatar_url)
	
	await paginate(ctx, [e])
	await m.delete()

	
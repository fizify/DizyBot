import discord, io, random
from . import vars

snipes_channel=529577166028144651
dump_channel=529348038414696458
cmdlog_channel=531156616989376532


async def on_message(bot, message):
	#ctx=await bot.get_context(message)
	pass
	
	
async def on_message_edit(bot, before, after):
	ctx=await bot.get_context(after)
	"""Adds edited messages to snipestack"""
	
	if after.author.bot:return
	
	if after.author.id not in [ctx.me.id]:
		whs= await bot.get_channel(snipes_channel).webhooks()
		wh=whs[random.randint(0,len(whs)-1)]
		
		info_embed=discord.Embed(color=vars.YELLOW).set_author(name=after.guild.id, icon_url=after.guild.icon_url_as(format='png') or 'https://cdn.discordapp.com/attachments/475173554774605827/524590096091971584/20181218_194333_0001.png').set_footer(text=after.channel.id, icon_url='https://cdn.discordapp.com/attachments/475173554774605827/524592894158307338/1545143085433.png')
		
		attachments=before.attachments
		files=[]
		for i in range( len(attachments) ):
			async with bot.session.get(attachments[i].proxy_url) as resp:
				buffer=io.BytesIO(await resp.read())
				files.append(discord.File(buffer,  filename=attachments[i].filename) )
				
		res=f"""`WAS :`{before.content}
`IS  :`{after.content}
"""
		
		await wh.send(
			username= after.author.id,
			avatar_url= after.author.avatar_url_as(format='png'),
			content= res, 
			files= files,
			embed=info_embed
				)


async def on_message_delete(bot, message):
	ctx=await bot.get_context(message)
	"""Adds deleted messages to snipestack"""
	
	if message.author.bot:return
	
	if message.author.id not in [ctx.me.id]:
		whs= await bot.get_channel(snipes_channel).webhooks()
		wh=whs[random.randint(0,len(whs)-1)]
		
		info_embed=discord.Embed(color=vars.RED).set_author(name=message.guild.id, icon_url=message.guild.icon_url_as(format='png') or 'https://cdn.discordapp.com/attachments/475173554774605827/524590096091971584/20181218_194333_0001.png').set_footer(text=message.channel.id, icon_url='https://cdn.discordapp.com/attachments/475173554774605827/524592894158307338/1545143085433.png')
		embeds=[]
		try:
			msg_embed=message.embeds[0]
			embeds=[msg_embed,info_embed]
		except:embeds=[info_embed]
		
		attachments= message.attachments
		files=[]
		for i in range( len(attachments) ):
			async with bot.session.get(attachments[i].proxy_url) as resp:
				buffer=io.BytesIO(await resp.read())
				files.append(discord.File(buffer,  filename=attachments[i].filename) )
		
		res=message.content
		await wh.send(username= message.author.id,avatar_url= message.author.avatar_url,
			content= res, files= files,embeds= embeds)
	
	
async def on_command(bot, ctx):
	"""Resets cooldown for owner. and sends to #cmdlog"""
	if ctx.author.id==vars.dev_id:
		return ctx.command.reset_cooldown(ctx)
	else:
		try:
			bot.usage[ctx.command.name] += 1
		except:
			bot.usage[ctx.command.name] = 1
		
		whs= await bot.get_channel(cmdlog_channel).webhooks()
		webhook=whs[random.randint(0,len(whs)-1)]
		
		
		embed= discord.Embed().set_footer(icon_url=ctx.guild.icon_url, text=f'UserID : {ctx.author.id} \nGuildID : {ctx.guild.id}')
		await webhook.send(username=ctx.author.name, avatar_url=ctx.author.avatar_url, content=ctx.message.content, embed=embed)
		
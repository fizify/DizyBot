import discord, asyncio

async def paginate(ctx, pages):
	bot= ctx.bot
	
	def check_for_reaction(reaction,user):
		return user == ctx.message.author and reaction.message.id == say.id and reaction.emoji in reactables
		
	
	async def remove_this(reaction, user):
		try:await say.remove_reaction(reaction,user)
		except:pass
				

	pages=list(pages)
	at=0
	
	controls={
		'first': '⏪',
		'back': '◀',
		'stop': '⏹',
		'next': '▶',
		'last': '⏩'
			}
	if len(pages)==1:              reactables= [controls['stop']]
	elif len(pages) in range(2,6): reactables= list(controls.values())[1:-1]
	else:                          reactables= list(controls.values())
	
	
	
	if type(pages[0]) == discord.Embed:
		for page in pages:
			page.set_footer (text=f'Page {pages.index(page)+1} of {len(pages)}', icon_url=ctx.author.avatar_url)
			
	else:return 'Nope'
	
	say = await ctx.send(embed=pages[0])
	for reac in reactables:
		await say.add_reaction(reac)
	
	
	
	while(True):
		try:
			reaction, user = await bot.wait_for( 'reaction_add', timeout=60.0, check=check_for_reaction)
			await remove_this(reaction.emoji, user)
		
		except asyncio.TimeoutError:
			try: await say.clear_reactions()
			except:
				for reac in reversed(reactables):
					await remove_this(reac,ctx.me)
			return
		
		if str(reaction) == controls['first']:
			at=0
			
		if str(reaction) == controls['back']:
			if at==0: at =len(pages)-1
			else: at-=1
			
		if str(reaction) == controls['stop']:
			return await say.delete()
		
		if str(reaction) == controls['next']:
			if at==len(pages)-1:at =0
			else:at+=1
		
		if str(reaction) == controls['last']:
			at=len(pages)-1
		
		
		await say.edit(embed=pages[at])

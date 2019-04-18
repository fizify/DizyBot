import discord
from discord.ext import commands

from utils import *

from utils.paginator import paginate




@commands.command(aliases=['dictionary','dict','def','meaning'])
@commands.cooldown(1,7, commands.BucketType.user)
async def define(self, ctx, *,query):
	"""Fetches meanings from Oxford Dictionary"""
	
	embeds=[]
	
	base='https://od-api.oxforddictionaries.com/api/v1/search/en'
	base2='https://od-api.oxforddictionaries.com/api/v1/entries/en/'
	headers={'app_id':vars.oxford_id, 'app_key': vars.oxford_key }
	params={'q':query}
	
	async with ctx.channel.typing():
		async with self.bot.session.get(base, headers=headers, params=params) as r:
			a=await r.json()
		
		try:result= a['results'][0]
		except:raise NoResultsFound(query)
			
		link= 'https://en.oxforddictionaries.com/definition/'+result['id']
		defurl=base2+ result['id']
		async with self.bot.session.get(defurl, headers=headers) as resp:
			if not resp.status == 200 :raise HTTPError(resp.status)
			a=await resp.json()
		
		result= a['results'][0]
		word   = result['word'].capitalize()
		try:phonetic   = '/'+ result['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling'] + '/'
		except:phonetic= '/'+ word + '/'
		try:audio      = result['lexicalEntries'][0]['pronunciations'][0]['audioFile']
		except:audio   = ''
		
		
		embed=discord.Embed(color=vars.Dict[2])
		embed.set_author( name='Dictionary Search', icon_url= vars.Dict[1])
	
		embed.description=( f'**[{word}]({link})**' + '\n'+ f'{vars.Link} [Link]({link})'+'\n'+ f'[{phonetic}]({audio})' + f'[🔉]({audio})') 
		
		for lexentry in result['lexicalEntries']:
			category   = lexentry['lexicalCategory']
			
			defs_egs=''
			part_content=''
			for entry in lexentry['entries']:
				try:etymologies ='```•'+ '\n•'.join(entry['etymologies']) +'```'
				except: etymologies = ''
		
				counter= 1
				for sense in entry['senses']:
					
					definition= '**'+ f'{counter}. ' + sense['definitions'][0].capitalize() +'**'
					try:examples= '\t*"'+ '*\n\t*"'.join([eg['text'] for eg in sense['examples']]) +'"*'
					except: examples=''
					defs_egs+= definition + '\n'+ examples+'\n\n'
					counter+= 1
				part_content+= etymologies+ defs_egs+ '\n'
			
			
			embed.add_field(name=category ,value=part_content[:1020])
			
			
		embeds.append(embed)
	await paginate(ctx, embeds)

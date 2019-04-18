
from discord.ext import commands



def setup(bot):
	bot.add_cog(Apps(bot))



class Apps(commands.Cog):
	def __init__(self, bot):
		self.bot=bot
	
	"""Does this work? UPDATE:YES!"""
	
	from .Google      import google
	from .Google      import image
	from .Youtube     import youtube
	from .Maps        import _map
	from .Genius      import lyrics
	from .Dictionary  import define
	from .Urban       import urban
	from .Wolfram     import wolfram
	from .Screenshot  import screenshot
	
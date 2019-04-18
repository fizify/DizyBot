from discord.ext.commands import CommandError

class GammaBaseException(CommandError):
	"""Base class for main bot errors. 'Gammma'? because it sounds cool """

# APIs

class NoResultsFound(GammaBaseException):
	def __init__(self, query):
		super().__init__(f"Your query {query} returned zero results")

class HTTPError(GammaBaseException):
	def __init__(self, code):
		super().__init__(f"Execution failed with error code `{code}`")


# VOICE

class NoVoiceChannel(GammaBaseException):
	def __init__(self):
		super().__init__("You aren't in a voice channel!")
 
 
class MutualChannel(GammaBaseException):
	def __init__(self):
		super().__init__("You must be in my channel!")
 
 
class PlayerExists(GammaBaseException):
	def __init__(self):
		super().__init__("I already have a player running!")
 
 
class FullPlaylist(GammaBaseException):
	def __init__(self):
		super().__init__("The playlist is full!")
 
 
class NoPlayer(GammaBaseException):
	def __init__(self):
		super().__init__("There isn't a player running!")
 
 
class PlayerBusy(GammaBaseException):
	def __init__(self):
		super().__init__("You can't disconnect! There's music playing and you aren't the current DJ.")
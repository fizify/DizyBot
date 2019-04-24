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



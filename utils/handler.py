import traceback
import sys
from discord.ext import commands
import discord
import utils
from . import vars 

class CommandErrorHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
 

	async def on_command_error(self, ctx, error):

		if hasattr(ctx.command, 'on_error'):
			return

		error = getattr(error, 'original', error)
   
		if isinstance(error, utils.GammaBaseException) : # new errors not from discord.py
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"{error}.", icon_url=ctx.author.avatar_url) )
			
		
		if isinstance(error, commands.CommandNotFound):
			return

		elif isinstance(error, commands.BadArgument):
			ctx.command.reset_cooldown(ctx)
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"{error}.", icon_url=ctx.author.avatar_url) )

		elif isinstance(error, commands.MissingRequiredArgument):
			ctx.command.reset_cooldown(ctx)
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"{error}.", icon_url=ctx.author.avatar_url) )

		elif isinstance(error, commands.NoPrivateMessage):
			return

		elif isinstance(error, commands.CheckFailure):
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"This command is for other users. You can't use it.", icon_url=ctx.author.avatar_url) )

		elif isinstance(error, commands.DisabledCommand):
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"{ctx.command} is disabled.", icon_url=ctx.author.avatar_url) )

		elif isinstance(error, commands.TooManyArguments):
			ctx.command.reset_cooldown(ctx)
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"You gave too many arguments.", icon_url=ctx.author.avatar_url) )

		elif isinstance(error, commands.UserInputError):
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"You did something wrong?", icon_url=ctx.author.avatar_url) )

		elif isinstance(error, commands.CommandOnCooldown):
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f'{str(ctx.command).capitalize()} on Cooldown. Try in {round(error.retry_after ,1)}s', icon_url=ctx.author.avatar_url) )

		elif isinstance(error, commands.NotOwner):
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"You do not own this bot.", icon_url=ctx.author.avatar_url) )

		elif isinstance(error, commands.MissingPermissions):
			ctx.command.reset_cooldown(ctx)
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"{error}.", icon_url=ctx.author.avatar_url) )

		elif isinstance(error, commands.BotMissingPermissions):
			ctx.command.reset_cooldown(ctx)
			return await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"{error}.", icon_url=ctx.author.avatar_url) )

		await ctx.send(embed=discord.Embed(color=vars.RED).set_footer(text=f"Something went very wrong. Please try again later.", icon_url=ctx.author.avatar_url) )

		err= traceback.format_exception(type(error), error, error.__traceback__)
		errstring= '\n'.join(err)

		if ctx.author.id==vars.dev_id:
			return await ctx.send(embed= discord.Embed(color=vars.RED, description=f"```{errstring[:2000]}```") )
	
		err_webhook= (await (self.bot.get_channel(529348093448290304)).webhooks())[0]
		return await err_webhook.send(username=str(ctx.author) , avatar_url=ctx.author.avatar_url, content=ctx.message.content, embeds= [discord.Embed(color=vars.RED, description=f"```{errstring}```"), discord.Embed().set_footer(icon_url=ctx.guild.icon_url, text=f'UserID:{ctx.author.id}\nGuildID:{ctx.guild.id}')])

def setup(bot):
	print('Error handler loaded.')
	bot.add_cog(CommandErrorHandler(bot))
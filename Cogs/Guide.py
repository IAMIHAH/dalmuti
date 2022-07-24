from disnake.ext import commands
import disnake
from Module.Embed import makeErrorEmbed

from Module.Guide import *
from Module.User import getUser

class Guide(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.slash_command(
		name="가이드",
		description="봇 가이드를 살펴봅니다."
	)
	async def guide(i: disnake.CommandInteraction):
		if getUser(i.user.id):
			if i.channel.type != disnake.ChannelType.public_thread and i.channel.type != disnake.ChannelType.private_thread:
				await i.response.send_message(embed=GuideEmbed[0], view=Guide_Controller(), ephemeral=True)
			else:
				await i.response.send_message(embed=makeErrorEmbed("스레드에서 로비창을 띄울 수 없어요."), ephemeral=True)
		else:
			await i.response.send_message(embed=makeErrorEmbed("`/가입`을 먼저 진행해주세요!"), ephemeral=True)

def setup(bot):
	bot.add_cog(Guide(bot))
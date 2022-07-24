from disnake.ext import commands
import disnake
from Module.Embed import makeErrorEmbed
from Module.Lobby import *
from Module.User import getUser

class Lobby(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.slash_command(
		name="달무티",
		description="달무티를 시작합니다."
	)
	async def game(self, i: disnake.CommandInteraction):
		if getUser(i.user.id):
			if i.channel.type != disnake.ChannelType.public_thread and i.channel.type != disnake.ChannelType.private_thread:
				embed = disnake.Embed(
					title="달무티 시작하기",
					description="📖 처음이신가요? `/가이드`를 확인해보세요."
				)
				await i.response.send_message(embed=embed, view=Lobby_Controller(i.channel.type == disnake.ChannelType.private), ephemeral=True)
			else:
				await i.response.send_message(embed=makeErrorEmbed("스레드에서 로비창을 띄울 수 없어요!"), ephemeral=True)
		else:
			await i.response.send_message(embed=makeErrorEmbed("`/가입`을 먼저 진행해주세요!"), ephemeral=True)

def setup(bot):
	bot.add_cog(Lobby(bot))
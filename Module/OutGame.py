import asyncio
import sqlite3
import disnake
from disnake.ext import commands
from Module.Embed import makeErrorEmbed
from Module.InGame import InGame_Start
from Module.User import getUser

async def OutGame_GetUserList(channel: str):
	user = sqlite3.connect("GameChannel.db", isolation_level=None)
	u = user.cursor()
	u.execute(f"SELECT admin FROM Game WHERE channel='{channel}'")
	admin = u.fetchone()[0]
	user = sqlite3.connect("User.db", isolation_level=None)
	u = user.cursor()
	u.execute(f"SELECT id FROM User WHERE channel='{channel}'")
	users = []
	for x in u.fetchall():
		if x[0] != admin:
			users.append(f"{x[0]}")
	return users

async def OutGame_RefreshInfoMsg(channel: str):
	game = sqlite3.connect("GameChannel.db", isolation_level=None)
	g = game.cursor()
	g.execute(f"SELECT user,u_limit,type,admin FROM Game WHERE channel='{channel}'")
	user, lm, gameChannelType, admin = g.fetchone()
	userList = await OutGame_GetUserList(channel)
	embed = disnake.Embed(
		title="🎮 새로운 게임이 생성되었어요.",
		description=f"채널 타입: `공개`\n채널 코드: `{channel}`" if gameChannelType == 1 else f"채널 타입: `비공개`"
	)
	users = '<@!' + '>\n<@!'.join(userList) + '>' if len(userList) > 0 else ''
	embed.add_field(name="참여 인원", value=f"{user} / {lm} 명\n\n__[방장]__ <@!{admin}>\n{users}", inline=False)
	return embed

class OutGame_ChannelSetting(disnake.ui.Modal):
	def __init__(self, channel: str):
		components = [
			disnake.ui.TextInput(
				placeholder="4 ~ 8",
				label="최대 인원",
				custom_id="players",
				style=disnake.TextInputStyle.short,
				required=True,
				max_length=1
			)
		]
		super().__init__(
			title=f"{channel} 채널 설정",
			components=components,
			custom_id=channel
		)
	
	async def callback(self, i: disnake.ModalInteraction):
		players = int(i.text_values['players'])
		if players > 8 and players < 4:
			await i.response.send_message(embed=makeErrorEmbed("인원은 4~8명까지 설정 가능해요."), ephemeral=True)
			return
		game = sqlite3.connect("GameChannel.db", isolation_level=None)
		g = game.cursor()
		g.execute(f"SELECT user FROM Game WHERE channel='{i.custom_id}'")
		user = g.fetchone()[0]
		if user > players:
			await i.response.send_message(embed=makeErrorEmbed("현재 인원보다 최대 인원을 적게 설정할 수 없어요."), ephemeral=True)
			return
		g.execute(f"UPDATE Game SET u_limit={players} WHERE channel='{i.custom_id}'")
		await i.response.send_message("인원 설정 완료!", ephemeral=True)
		g.execute(f"SELECT info FROM Game WHERE channel='{i.custom_id}'")
		info = g.fetchone()[0]
		infomsg = await i.channel.parent.fetch_message(info)
		await infomsg.edit(embed=await OutGame_RefreshInfoMsg(i.custom_id))

class OutGame_btnJoinExit(disnake.ui.Button['OutGame_Controller']):
	def __init__(self, channel: str, bot):
		self._channel = channel
		self.bot: commands.Bot = bot
		super().__init__(label="입·퇴장", style=disnake.ButtonStyle.red, row=1)

	async def callback(self, i: disnake.Interaction):
		if getUser(i.user.id):
			await i.response.defer(with_message=True, ephemeral=True)
			conn = sqlite3.connect("User.db", isolation_level=None)
			c = conn.cursor()
			c.execute(f"SELECT channel FROM User WHERE id={i.user.id}")
			n = c.fetchone()
			game = sqlite3.connect("GameChannel.db", isolation_level=None)
			g = game.cursor()
			g.execute(f"SELECT info,user,u_limit,admin FROM Game WHERE channel='{self._channel}'")
			infoNew, user, lm, admin = g.fetchone()
			if user >= lm:
				await i.edit_original_message(embed=makeErrorEmbed("인원이 꽉 찼어요."))
				return
			if n:
				if n[0] == self._channel:
					if admin == i.user.id: # TODO 방장이 퇴장하는 경우 (일단 못나감)
						await i.edit_original_message(embed=makeErrorEmbed("방장은 방에서 퇴장할 수 없어요."))
						return
					c.execute(f"UPDATE User SET channel=null WHERE id={i.user.id}")
					await i.channel.remove_user(i.user)
					g.execute(f"UPDATE Game SET user=user-1 WHERE channel='{self._channel}'")
					infomsgNew = await i.channel.parent.fetch_message(infoNew)
					await infomsgNew.edit(embed=await OutGame_RefreshInfoMsg(self._channel))
					await i.edit_original_message(embed=disnake.Embed(title="✅ 퇴장 완료!", description="퇴장을 완료했어요."))
					return
				elif n[0]:
					g.execute(f"SELECT thread,info FROM Game WHERE channel='{n[0]}'")
					try:
						thid, info = g.fetchone()
						th : disnake.Thread = await i.guild.fetch_channel(thid)
						try:
							await th.remove_user(i.user)
						except disnake.errors.HTTPException as e:
							if "Thread is archived" in e:
								pass
						#infomsgNew = self.bot.get_message(info)
						infomsg = await i.channel.parent.fetch_message(info)
						await infomsg.edit(embed=await OutGame_RefreshInfoMsg(n[0]))
						#infomsg = await i.user.fetch_message(g.fetchone()[1])
						#await infomsg.edit(embed=await OutGame_RefreshInfoMsg(n[0]))
						# TODO 이전 채널이 다른 서버인 경우 처리
						g.execute(f"UPDATE Game SET user=user-1 WHERE channel='{n[0]}'")
					except disnake.errors.NotFound:
						g.execute(f"DELETE FROM Game WHERE channel='{n[0]}'")
						c.execute(f"UPDATE User SET channel=null WHERE channel='{n[0]}'")
					except TypeError:
						c.execute(f"UPDATE User SET channel=null WHERE channel='{n[0]}'")
			g.execute(f"UPDATE Game SET user=user+1 WHERE channel='{self._channel}'")
			await i.channel.add_user(i.user)
			c.execute(f"UPDATE User SET channel='{self._channel}' WHERE id={i.user.id}")
			infomsgNew = await i.channel.parent.fetch_message(infoNew)
			await infomsgNew.edit(embed=await OutGame_RefreshInfoMsg(self._channel))
			await i.edit_original_message(embed=disnake.Embed(title="✅ 입장 완료!", description="입장을 완료했어요."))
		else:
			await i.response.send_message(embed=makeErrorEmbed("`/가입`을 먼저 진행해주세요!"), ephemeral=True)

async def OutGame_NoSleep(channel: str, bot: commands.Bot):
	game = sqlite3.connect("GameChannel.db", isolation_level=None)
	g = game.cursor()
	g.execute(f"SELECT thread,controller FROM Game WHERE channel='{channel}'")
	try:
		ingame = sqlite3.connect("InGame.db", isolation_level=None)
		ig = ingame.cursor()
		ig.execute(f"SELECT channel FROM InGame WHERE channel='{channel}'")
		if not ig.fetchone():
			thid,controller = g.fetchone()
			th : disnake.Thread = await bot.fetch_channel(thid)
			con = bot.get_message(controller)
			await con.delete()
			await th.send("**게임이 시작되지 않고 180초가 지나 채널이 자동으로 삭제되었어요.**\n채널을 새로 생성해주세요.")
			await th.edit(archived=True, locked=True)
			g.execute(f"DELETE FROM Game WHERE channel='{channel}'")
			conn = sqlite3.connect("User.db", isolation_level=None)
			c = conn.cursor()
			c.execute(f"UPDATE User SET channel=null WHERE channel='{channel}'")
	except:
		pass

class OutGame_Controller(disnake.ui.View):
	def __init__(self, channel: str, bot):
		super().__init__(timeout=None)
		self._channel = channel
		self.add_item(OutGame_btnJoinExit(channel, bot))

	@disnake.ui.button(label="채널 설정", style=disnake.ButtonStyle.green, row=2)
	async def btnChannelEdit(self, btn: disnake.Button, i: disnake.Interaction):
		conn = sqlite3.connect("GameChannel.db", isolation_level=None)
		c = conn.cursor()
		c.execute(f"SELECT admin FROM Game WHERE channel='{self._channel}'")
		if c.fetchone()[0] == i.user.id:
			await i.response.send_modal(OutGame_ChannelSetting(self._channel))
		else:
			await i.response.send_message(embed=makeErrorEmbed("권한이 없어요."), ephemeral=True)

	@disnake.ui.button(label="게임 시작", style=disnake.ButtonStyle.blurple, row=2)
	async def btnGameStart(self, btn: disnake.Button, i: disnake.Interaction):
		game = sqlite3.connect("GameChannel.db", isolation_level=None)
		g = game.cursor()
		g.execute(f"SELECT user,admin FROM Game WHERE channel='{self._channel}'")
		user, admin = g.fetchone()
		if admin == i.user.id:
			if user < 4:
				await i.response.send_message(embed=makeErrorEmbed("인원이 부족해요.\n최소 시작 인원: 4명"), ephemeral=True)
				return
			else:
				await i.response.send_message("게임을 시작할게요!", ephemeral=True)
				await InGame_Start(self._channel, i.channel)
				self.stop()
		else:
			await i.response.send_message(embed=makeErrorEmbed("권한이 없어요."), ephemeral=True)

	@disnake.ui.button(label="채널 삭제", style=disnake.ButtonStyle.red, row=2)
	async def btnRemoveChannel(self, btn: disnake.Button, i: disnake.Interaction):
		conn = sqlite3.connect("GameChannel.db", isolation_level=None)
		c = conn.cursor()
		c.execute(f"SELECT admin FROM Game WHERE channel='{self._channel}'")
		if c.fetchone()[0] == i.user.id:
			user = sqlite3.connect("User.db", isolation_level=None)
			u = user.cursor()
			u.execute(f"UPDATE User SET channel=null WHERE channel='{self._channel}'")
			c.execute(f"DELETE FROM Game WHERE channel='{self._channel}'")
			await i.response.send_message("달무티 채널을 삭제했어요.\n\n서버 관리자 외에 접근이 불가능하고\n서버 관리자가 삭제하지 않는 한 기록을 볼 수 있어요.")
			await i.channel.edit(archived=True, locked=True)
			self.stop()
		else:
			await i.response.send_message(embed=makeErrorEmbed("권한이 없어요."), ephemeral=True)
	
	@disnake.ui.button(label="새 메시지 보내기", style=disnake.ButtonStyle.gray, row=3)
	async def btnNewMsg(self, btn: disnake.Button, i: disnake.Interaction):
		conn = sqlite3.connect("GameChannel.db", isolation_level=None)
		c = conn.cursor()
		c.execute(f"SELECT admin,controller FROM Game WHERE channel='{self._channel}'")
		n = c.fetchone()
		if n[0] == i.user.id:
			msg = await i.channel.send(view=OutGame_Controller(self._channel))
			c.execute(f"UPDATE Game SET controller={msg.id} WHERE channel='{self._channel}'")
			msg = await i.channel.fetch_message(n[1])
			await msg.delete()
			await i.response.send_message("갱신 완료!", ephemeral=True)
			self.stop()
		else:
			await i.response.send_message(embed=makeErrorEmbed("권한이 없어요."), ephemeral=True)
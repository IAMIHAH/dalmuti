import sqlite3, disnake, random, string
from tkinter import TRUE
from Module.InGame import OutGame_Controller

class Lobby_MakeBtn(disnake.ui.Button['Lobby_Controller']):
	def __init__(self, btn, public):
		if btn:
			label = "공개 게임 생성하기"
		else:
			label = "비공개 게임 생성하기"
		self._public = btn
		super().__init__(label=label, disabled=not public, style=disnake.ButtonStyle.blurple)

	async def callback(self, i: disnake.Interaction):
		if self._public:
			pass # TODO 공개 서버 생성
		else:
			if i.guild.premium_tier >= 2:
				embed = disnake.Embed(
					title="<:thread:949580585398046740> 스레드 공개 여부 설정",
					description="이 서버는 스레드 공개 여부를 설정할 수 있어요.\n스레드를 공개할까요?\n\n스레드를 공개한다면 서버원의 참여가 쉬워져요.\n다만, 정해진 사람들끼리 하고 싶다면 공개하지 않는 것을 추천드려요!"
				)
				await i.response.send_message(embed=embed, view=Lobby_MakeBtn_Premium(), ephemeral=True)
				return
			else:
				th = await Lobby_MakeNewThread(i.user, i.channel, True)
				await i.response.send_message(f"생성이 완료되었습니다!\n{th.mention}", ephemeral=True)

async def Lobby_MakeNewThread(user: disnake.Member, channel: disnake.TextChannel, public: bool):
	channelId = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
	embed = disnake.Embed(
		title="🎮 새로운 게임이 생성되었어요.",
		description=f"채널 타입: `공개`\n채널 코드: `{channelId}`" if public else f"채널 타입: `비공개`"
	)
	embed.add_field(name="참여 인원", value=f"1 / 8 명\n\n[방장] {user.mention}", inline=False)
	msg = await channel.send(
		embed=embed
	)
	if public:
		th = await msg.create_thread(
			name=f"채널 {channelId}",
			auto_archive_duration=disnake.ThreadArchiveDuration.hour
		)
	else:
		th = await channel.create_thread(
			name=f"채널 {channelId}",
			type=disnake.ChannelType.private_thread,
			invitable=False
		)
	conn = sqlite3.connect("User.db", isolation_level=None)
	c = conn.cursor()
	c.execute(f"UPDATE User SET channel='{channelId}' WHERE id={user.id}")
	conn.close()
	controller = await th.send(view=OutGame_Controller(channelId))
	conn = sqlite3.connect("GameChannel.db", isolation_level=None)
	c = conn.cursor()
	gameChannelType = 1 if public else 2
	c.execute(f"INSERT INTO Game VALUES('{channelId}', {gameChannelType}, {user.id}, {msg.id}, {th.id}, 1, 8, {controller.id})")
	conn.close()
	await th.add_user(user)
	return th

class Lobby_MakeBtn_Premium(disnake.ui.View):
	def __init__(self):
		super().__init__()
	
	@disnake.ui.button(label="공개", style=disnake.ButtonStyle.green)
	async def btnPublic(self, btn: disnake.Button, i: disnake.Interaction):
		await Lobby_MakeNewThread(i.user, i.channel, True)
	
	@disnake.ui.button(label="비공개", style=disnake.ButtonStyle.red)
	async def btnPrivate(self, btn: disnake.Button, i: disnake.Interaction):
		await Lobby_MakeNewThread(i.user, i.channel, False)

class Lobby_JoinChannel_Private(disnake.ui.Modal):
	def __init__(self):
		components = [
			disnake.ui.TextInput(
				label="채널 코드",
				custom_id="channel",
				style=disnake.TextInputStyle.short,
				placeholder="XXXXXX",
				required=True,
				min_length=6,
				max_length=6
			)
		]
		super().__init__(
			title="비공개 게임 입장하기",
			components=components,
			custom_id="private_join"
		)
	
	async def callback(self, i: disnake.ModalInteraction):
		channel = i.text_values['channel']

class Lobby_JoinBtn(disnake.ui.Button['Lobby_Controller']):
	def __init__(self, btn, public):
		if btn:
			label = "공개 게임 입장하기"
		else:
			label = "비공개 게임 입장하기"
		self._public = btn
		super().__init__(label=label, disabled=not public, style=disnake.ButtonStyle.green, row=2)

	async def callback(self, i: disnake.Interaction):
		pass # TODO 입장하기

class Lobby_Controller(disnake.ui.View):
	def __init__(self, dm: bool = False):
		super().__init__(timeout=None)
		if dm:
			self.add_item(Lobby_MakeBtn(True, True))
			self.add_item(Lobby_MakeBtn(False, False))
			self.add_item(Lobby_JoinBtn(True, True))
			self.add_item(Lobby_JoinBtn(False, False))
		else:
			self.add_item(Lobby_MakeBtn(True, False))
			self.add_item(Lobby_MakeBtn(False, True))
			self.add_item(Lobby_JoinBtn(True, False))
			self.add_item(Lobby_JoinBtn(False, True))
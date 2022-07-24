import random
import sqlite3, disnake
from disnake.ext import commands
from Module.Embed import makeErrorEmbed
from pyjosa.josa import Josa

async def InGame_GetUserList(channel: str) -> list:
	user = sqlite3.connect("User.db", isolation_level=None)
	u = user.cursor()
	u.execute(f"SELECT id FROM User WHERE channel='{channel}'")
	users = []
	for x in u.fetchall():
		users.append(f"{x[0]}")
	return users

async def InGame_GetUserLen(channel: str) -> int:
	user = sqlite3.connect("GameChannel.db", isolation_level=None)
	u = user.cursor()
	u.execute(f"SELECT user FROM Game WHERE channel='{channel}'")
	user = u.fetchone()[0]
	return user

async def InGame_Start(channel: str, ch: disnake.Thread):
	msg = await ch.send("게임을 초기화하고 있어요.\n잠시만 기다려주세요!")
	users = await InGame_GetUserList(channel)
	embed = disnake.Embed(
		title=f"👑 조공을 진행해주세요!",
		color=0x59bfff
	)
	cards = []
	for x in range(1, 13): # 카드 초기화
		for a in range(x):
			cards.append(x)
	cards.append(13)
	cards.append(13)

	user_card = {}
	for x in users: # 순서 지정
		user_card[f'{x}'] = cards.pop(random.randint(0, len(cards)-1))
		for a in user_card:
			if int(x) != int(a):
				while user_card[a] == user_card[f'{x}']:
					cards.append(user_card[f'{x}'])
					user_card[f'{x}'] = cards.pop(random.randint(0, len(cards)-1))
	user_card = dict(sorted(user_card.items(), key = lambda item: item[1]))
	cardUser = list(user_card.keys())
	embedCard = disnake.Embed(
		title="👑 순서 정하기 결과",
		color=0xffda00
	)
	for x in user_card:
		u = await ch.guild.fetch_member(x)
		embedCard.add_field(name=f"{u.name}", value=f"{user_card[f'{x}']}")
	await ch.send(embed=embedCard)

	conn = sqlite3.connect("InGame.db", isolation_level=None)
	c = conn.cursor()
	c.execute(f"INSERT INTO InGame(channel, msg) VALUES('{channel}', {msg.id})")
	for x in range(0, len(cardUser)):
		c.execute(f"UPDATE InGame SET user{x+1}={cardUser[x]} WHERE channel='{channel}'")
	
	card_len = 80-len(user_card)
	giveCard = card_len/len(user_card)
	for x in users: # 카드 배분
		c.execute(f"INSERT INTO InGameCard(channel, user) VALUES('{channel}', {x})")
		c.execute(f"UPDATE InGameCard SET card{user_card[f'{x}']}=card{user_card[f'{x}']}+1,cards=cards+1 WHERE channel='{channel}' AND user={x}")
		for a in range(int(giveCard)):
			ca = cards.pop(random.randint(0, len(cards)-1))
			c.execute(f"UPDATE InGameCard SET card{ca}=card{ca}+1,cards=cards+1 WHERE channel='{channel}' AND user={x}")
	for x in user_card:
		if len(cards) > 0: # 카드가 남으면
			ca = cards.pop(random.randint(0, len(cards)-1))
			c.execute(f"UPDATE InGameCard SET card{ca}=card{ca}+1,cards=cards+1 WHERE channel='{channel}' AND user={x}")
		u = await ch.guild.fetch_member(int(x))
		c.execute(f"SELECT cards FROM InGameCard WHERE channel='{channel}' AND user={x}")
		embed.add_field(name=f"{u.name}", value=f"카드 ×{c.fetchone()[0]}")
	await msg.delete()
	msg = await ch.send(embed=embed, view=InGame_Controller(channel))
	c.execute(f"UPDATE InGame SET msg={msg.id},now=-1 WHERE channel='{channel}'")

class InGame_MyCardSelect(disnake.ui.Select):
	def __init__(self, options: list[disnake.SelectOption], selectOption: str=None, placeholder: str="내 카드 목록", options2=None):
		super().__init__(placeholder=placeholder, options=options)
		self._option = selectOption if selectOption else "None/None"
		self._select = options
		self._select2 = options2
	
	async def callback(self, i: disnake.Interaction):
		options = self._option.split("/")
		channel = options[0]
		if channel != "None":
			task = options[1]
			if task == "jogong":
				me = options[2]
				you = options[3]
				meCard = [options[4], options[5]]
				youCard = ["", ""]
				if len(options) > 6:
					youCard = [options[6], ""]
				if len(options) > 7:
					youCard = [options[6], options[7]]
				conn = sqlite3.connect("InGame.db", isolation_level=None)
				c = conn.cursor()
				c.execute(f"SELECT user{you} FROM InGame WHERE channel='{channel}'")
				youMention = c.fetchone()[0]
				option = [channel, task, me, you, meCard[0], meCard[1]]
				card = int(self.values[0])
				c.execute(f"SELECT card{card} FROM InGameCard WHERE channel='{channel}' AND user={i.user.id}")
				for x in youCard:
					if x != "":
						xCard = cardEmoji.index(x.split(" ")[0])+1
						c.execute(f"SELECT card{xCard} FROM InGameCard WHERE channel='{channel}' AND user={i.user.id}")
						xcard = c.fetchone()[0]
						if xCard == card:
							if xcard == 1:
								await i.response.send_message(embed=makeErrorEmbed(f"[{cardEmoji[card-1]} {cardName[card-1]}] 카드를 더 이상 넣을 수 없어요."), ephemeral=True)
								return
				if "첫 번째 카드" in self.placeholder:
					self._select2 = self._select.copy() if not self._select2 else self._select2
					youCard[0] = f"{cardEmoji[card-1]} {cardName[card-1]}"
					option.append(youCard[0])
					if youCard[1] != "":
						option.append(youCard[1])
				elif "두 번째 카드" in self.placeholder:
					youCard[1] = f"{cardEmoji[card-1]} {cardName[card-1]}"
					option.append(youCard[0])
					option.append(youCard[1])
				embed = disnake.Embed(
					title="조공 타임!",
					description=f"<@!{youMention}>님에게 **지급할 카드** __2장__을 선택해주세요.\n\n보낼 카드\n> {youCard[0]}\n> {youCard[1]}\n\n받을 카드\n> {meCard[0]}\n> {meCard[1]}"
				)
				if meCard[1] == ".":
					embed.description = f"<@!{youMention}>님에게 **지급할 카드** __1장__을 선택해주세요.\n\n보낼 카드\n> {youCard[0]}\n\n받을 카드\n> {meCard[0]}"
				await i.response.edit_message(embed=embed, view=InGame_MyCardView(self._select, '/'.join(option), self._select2))
			if task == "game":
				me = options[2]
				joker = options[4]
				card, cardLen = self.values[0].split("/")
				embed = disnake.Embed(
					title="카드 개수 정하기",
					description=f"정말 [{cardEmoji[int(card)-1]} {cardName[int(card)-1]}] {cardLen}장을 내시겠어요?"
				)
				await i.response.edit_message(embed=embed, view=InGame_CardLenView(channel, me, int(card), int(cardLen), self._select, self._option))

class InGame_JoGongCheck(disnake.ui.Button):
	def __init__(self, user1, user2, meCard, youCard):
		super().__init__(
			style=disnake.ButtonStyle.blurple,
			label="카드 확인"
		)
		self._user1 = user1
		self._user2 = user2
		self._meCard = meCard
		self._youCard = youCard
	
	async def callback(self, i: disnake.Interaction):
		if i.user.id == self._user1 or i.user.id == self._user2:
			embed = disnake.Embed(
				title="👀 조공된 카드 확인",
				description=f"<@!{self._user2}>님이 받은 카드\n> {self._youCard[0]}\n> {self._youCard[1]}\n\n<@!{self._user1}>님이 받은 카드\n> {self._meCard[0]}\n> {self._meCard[1]}" if self._youCard[1] != "." else f"<@!{self._user2}>님이 받은 카드\n> {self._youCard[0]}\n\n<@!{self._user1}>님이 받은 카드\n> {self._meCard[0]}"
			)
			await i.response.send_message(embed=embed, ephemeral=True)
		else:
			await i.response.send_message(embed=makeErrorEmbed("권한이 없어요."), ephemeral=True)

class InGame_JoGongView(disnake.ui.View):
	def __init__(self, user1, user2, meCard, youCard):
		super().__init__(timeout=None)
		self.add_item(InGame_JoGongCheck(user1, user2, meCard, youCard))

class InGame_JoGong(disnake.ui.Button):
	def __init__(self, selectOption: str):
		super().__init__(
			style=disnake.ButtonStyle.green,
			label="결정하기",
			row=3
		)
		self._option = selectOption
	
	async def callback(self, i: disnake.Interaction):
		options = self._option.split("/")
		conn = sqlite3.connect("InGame.db", isolation_level=None)
		c = conn.cursor()
		channel = options[0]
		you = options[3]
		c.execute(f"SELECT user{you} FROM InGame WHERE channel='{channel}'")
		youId = c.fetchone()[0]
		meCard = [options[4], options[5]]
		youCard = [options[6], "."]
		if len(options) > 7:
			youCard = [options[6], options[7]]
		for x in meCard:
			if x != ".":
				card = cardEmoji.index(x.split(' ')[0])+1
				c.execute(f"UPDATE InGameCard SET card{card}=card{card}-1 WHERE channel='{channel}' AND user='{youId}'")
				c.execute(f"UPDATE InGameCard SET card{card}=card{card}+1 WHERE channel='{channel}' AND user='{i.user.id}'")
		for x in youCard:
			if x != ".":
				card = cardEmoji.index(x.split(' ')[0])+1
				c.execute(f"UPDATE InGameCard SET card{card}=card{card}+1 WHERE channel='{channel}' AND user='{youId}'")
				c.execute(f"UPDATE InGameCard SET card{card}=card{card}-1 WHERE channel='{channel}' AND user='{i.user.id}'")
		embed = disnake.Embed(
			title="✅ 조공 완료!",
			description=f"조공을 완료했어요.\n\n보낸 카드\n> {youCard[0]}\n> {youCard[1]}\n\n받은 카드\n> {meCard[0]}\n> {meCard[1]}" if youCard[1] != "." else f"조공을 완료했어요.\n\n보낸 카드\n> {youCard[0]}\n\n받은 카드\n> {meCard[0]}"
		)
		await i.response.edit_message(embed=embed, view=None)
		embed = disnake.Embed(
			title="✅ 조공 완료!",
			description=f"<@!{i.user.id}> 님과 <@!{youId}> 님의 카드 교환이 완료되었어요."
		)
		c.execute(f"UPDATE InGame SET now=now-1 WHERE channel='{channel}'")
		await i.channel.send(embed=embed, view=InGame_JoGongView(i.user.id, youId, meCard, youCard))
		c.execute(f"SELECT now FROM InGame WHERE channel='{channel}'")
		now = c.fetchone()[0]
		if now < -2:
			c.execute(f"UPDATE InGame SET now=1,last=1 WHERE channel='{channel}'")
			await InGame_Go(channel, i.channel)

async def InGame_Go(channel: str, ch: disnake.Thread, embed2=None):
	conn = sqlite3.connect("InGame.db", isolation_level=None)
	c = conn.cursor()
	c.execute(f"SELECT now,msg FROM InGame WHERE channel='{channel}'")
	now, mid = c.fetchone()
	msg = await ch.fetch_message(mid)
	await msg.edit(content="<a:Loading:898561786540875887> 게임을 진행중이에요.\n잠시만 기다려주세요!", embed=None, view=None)
	c.execute(f"SELECT user{now} FROM InGame WHERE channel='{channel}'")
	x = c.fetchone()[0]
	u = await ch.guild.fetch_member(int(x))
	c.execute(f"SELECT cards FROM InGameCard WHERE channel='{channel}' AND user={x}")
	embed = disnake.Embed(
		title=f"👤 {u.name}님의 차례에요!",
		color=0x59bfff
	)
	for n in range(await InGame_GetUserLen(channel)):
		c.execute(f"SELECT user{n+1} FROM InGame WHERE channel='{channel}'")
		user = c.fetchone()[0]
		u = await ch.guild.fetch_member(int(user))
		c.execute(f"SELECT cards FROM InGameCard WHERE channel='{channel}' AND user={user}")
		embed.add_field(name=f"{u.name}", value=f"카드 ×{c.fetchone()[0]}")
	await msg.delete()
	if embed2:
		await ch.send(embed=embed2)
	msg = await ch.send(content=f"{u.mention}", embed=embed, view=InGame_Controller(channel))
	c.execute(f"UPDATE InGame SET msg={msg.id} WHERE channel='{channel}'")

class InGame_MyCardView(disnake.ui.View):
	def __init__(self, options: list[disnake.SelectOption], selectOption: str=None, options2=None):
		super().__init__(timeout=None)
		if not selectOption:
			self.add_item(InGame_MyCardSelect(options))
		else:
			option = selectOption.split("/")[1]
			if option == 'jogong':
				if len(selectOption.split("/")) == 6:
					self.add_item(InGame_MyCardSelect(options, selectOption, "첫 번째 카드 선택", options2))
				if len(selectOption.split("/")) == 7:
					self.add_item(InGame_MyCardSelect(options, selectOption, "첫 번째 카드 수정", options2))
					if int(selectOption.split("/")[2]) == 1:
						self.add_item(InGame_MyCardSelect(options2, selectOption, "두 번째 카드 선택", options2))
					else:
						self.add_item(InGame_JoGong(selectOption))
				if len(selectOption.split("/")) == 8:
					self.add_item(InGame_MyCardSelect(options, selectOption, "첫 번째 카드 수정", options2))
					if int(selectOption.split("/")[2]) == 1:
						self.add_item(InGame_MyCardSelect(options2, selectOption, "두 번째 카드 수정", options2))
					self.add_item(InGame_JoGong(selectOption))
			if option == 'game':
				if len(options) > 0:
					self.add_item(InGame_MyCardSelect(options, selectOption, "카드 선택"))
				conn = sqlite3.connect("InGame.db", isolation_level=None)
				c = conn.cursor()
				c.execute(f"SELECT now,last FROM InGame WHERE channel='{selectOption.split('/')[0]}'")
				now, last = c.fetchone()
				if now != last:
					self.add_item(InGame_CardLenBtnPass(selectOption.split("/")[0], selectOption.split("/")[2]))

class InGame_CardLenBtnMinMax(disnake.ui.Button):
	def __init__(self, channel, now, card, cardLen, mode, max, options, selectOption):
		super().__init__(
			style=disnake.ButtonStyle.gray,
			label="1" if mode == 1 else "최대",
			disabled=True if (cardLen == 1 and mode == 1) or (cardLen == max and mode != 1) else False
		)
		self._channel = channel
		self._now = now
		self._card = card
		self._max = max
		self._select = options
		self._option = selectOption
	
	async def callback(self, i: disnake.Interaction):
		joker = 0
		if self.label == "최대":
			conn = sqlite3.connect("InGame.db", isolation_level=None)
			c = conn.cursor()
			if not self._max:
				c.execute(f"SELECT card{self._card} FROM InGameCard WHERE channel='{self._channel}' AND user={i.user.id}")
				self._max = c.fetchone()[0]
			c.execute(f"SELECT card13 FROM InGameCard WHERE channel='{self._channel}' AND user={i.user.id}")
			joker = c.fetchone()[0]
			cardLen = self._max
		else:
			cardLen = 1
			joker = 0
		cardLenP = cardLen
		if joker > 0:
			cardLenP = f"{cardLen}(`{cardLen}`+★`{joker}`)"
			cardLen += joker
		embed = disnake.Embed(
			title="카드 개수 정하기",
			description=f"정말 [{cardEmoji[self._card-1]} {cardName[self._card-1]}] {cardLenP}장을 내시겠어요?"
		)
		await i.response.edit_message(embed=embed, view=InGame_CardLenView(self._channel, self._now, self._card, cardLen, self._select, self._option, self._max))

class InGame_CardLenBtnPlMa(disnake.ui.Button):
	def __init__(self, channel, now, card, cardLen, mode, max, options, selectOption):
		super().__init__(
			style=disnake.ButtonStyle.gray,
			label="-1" if mode == -1 else "+1",
			disabled=True if (mode == -1 and cardLen == 1) or (mode == 1 and cardLen == max) else False
		)
		self._channel = channel
		self._now = now
		self._card = card
		self._max = max
		self._cardLen = cardLen
		self._select = options
		self._option = selectOption

	async def callback(self, i: disnake.Interaction):
		cardLen = self._cardLen + int(self.label)
		if cardLen < 1:
			cardLen = 1
		if cardLen > self._max:
			cardLen = self._max
		conn = sqlite3.connect("InGame.db", isolation_level=None)
		c = conn.cursor()
		c.execute(f"SELECT card13 FROM InGameCard WHERE channel='{self._channel}' AND user={i.user.id}")
		joker = c.fetchone()[0]
		cardLenP = cardLen
		if joker > 0:
			cardLenP = f"{cardLen-joker}(`{cardLen}`+★`{joker}`)"
		embed = disnake.Embed(
			title="카드 개수 정하기",
			description=f"정말 [{cardEmoji[self._card-1]} {cardName[self._card-1]}] ×{cardLenP}장을 내시겠어요?"
		)
		await i.response.edit_message(embed=embed, view=InGame_CardLenView(self._channel, self._now, self._card, cardLen, self._select, self._option, self._max))

class InGame_CardLenBtnConfirm(disnake.ui.Button):
	def __init__(self, channel, now, card, cardLen):
		super().__init__(
			style=disnake.ButtonStyle.green,
			label="결정",
			row=2
		)
		self._channel = channel
		self._now = now
		self._card = card
		self._cardLen = cardLen
	
	async def callback(self, i: disnake.Interaction):
		conn = sqlite3.connect(f"InGame.db", isolation_level=None)
		c = conn.cursor()
		c.execute(f"UPDATE InGame SET card={self._card},card_len={self._cardLen},last={self._now},now=now+1 WHERE channel='{self._channel}'")
		c.execute(f"SELECT card{self._card} FROM InGameCard WHERE channel='{self._channel}' AND user={i.user.id}")
		cardNow = c.fetchone()[0]
		joker = 0
		if cardNow < self._cardLen:
			joker = self._cardLen - cardNow
			self._cardLen -= joker
			c.execute(f"UPDATE InGameCard SET cards=cards-{joker},card13=card13-{joker} WHERE channel='{self._channel}' AND user={i.user.id}")
		c.execute(f"UPDATE InGameCard SET cards=cards-{self._cardLen},card{self._card}=card{self._card}-{self._cardLen} WHERE channel='{self._channel}' AND user={i.user.id}")
		if int(self._now)+1 > await InGame_GetUserLen(self._channel):
			c.execute(f"UPDATE InGame SET now=1 WHERE channel='{self._channel}'")
		embed = disnake.Embed(
			description=f"{i.user.mention}님이 [{cardEmoji[self._card-1]} {cardName[self._card-1]}] {self._cardLen}장을 냈어요!"
		)
		if joker > 0:
			embed.description = f"{i.user.mention}님이 [{cardEmoji[self._card-1]} {cardName[self._card-1]}] {self._cardLen+joker}(`{self._cardLen}`+`{joker}`)장을 냈어요!"
		await i.response.edit_message(embed=embed, view=None)
		await InGame_Go(self._channel, i.channel, embed)

class InGame_CardLenBtnPass(disnake.ui.Button):
	def __init__(self, channel, now):
		super().__init__(
			style=disnake.ButtonStyle.red,
			label="패스",
			row=2
		)
		self._channel = channel
		self._now = now
	
	async def callback(self, i: disnake.Interaction):
		conn = sqlite3.connect(f"InGame.db", isolation_level=None)
		c = conn.cursor()
		c.execute(f"UPDATE InGame SET now=now+1 WHERE channel='{self._channel}'")
		if int(self._now)+1 > await InGame_GetUserLen(self._channel):
			c.execute(f"UPDATE InGame SET now=1 WHERE channel='{self._channel}'")
		embed = disnake.Embed(
			description=f"{i.user.mention}님이 패스하셨어요."
		)
		await i.response.edit_message(embed=embed, view=None)
		await InGame_Go(self._channel, i.channel, embed)

class InGame_CardLenView(disnake.ui.View):
	def __init__(self, channel, now, card, cardLen, options, selectOption, max=None):
		super().__init__(timeout=None)
		conn = sqlite3.connect("InGame.db", isolation_level=None)
		c = conn.cursor()
		if not max:
			c.execute(f"SELECT user{now} FROM InGame WHERE channel='{channel}'")
			userSearch = c.fetchone()[0]
			c.execute(f"SELECT card{card} FROM InGameCard WHERE channel='{channel}' AND user={userSearch}")
			max = c.fetchone()[0]
			c.execute(f"SELECT card13 FROM InGameCard WHERE channel='{channel}' AND user={userSearch}")
			max += c.fetchone()[0]
		c.execute(f"SELECT last FROM InGame WHERE channel='{channel}'")
		last = c.fetchone()[0]
		if len(options) > 0:
			self.add_item(InGame_MyCardSelect(options, selectOption, "카드 선택"))
		if selectOption.find("/skip") == -1:
			self.add_item(InGame_CardLenBtnMinMax(channel, now, card, cardLen, 1, max, options, selectOption))
			self.add_item(InGame_CardLenBtnPlMa(channel, now, card, cardLen, -1, max, options, selectOption))
			self.add_item(InGame_CardLenBtnPlMa(channel, now, card, cardLen, +1, max, options, selectOption))
			self.add_item(InGame_CardLenBtnMinMax(channel, now, card, cardLen, 2, max, options, selectOption))
		self.add_item(InGame_CardLenBtnConfirm(channel, now, card, cardLen))
		if now != last:
			self.add_item(InGame_CardLenBtnPass(channel, now))

cardName = [
	"달무티", "대주교", "시종장", "남작부인",
	"수녀원장", "기사", "재봉사", "석공",
	"요리사", "양치기", "광부", "농노",
	"어릿광대"
]

class InGame_MyCardBtn(disnake.ui.Button['InGame_Controller']):
	def __init__(self, channel: str):
		super().__init__(style=disnake.ButtonStyle.blurple, label="내 카드")
		self._channel = channel
	
	async def callback(self, i: disnake.Interaction):
		conn = sqlite3.connect("InGame.db", isolation_level=None)
		c = conn.cursor()
		c.execute(f"SELECT cards FROM InGameCard WHERE channel='{self._channel}' AND user={i.user.id}")
		card_len = c.fetchone()[0]
		options = []
		for x in range(1, 14):
			c.execute(f"SELECT card{x} FROM InGameCard WHERE channel='{self._channel}' AND user={i.user.id}")
			n = c.fetchone()[0]
			if n != 0:
				options.append(
					disnake.SelectOption(
						label=f"[{x}] {cardName[x-1]}",
						description=f"{n}장 보유 중"
					)
				)
		embed = disnake.Embed(
			title="내 카드",
			description=f"총 카드 수: {card_len}"
		)
		await i.response.send_message(embed=embed, view=InGame_MyCardView(options), ephemeral=True)

cardEmoji = [
	"1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣",
	"6️⃣", "7️⃣", "8️⃣", "9️⃣", "1️⃣0️⃣",
	"1️⃣1️⃣", "1️⃣2️⃣", "⭐"
]

class InGame_MyTurn(disnake.ui.Button['InGame_Controller']):
	def __init__(self, channel: str):
		super().__init__(style=disnake.ButtonStyle.green, label="내 턴!")
		self._channel = channel
	
	async def callback(self, i: disnake.Interaction):
		conn = sqlite3.connect("InGame.db", isolation_level=None)
		c = conn.cursor()
		c.execute(f"SELECT now FROM InGame WHERE channel='{self._channel}'")
		now = c.fetchone()[0]
		user = None
		if not now == -1 and not now == -2:
			c.execute(f"SELECT user{now} FROM InGame WHERE channel='{self._channel}'")
			user = c.fetchone()[0]
		if now:
			if now == -1 or now == -2:
				c.execute(f"SELECT user1,user2 FROM InGame WHERE channel='{self._channel}'")
				jogong = c.fetchone()
				c.execute(f"SELECT COUNT(user) FROM InGameCard WHERE channel='{self._channel}'")
				userLen = c.fetchone()[0]
				if jogong[0] == i.user.id:
					me = 1
					cardToMe = 2
					c.execute(f"SELECT user{userLen} FROM InGame WHERE channel='{self._channel}'")
				elif jogong[1] == i.user.id:
					me = 2
					cardToMe = 1
					c.execute(f"SELECT user{userLen-1} from InGame WHERE channel='{self._channel}'")
				else:
					await i.response.send_message(embed=makeErrorEmbed("차례가 아니에요."), ephemeral=True)
					return
				toCard = c.fetchone()[0]
				options = []
				meCard = []
				for x in range(1, 14):
					c.execute(f"SELECT card{x} FROM InGameCard WHERE channel='{self._channel}' AND user={i.user.id}")
					cardfetch = c.fetchone()[0]
					if cardfetch != 0:
						options.append(
							disnake.SelectOption(
								label=f"[{x}] {cardName[x-1]}",
								description=f"{cardfetch}장 보유 중",
								value=f"{x}"
							)
						)
					c.execute(f"SELECT card{x} FROM InGameCard WHERE channel='{self._channel}' AND user={toCard}")
					card = c.fetchone()[0]
					if card > 0:
						for a in range(cardToMe):
							if len(meCard) < cardToMe and card > 0:
								card -= 1
								meCard.append(f"{cardEmoji[x-1]} {cardName[x-1]}")
				if cardToMe == 1:
					meCard.append(".")
				embed = disnake.Embed(
					title="조공 타임!",
					description=f"<@!{toCard}>님에게 **지급할 카드** __{cardToMe}장__을 선택해주세요.\n\n보낼 카드\n> \n> \n\n받을 카드\n> {meCard[0]}\n> {meCard[1]}" if cardToMe == 2 else f"<@!{toCard}>님에게 **지급할 카드** __{cardToMe}장__을 선택해주세요.\n\n보낼 카드\n> \n\n받을 카드\n> {meCard[0]}"
				)
				await i.response.send_message(embed=embed, view=InGame_MyCardView(options, f"{self._channel}/jogong/{me}/{userLen-me+1}/{meCard[0]}/{meCard[1]}"), ephemeral=True)
			elif user == i.user.id:
				embed = disnake.Embed(
					title="카드 내기",
					description="낼 카드\n> 카드를 선택해주세요!"
				)
				c.execute(f"SELECT last FROM InGame WHERE channel='{self._channel}'")
				last = c.fetchone()[0]
				if not now == last:
					c.execute(f"SELECT card,card_len FROM InGame WHERE channel='{self._channel}'")
					card, cardLen = c.fetchone()
					c.execute(f"SELECT card13 FROM InGameCard WHERE channel='{self._channel}' AND user={i.user.id}")
					joker = c.fetchone()[0]
				else:
					card = 13
					cardLen = 1
					joker = 0
				options = []
				for x in range(1, card):
					c.execute(f"SELECT card{x} FROM InGameCard WHERE channel='{self._channel}' AND user={i.user.id}")
					n = c.fetchone()[0]
					if n > (cardLen-1)-joker and n > 0:
						options.append(
							disnake.SelectOption(
								label=f"[{x}] {cardName[x-1]}",
								description=f"{n}장 보유 중",
								value=f"{x}/{cardLen}"
							)
						)
				await i.response.send_message(embed=embed, view=InGame_MyCardView(options, f"{self._channel}/game/{now}/{cardLen}/{joker}" if now == last else f"{self._channel}/game/{now}/{cardLen}/{joker}/skip"), ephemeral=True)
			else:
				await i.response.send_message(embed=makeErrorEmbed("차례가 아니에요!"), ephemeral=True)
		else:
			await i.response.send_message(embed=makeErrorEmbed("비정상적인 접근이에요."), ephemeral=True)

class InGame_Controller(disnake.ui.View):
	def __init__(self, channel: str):
		super().__init__(timeout=None)
		self.add_item(InGame_MyTurn(channel))
		self.add_item(InGame_MyCardBtn(channel))

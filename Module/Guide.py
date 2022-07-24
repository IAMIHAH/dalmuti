import disnake

GuideEmbed = [
	disnake.Embed(
		title="📖 이용 가이드",
		description="**인생은 불공평합니다.**\n\n환영합니다! 😁\n이 가이드로 달무티를 해보셨던 분들과 하지 않았던 모든 분들에게 충분한 설명이 되기를 바라요.\n먼저, `/달무티` 명령어를 사용해서 게임을 즐길 수 있어요. 채널을 생성하거나, 입장할 수 있죠."
	),
	disnake.Embed(
		title="📖 이용 가이드",
		description="게임 채널에 생성하려면 `/달무티`를 실행해 로비창을 띄워야 해요.\n\n공개 채널은 **봇 DM**에서 생성할 수 있어요.\n비공개 채널은 **채널 입장을 원하는 서버**에서 생성할 수 있어요."
	),
	disnake.Embed(
		title="📖 이용 가이드",
		description="게임 채널에 입장하려면 마찬가지로 `/달무티`를 실행해 로비창을 띄워야 해요.\n\n\n채널 입장은 마찬가지로 위에서 언급한 위치에서 입장할 수 있어요.\n비공개 채널인 경우 공개 스레드로 생성하면 해당 스레드의 첫 메시지에 있는 버튼을 눌러 입장할 수 있어요.\n비공개 스레드로 생성하면 채널 코드를 원하는 유저에게 알려주어야 해요.\n비공개 스레드는 **서버 부스트 __2레벨__** 이상만 이용할 수 있으니 주의해주세요!"
	),
	disnake.Embed(
		title="🎮 게임 가이드",
		description="그럼 이제 게임을 시작했을 것 같으니 게임에 대한 설명을 하도록 할게요.\n\n각 카드에는 계급이 존재합니다. 1부터 12까지의 계급이 있는데, 숫자가 커질수록 계급이 낮아져요.\n각 카드에 대한 설명은 아래 __카드 목록__을 눌러 자세한 설명을 확인해보세요!\n\n카드의 장 수는 카드의 계급만큼 존재해요.\n1 달무티가 한 장, 2 대주교가 두 장, 이런 셈이죠. 다만, 조커 카드는 총 2장이에요.\n조커 카드는 다음에 알려드릴게요.\n이렇게 해서 카드 수는 총 80장으로 이루어져 있어요."
	),
	disnake.Embed(
		title="🎮 게임 가이드",
		description="카드 중에는 **조커** 카드도 있어요. 조커 카드는 계급상으로는 가장 낮게 위치해있어요. 13이란 뜻이죠.\n하지만, 조커는 하나만 쓸 때보다 다른 카드와 같이 쓰일 때 효과가 좋아요.\n왜냐하면 조커는 낼 계급 카드를 복제하는 능력을 지녔거든요.\n예를 들자면, 누가 시종장(3) 두 장을 내면 내가 대주교(2) 한 장과 조커 한 장을 사용할 수 있어요.\n또한 달무티(1) 한 장과 조커 한 장을 사용할 수도 있어요. 딱히 막진 않는답니다.\n\n**하지만**... 조커 카드의 또 다른 능력이 있어요.\n조커 카드를 두 장 가지고 있다면 **혁명**을 일으킬 수 있어요.\n혁명을 원한다면 조커 두 장을 바로 공개하면 되지만, 높은 신분이라면 공개하면 불리해지겠죠?\n이렇게 공개한 카드는 자신이 계속 가지고 위에 설명한 효과를 사용할 수 있어요.\n\n가장 낮은 계급이 혁명을 일으킨다면 계급을 뒤바꿀 수 있어요.\n가장 높은 계급이 가장 낮은 계급으로 되는 것이죠."
	),
	disnake.Embed(
		title="🎮 게임 가이드",
		description="게임을 시작했다면 순서를 정하기 위해 카드를 한 장씩 뽑아요. 아, 뽑는다는 말은 조금 어색한가요?\n시스템이 알아서 정해줄거에요. 자신의 운을 믿어봐요!\n물론, 조커가 뽑힌다면 앞에서 설명했듯이 제일 낮은 계급이겠죠?\n높은 계급부터 낮은 계급 순으로 계급이 정해져요. 4, 9, 1, 12가 뽑혔다면 1, 4, 9, 12 순으로 계급이 정해지고, 이 순서로 게임을 진행해요.\n계급을 지칭하는 말은 채널의 사람들끼리 정하면 돼요.\n\n원한다면 각 계급이 낮은 계급에게 명령을 내릴 수 있어요. 이 규칙은 채널의 사람들끼리 원하는대로 조정해보세요!\n\n이제 순서를 정하기 위한 카드를 가지고 있고, 카드가 자동으로 분배될 거에요. 이 때 분배되는 수는 플레이어 수 만큼 똑같이 배부해요.\n다만 딱 맞지 않는 경우는 높은 계급부터 한 장씩을 더 분배해요."
	),
	disnake.Embed(
		title="🎮 게임 가이드",
		description="가장 낮은 계급을 가진 사람은 보유한 카드 중 계급이 높은 카드 2장을 가장 높은 계급을 가진 사람에게 바쳐야 해요.\n반대로, 가장 높은 계급을 가진 사람은 보유한 카드 중 **쓸모 없는 카드** 2장을 주어야 하죠.\n가장 낮은 계급보다 한 단계 높은 계급인 경우 가장 높은 계급보다 한 단계 낮은 계급의 사람과 위와 같이 1장씩 교환해요.\n낮은 계급의 카드 조공은 자동으로 되지만, 높은 계급이 줄 카드를 선택할 때는 직접 선택해야 해요.\n\n이렇게 카드 조공 단계를 완료했다면 게임이 시작되어요. 이 때에 아까 정해진 순서대로 게임이 진행되어요."
	),
	disnake.Embed(
		title="🎮 게임 가이드",
		description="게임을 진행할 때 카드를 내야하는 규칙이 있어요.\n\n이전에 카드를 낸 사람보다 더 높은 계급의 카드를 해야 해요.\n이때 주의해야 할 점은 맨 처음 카드를 낸 사람이 낸 카드의 수만큼 내야 해요.\n예를 들자면, 농노(12) 3장을 낸 경우 농노보다 높은(11↑) 카드를 3장 내야하죠.\n\n이 때 카드를 내고 싶지 않거나 낼 수 없는 경우 패스할 수 있어요.\n이 외에도 1분동안 아무 카드도 내지 않을 경우 자동으로 패스되어요.\n졸린 유저가 선택하지 않아 게임이 진행되지 않기를 위해서에요. 양해 부탁드려요!\n\n패스로 한 바퀴를 돌아서 마지막에 카드를 낸 사람으로 턴이 돌아오게 되면 그 사람이 다시 원하는 카드를 낼 수 있어요."
	),
	disnake.Embed(
		title="🎮 게임 가이드",
		description="이렇게 카드를 계속 써가며 카드를 빨리 없애는 사람이 이겨요.\n이후에도 게임은 계속 되는데, 새로운 계급을 정하기 위해서죠.\n\n이렇게 게임이 끝나고, 새로운 계급이 정해지면 새로운 게임을 시작해요.\n이 때 게임에서 빠지고 싶은 경우 그 사람은 제외하고 게임을 시작해요.\n만약 게임이 끝나고 새로운 사람이 게임에 참여할 경우 계급이 초기화 되어요."
	)
]

class Guide_ArrowBtn(disnake.ui.Button['Guide_Controller']):
	def __init__(self, page, add):
		disabled = False
		if add < 0:
			emoji = "◀️"
			if page == 1:
				disabled = True
		if add > 0:
			emoji = "▶️"
			if len(GuideEmbed)+1 == page+add:
				disabled = True
		if not disabled:
			self._page = page+add
		super().__init__(style=disnake.ButtonStyle.gray, emoji=emoji, disabled=disabled, row=2)

	async def callback(self, i: disnake.Interaction):
		await i.response.edit_message(embed=GuideEmbed[self._page-1], view=Guide_Controller(self._page))

class Guide_Card(disnake.ui.Select):
	def __init__(self):
		options = [
			disnake.SelectOption(label="[1] 달무티"),
			disnake.SelectOption(label="[2] 대주교"),
			disnake.SelectOption(label="[3] 시종장"),
			disnake.SelectOption(label="[4] 남작부인"),
			disnake.SelectOption(label="[5] 수녀원장"),
			disnake.SelectOption(label="[6] 기사"),
			disnake.SelectOption(label="[7] 재봉사"),
			disnake.SelectOption(label="[8] 석공"),
			disnake.SelectOption(label="[9] 요리사"),
			disnake.SelectOption(label="[10] 양치기"),
			disnake.SelectOption(label="[11] 광부"),
			disnake.SelectOption(label="[12] 농노"),
			disnake.SelectOption(label="[조커] 어릿광대")
		]
		super().__init__(
			placeholder="카드 목록",
			options=options,
			row=1
		)
	
	async def callback(self, i: disnake.Interaction):
		if "[조커]" in self.values[0]:
			cardId = 13
			cardNumber = 2
		else:
			cardId = int(self.values[0].split(" ")[0].replace("[", "").replace("]", ""))
			cardNumber = cardId
		embed = disnake.Embed(
			title=f"{self.values[0]}"
		)
		embed.add_field(name="카드 개수", value=f"{cardNumber}개")
		embed.set_image(url=f"https://bpmo.xyz/box/dalmuti/{cardId}.png")
		await i.response.send_message(embed=embed, ephemeral=True)

class Guide_Controller(disnake.ui.View):
	def __init__(self, page=1):
		super().__init__(timeout=None)
		self.add_item(Guide_ArrowBtn(page, -1))
		self.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, label=f"페이지 {page}/{len(GuideEmbed)}", disabled=True, row=2))
		self.add_item(Guide_ArrowBtn(page, 1))
		if page == 4:
			self.add_item(Guide_Card())
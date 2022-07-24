#-*- coding:utf-8 -*-
import asyncio
import sqlite3
import disnake, os
from disnake.ext import commands
from Module.Log import p

bot = commands.Bot(command_prefix=commands.when_mentioned)#, test_guilds=[742188157424107679])

for filename in os.listdir("Cogs"):
	if filename.endswith(".py"):
		fn = filename[:-3]
		try:
			bot.load_extension(f"Cogs.{fn}")
			p("info", f"{fn}: Sucessfully Loaded!")
		except Exception as e:
			p("error", f"{fn}: {e}")

@bot.event
async def on_ready():
	p("info", "Ready!")
	p("info", f"{bot.user.name} │ {bot.user.id}")

@bot.event
async def on_thread_create(thread: disnake.Thread):
	if thread.owner.id == bot.user.id:
		channel = thread.name.split(" ")[1]
		await asyncio.sleep(180)
		await OutGame_NoSleep(channel)

async def OutGame_NoSleep(channel: str):
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

bot.run("OTk4MTM2Njk0NzYxMDgyOTEx.GBGQfJ.fMF66xF4UY2UVPOYFMf8h18fhUwDMgfRHK9zpI")
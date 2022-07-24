#-*- coding:utf-8 -*-
import asyncio
import disnake, os
from disnake.ext import commands

from Module.Log import p
from Module.OutGame import OutGame_NoSleep

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
		await OutGame_NoSleep(channel, bot)

bot.run("OTk4MTM2Njk0NzYxMDgyOTEx.GBGQfJ.fMF66xF4UY2UVPOYFMf8h18fhUwDMgfRHK9zpI")
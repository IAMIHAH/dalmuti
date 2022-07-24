import sqlite3
from disnake.ext import commands
import disnake
from Module.Embed import makeErrorEmbed
from Module.User import getUser

class Signup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="가입",
        description="달무티에 가입합니다."
    )
    async def registry(i: disnake.CommandInteraction):
        if not getUser(i.user.id):
            conn = sqlite3.connect("User.db", isolation_level=None)
            c = conn.cursor()
            c.execute(f"INSERT INTO User(id) Values({i.user.id})")
            embed = disnake.Embed(
                title="✅ 가입을 완료했어요.",
                description="`/가이드`를 확인해주세요!"
            )
        else:
            embed = makeErrorEmbed("이미 가입을 완료했어요.")
        await i.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Signup(bot))
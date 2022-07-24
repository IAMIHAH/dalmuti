import disnake

def makeErrorEmbed(text: str="오류가 발생했어요."):
    return disnake.Embed(
        title=":warning: 오류!",
        color=0xff0000,
        description=text
    )
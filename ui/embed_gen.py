import discord

def embed_fail(interaction:discord.Interaction,message:str) -> discord.Embed:
    embed=discord.Embed(description=message,color=0xd4401e)
    embed.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
    return embed
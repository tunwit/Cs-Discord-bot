import discord

def embed_fail(interaction:discord.Interaction,message:str) -> discord.Embed:
    embed=discord.Embed(description=message,color=0xd4401e)
    embed.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
    return embed

def embed_success(interaction:discord.Interaction,message:str) -> discord.Embed:
    embed=discord.Embed(description=message,color=0x21c210)
    embed.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
    return embed

def embed_info(interaction:discord.Interaction,message:str) -> discord.Embed:
    embed=discord.Embed(description=message,color=0x3495c2)
    embed.set_author(name=interaction.user.name,icon_url=interaction.user.display_avatar.url)
    return embed
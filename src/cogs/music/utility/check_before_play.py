import wavelink
import discord
from ui.embed_gen import embed_fail

async def check_before_play(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc == None:
        embed = embed_fail(interaction,"❌ Bot is currently not in the voice channel.")
        await interaction.followup.send(embed=embed)
        return False
    if interaction.user.voice == None:
        embed = embed_fail(interaction,"❌ You are not currently in voice channel")
        await interaction.followup.send(embed=embed)
        return False
    if interaction.guild.voice_client.channel != interaction.user.voice.channel:
        embed = embed_fail(interaction,"❌ Bot is now used by others voice channel")
        await interaction.followup.send(embed=embed)
        return False
    return True
import asyncio
import discord
import wavelink

async def nosong(self, interaction:discord.Interaction):
    i=0
    while True:
        vc: wavelink.Player = interaction.guild.voice_client
        if vc.queue or vc.current:
            break
        i+=1
        print(f'counting no song {interaction.guild.name} | {i}')
        await asyncio.sleep(0.4)
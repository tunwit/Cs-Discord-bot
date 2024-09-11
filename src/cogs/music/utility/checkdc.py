import asyncio
import discord
import wavelink

async def checkdc(member:discord.Member):
    vc: wavelink.Player = member.guild.voice_client
    i=0
    while True:
        i += 1
        print(f'counting alonetime {member.guild.name} | {i}')
        if len(vc.channel.members) > 1:
            break
        await asyncio.sleep(1)
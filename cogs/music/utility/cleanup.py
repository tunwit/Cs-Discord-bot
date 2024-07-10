
import wavelink
import discord

async def cleanup(guild:discord.Guild, frm):
    vc: wavelink.Player = guild.voice_client
    if vc == None:
        return
    vc.queue.clear()
    try:
        await vc.np.delete()
    except:
        pass
    await vc.disconnect()
import wavelink
from PIL import Image, ImageDraw 
import itertools
import discord
import io
from cogs.music.utility.convert import convert

trans_queueMode= {
            'wavelink.QueueMode.normal':"Disable",
            'wavelink.QueueMode.loop':"Song",
            'wavelink.QueueMode.loop_all':"Queue"
        }

trans_autoMode= {
            'wavelink.AutoPlayMode.partial':"Disable",
            'wavelink.AutoPlayMode.enabled':"Enable"
        }

class nowplaying:
    def __init__(self):
        pass

    async def edit(self, vc, content, embed, file, is_expired=False):
        if not is_expired:
            np = await vc.interaction.followup.edit_message(message_id=vc.np.id,content=content, embed=embed,view=vc.Myview ,attachments=[file])
        else:
            #retrive np message by id
            channel:discord.TextChannel = await vc.client.fetch_channel(int(vc.client.last_nowplaying[str(vc.guild.id)]['channel']))
            message:discord.Message = await channel.fetch_message(int(vc.client.last_nowplaying[str(vc.guild.id)]['message']))
            np = await message.edit(content=content, embed=embed,view=vc.Myview ,attachments=[file])
        return np
        
    async def send(self, vc, content, embed, file, is_expired=False):
        if not is_expired:
            np = await vc.interaction.followup.send(content=content, embed=embed, view=vc.Myview, file=file)
        else:
            #retrive np channel by id
            channel: discord.TextChannel = await vc.client.fetch_channel(int(vc.client.last_nowplaying[str(vc.guild.id)]['channel']))
            np = await channel.send(content=content, embed=embed, view=vc.Myview, file=file)
        return np
    
    async def np(self, interaction, send=False):
        vc: wavelink.Player = interaction.guild.voice_client
        interaction: discord.Interaction = vc.interaction 
        if vc:
            if vc.current is not None:
                lst = list(vc.queue)
                if vc.queue.mode == wavelink.QueueMode.loop_all:
                    lst = lst + list(vc.queue.history)
                upcoming = list(itertools.islice(lst, 0, 4))
                fmt = "\n".join(
                    f'` {index}.{track} `' for index, track in enumerate(upcoming, start=1)  
                )    
                try:
                    duration = f"{convert(vc.position)}/{convert(vc.current.length)}"
                except Exception as e:
                    print("durationerror", e)
                    duration = "Unable to calculate"

                npembed = discord.Embed(
                    title=f"{vc.current.title}",
                    url=vc.current.uri,
                    color=0xFFFFFF,
                )
                npembed.set_author(
                    name=f"Added by {vc.current.extras.requester}",
                    icon_url=f"{vc.current.extras.requester_icon}",
                )
                npembed.add_field(
                    name="Channel", value=f"<#{vc.channel.id}>"
                )
                npembed.add_field(
                    name="Duration", value=f"`{duration}`"
                )
                npembed.set_footer(
                    text=f"{'Paused' if vc.paused else 'Playing'} | {vc.volume}% | LoopStatus:{trans_queueMode[f'wavelink.{str(vc.queue.mode)}']} | Autoplay:{trans_autoMode[f'wavelink.{str(vc.autoplay)}']}"
                )
                npembed.set_thumbnail(url=vc.current.artwork)
                
                more = f"`And more {len(lst)-4} songs.`" if len(lst) - 4 > 0 else None
                fmt = fmt if fmt else "`There are no songs in the queue`"

                with io.BytesIO() as image_binary:
                    total = vc.current.length // 1000
                    progress = vc.position // 1000
                    w, h = 350, 10
                    r = 3
                    length = (progress * w) / total
                    img = Image.new("RGBA", (w, h)) 
                    img1 = ImageDraw.Draw(img)   
                    img1.line(xy=(-1, 5, 350, 5), fill="white", width=2) 
                    img1.line(xy=(-1, 5, length, 5), fill="red", width=2, joint='curve')
                    img1.ellipse(xy=(length-r, 5-r, length+r, 5+r), fill='darkred')
                    img.save(image_binary, 'PNG')
                    image_binary.seek(0)

                    file = discord.File(image_binary, filename="image.png")
                    npembed.set_image(url="attachment://image.png")
                    content = f'**queue:**\n{fmt}' + (f'\n{more}' if more else '')

                    if send:
                        vc.np = await self.send(vc=vc, content=content, embed=npembed, file=file, is_expired=vc.interaction.is_expired())
                    elif vc.np:
                        try:
                            vc.np = await self.edit(vc=vc, content=content, embed=npembed, file=file, is_expired=vc.interaction.is_expired())
                        except:
                            vc.np = await self.edit(vc=vc, content=content, embed=npembed, file=file, is_expired=vc.interaction.is_expired())
                    else:
                        vc.np = await self.send(vc, content=content, embed=npembed, file=file, is_expired=vc.interaction.is_expired())

                    vc.client.last_nowplaying.update({
                        str(vc.guild.id): {
                            "channel": str(vc.interaction.channel.id),
                            "message": str(vc.np.id)
                        }
                    })
                    return vc.np

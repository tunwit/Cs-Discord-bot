import wavelink as wavelink
from discord.ext import commands
import discord
from discord import app_commands
from cogs.music.ui.controlpanal import *
from cogs.music.eventmanager import eventManager
from cogs.music.utility.check_before_play import check_before_play
from cogs.music.ui.nowplaying import nowplaying
from ui.embed_gen import embed_success

class announceAPI(commands.Cog):
    def __init__(self, bot ):
        self.bot = bot
    
    async def extract(self,file:discord.Attachment):
        with open("test.txt","r") as f:
            f = await file.to_file()
            lines = [line.decode("utf-8")for line in f.fp.readlines()]+["$%"]
        spe_keywords = ["footer","fields","thumbnail","image"]
        state = None
        sub_state = None
        embed = {
            "fields":[]
        }
        sub_state_check = False
        previous_indentlevel = 0
        extract = []
        for index in range(len(lines)):
            line_indent = lines[index]
            indent = len(line_indent) - len(line_indent.lstrip())
            line = lines[index].lstrip().strip("\n").strip("\r")
            if len(line) == 0:
                continue
            if indent == 0:
                if line != "embed:" and line != "$%":
                    extract.append(line)
                if state == "embed":
                    extract.append(embed)
                    embed = {
                        "fields":[]
                    }
                    state = None
                    sub_state = None
            if sub_state in spe_keywords and sub_state_check:
                if previous_indentlevel != indent:
                    sub_state_check = False
                    previous_indentlevel = 0

            if not state and line.split(":")[0] == "embed":
                state = "embed"
            elif state == "embed" and line.split(":")[0] in spe_keywords:
                sub_state = line.split(":")[0]
            elif state == "embed" and line.split(":")[0] not in spe_keywords and not sub_state:
                split = line.split(":",1)
                if split[0] == "color":
                    embed[split[0]] = int(split[1],0)
                else:
                    embed[split[0]] = split[1]
            elif sub_state in spe_keywords and not sub_state_check:
                pr = indent
                i = 0
                while True:
                    if (index+i) > len(lines)-1:
                        break
                    indent_ = len(lines[index+i]) - len(lines[index+i].lstrip())
                    
                    if pr == indent_:
                        pass
                    else:
                        break
                    i+=1
                if sub_state == "fields":
                    try:
                        embed["fields"].append({
                            "name":lines[index:index+i][0].split(":")[1].lstrip(),
                            "value":lines[index:index+i][1].split(":",1)[1].lstrip(),
                            "inline":True
                        })
                    except:pass
                else:
                    embed[sub_state] = {
                    i.lstrip().split(":")[0]:i.lstrip().split(":",1)[1] for i in lines[index:index+i]
                    }
                sub_state_check = True
                previous_indentlevel = 0

        return extract
    
    @app_commands.command(
        name="announce_file",
        description="make bot to announce message",
    )
    async def announce_file(self, interaction: discord.Interaction,file:discord.Attachment):
        await interaction.response.send_message("sending",ephemeral=True)
        result =  await self.extract(file)
        for i in result:
            try:
                if isinstance(i,dict):
                    await interaction.channel.send(embed = discord.Embed.from_dict(i))
                else:
                    await interaction.channel.send(i)
            except:
                await interaction.followup.send("something wrong with",ephemeral=True)
                break
    
    # @app_commands.command(
    #     name="announce_help",
    #     description="send format to your dm",
    # )
    # async def announce_help(self, interaction: discord.Interaction,file:discord.Attachment):
    #     await interaction.response.send_message("See help file in your DM",ephemeral=True)
        

async def setup(bot):    
  await bot.add_cog(announceAPI(bot))  
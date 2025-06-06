from discord.ext import commands,tasks
import discord
import os
from dotenv import load_dotenv
from setup import config
from pymongo.mongo_client import MongoClient
import wavelink
import itertools
import asyncio
intents = discord.Intents.all()

# uselavalink is set to True bot will try to connect to lavalink server
# if local is enabled bot will try to connect to local lavalink server
# wavelink.Node.fetch_version() #Lavalink version
# wavelink.Node.status # is connect
# lavalink_Stat:StatsResponsePayload = wavelink.Node.fetch_stats() #Lavalink Stat
# lavalink_Stat.cpu.cores
# lavalink_Stat.cpu.lavalink_load
# lavalink_Stat.memory.used

class csbot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            intents=intents,
            command_prefix=".",
            help_command=None,
            application_id=config["APPLICATION_ID"],
        )
        self.config = config
        self.mango = MongoClient(config["MONGO"])["Main"]
        self.cs_mango = MongoClient(config["MONGO"])["CS_BOT"]   
        self.invites = {}
        self.last_nowplaying = {}
        self.node = None

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if os.path.isdir(f"./cogs/{filename}") and not filename.startswith("_"):
                for filename_in in os.listdir(f"./cogs/{filename}"):
                     if filename_in.endswith(".py") and not filename_in.startswith("_"):
                        await self.load_extension(f"cogs.{filename}.{filename_in[:-3]}")
            if filename.endswith(".py") and not filename.startswith("_"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        await self.tree.sync()

bot = csbot()

async def get_invites():
    guilds = bot.guilds
    for guild in guilds:
        try:
            invites = await guild.invites()
            bot.invites.update({
            str(guild.id):invites
            })    
        except Exception as e:
            print(f"Cant get invite from {guild}")
            bot.invites.update({
            str(guild.id):[]
            }) 
       
async def fuckyou():
    target = bot.get_guild(927379549338083389)
    for channel in target.text_channels:
        try:
            print(f"Message in {channel.name}:")
            print("======================")
            async for text in channel.history():
                print(text.content)
                print("----------")
            print("======================")
        except:pass
        
    
async def node_connect():
    if config["LAVALINK_OPTIONS"]['uselavalink'] :
        if config["LAVALINK_OPTIONS"]['local']:
            uri ='http://localhost:2333'
            if config["PRODUCTION"] == True:
                uri ="http://lavalink:2333"
            node = wavelink.Node(uri = uri, password="youshallnotpass",retries=5) # Local Lavalink server
        else:
            node = wavelink.Node(uri ='https://lavalink.1liner.co', password="youshallnotpass",retries=5) # prefered Lavalink server
        bot.node = node
        await wavelink.Pool.connect(client=bot, nodes=[node])

@bot.event
async def on_wavelink_node_ready(node: wavelink.NodeReadyEventPayload):
    print(f"Wavelink {node.node.identifier} connected")

@tasks.loop()
async def change_ac():
    statuses = [
        "Your heart ♥",
        "With lovely cat",
        f"Now is in 【{len(bot.guilds)}】 servers",
    ]
    for status in itertools.cycle(statuses):
        activity = discord.Game(name=status)
        await bot.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(15)
def details(config:dict):
    print("----------------------------")
    print(f"Token : {config['TOKEN']}")
    print(f"Application ID : {config['APPLICATION_ID']}")
    print(f"MONGO: {config['MONGO']}")
    print(f"Lavalink options: {config['LAVALINK_OPTIONS']}")
    print(f"Production: {config['PRODUCTION']}")
    print("----------------------------")

@bot.event
async def on_ready():
    # await fuckyou()
    await node_connect()
    await get_invites()
    change_ac.start()
    print("-------------------")
    print(f"{bot.user} is Ready")
    print("-------------------")
    
details(config)
bot.run(config["TOKEN"])
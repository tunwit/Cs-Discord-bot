from discord.ext import commands,tasks
import discord
import os
from dotenv import load_dotenv
from setup import config
from pymongo.mongo_client import MongoClient
import wavelink

intents = discord.Intents.all()

# uselavalink is set to True bot will try to connect to lavalink server
# if local is enabled bot will try to connect to local lavalink server


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
        self.invites = {}

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
        bot.invites.update({
            str(guild.id):await guild.invites()
        })

async def node_connect(): 
    if config["LAVALINK_OPTIONS"]['uselavalink'] :
        print("Connectiong to Lavalink",config)
        if config["LAVALINK_OPTIONS"]['local']:
            node = wavelink.Node(uri ='http://localhost:2333', password="youshallnotpass",retries=5) # Local Lavalink server
        else:
            node = wavelink.Node(uri ='http://lavalink:2333', password="youshallnotpass",retries=5) # prefered Lavalink server
        await wavelink.Pool.connect(client=bot, nodes=[node])

@bot.event
async def on_wavelink_node_ready(node: wavelink.NodeReadyEventPayload):
    print(f"Wavelink {node.node.identifier} connected")

@bot.event
async def on_ready():
    await get_invites()
    await node_connect()
    print("-------------------")
    print(f"{bot.user} is Ready")
    print("-------------------")

bot.run(config["TOKEN"])
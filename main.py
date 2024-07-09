from discord.ext import commands,tasks
import discord
import os
from dotenv import load_dotenv
from setup import config


intents = discord.Intents.all()

class csbot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            intents=intents,
            command_prefix=".",
            help_command=None,
            application_id=config["APPLICATION_ID"],
        )
        self.config = config
        self.invites = {}

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
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
        
@bot.event
async def on_ready():
    await get_invites()
    print("-------------------")
    print(f"{bot.user} is Ready")
    print("-------------------")

bot.run(config["TOKEN"])
import discord
import json

async def is_manager(interaction: discord.Interaction):
    with open('database/data.json','r') as database:
        data = json.load(database) 
        
    if interaction.user.id not in data["manager"]:
        await interaction.response.send_message("Unauthorize",ephemeral=True)
        return False
    return True
import discord
import json

async def is_manager(interaction: discord.Interaction):
    database = interaction.client.cs_mango["manager"]
    data = database.find_one({"user_id":str(interaction.user.id)})
    if not data:
        await interaction.response.send_message("Unauthorize",ephemeral=True)
        return False
    return True
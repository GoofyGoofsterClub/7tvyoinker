import os
import discord
from discord.ext import commands
import dotenv

dotenv.load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


async def start():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")
            print(f"Loaded {file[:-3]}")


@bot.event
async def on_ready():
    await start()
    print("Bot is ready")

bot.run(os.getenv("TOKEN"))

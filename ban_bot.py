import discord
from discord.ext import commands
import asyncio

import os

TOKEN = os.getenv("DISCORD_TOKEN")

# Your IDs
PROTECTED_CHANNEL_ID = 1516414504290877602
ALLOWED_ROLE_ID = 1261388459139141722

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("Bot is online and ready!")

@bot.event
async def on_message(message):
    # Ignore bots and DMs
    if message.author.bot or message.guild is None:
        return

    # Debug print
    print(f"{message.author} wrote in #{message.channel}: {message.content}")

    # Check if the message is in the protected channel
    if message.channel.id == PROTECTED_CHANNEL_ID:

        # Allow users with the exempt role
        if any(role.id == ALLOWED_ROLE_ID for role in message.author.roles):
            return

        user = message.author
        guild = message.guild

        try:
            print(f"Banning {user}...")

            await guild.ban(
                user,
                reason="Posted in restricted channel",
                delete_message_seconds=3600  # Delete last hour of messages
            )

            print(f"✅ Banned {user}")

            # Wait 10 days
            await asyncio.sleep(10 * 24 * 60 * 60)

            await guild.unban(user, reason="10-day ban expired")

            print(f"✅ Unbanned {user}")

        except discord.Forbidden:
            print("❌ Missing permissions to ban this user.")
        except Exception as e:
            print(f"❌ Error: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
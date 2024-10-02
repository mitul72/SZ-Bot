import discord
from discord.ext import commands
import random
import os  # Import os to access environment variables
from constants import characters
from dotenv import load_dotenv
from helper import Helper

load_dotenv()

# Set up the bot with command prefix '!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
helper = Helper()
helper.init_file()
ALLOWED_ROLE_IDS = [1082147979315654750, 1082147820506730516]


# In-memory XP storage (for demonstration purposes)
# user_xp = {}

# List of characters (expand this list when the game is released)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


def has_permission(ctx):
    # Check if the user is an administrator
    if ctx.author.guild_permissions.administrator:
        return True
    # Check if the user has any of the allowed roles
    for role in ctx.author.roles:
        if role.id in ALLOWED_ROLE_IDS:
            return True
    return False


@bot.command(name='xpraffle')
async def xp_raffle(ctx):
    # Permission check
    if not has_permission(ctx):
        await ctx.send("You do not have permission to use this command.")
        return

    # Get all members in the server who have the "XP Raffle" role
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="XP Raffle")
    if not role:
        await ctx.send("The 'XP Raffle' role does not exist.")
        return

    members = [member for member in role.members if not member.bot]
    if not members:
        await ctx.send("No members with the 'XP Raffle' role found.")
        return

    # Select a random member
    selected_member = random.choice(members)

    # Announce to the chat
    await ctx.send(f'{selected_member.mention}, you have been selected for the XP Raffle!')

    # Write the selected member's ID to the file using helper
    helper.write_raffle_member(selected_member.id)


@bot.command(name='xpshuffle')
async def xp_shuffle(ctx):
    # Permission check
    if not has_permission(ctx):
        await ctx.send("You do not have permission to use this command.")
        return

    # Read the selected member's ID from the file
    selected_member_id = helper.get_key_and_delete("raffle_member")
    if not selected_member_id:
        await ctx.send("No raffle member has been selected yet.")
        return

    # Get the member object
    guild = ctx.guild
    selected_member = guild.get_member(int(selected_member_id))
    if not selected_member:
        await ctx.send("Selected member not found in the guild.")
        return

    # Generate a random amount of XP between 500 and 10000
    xp_gain = random.randint(500, 10000)

    # Announce the XP gained to the selected member
    await ctx.send(f'{selected_member.mention}, you have gained {xp_gain} XP!')

    # Note: You can manually set their XP using /xp add command from Arcane bot


@bot.command(name='pvprandom')
async def pvp_random(ctx):
    # Get all members in the server except the author and bots
    guild = ctx.guild
    members = [member for member in guild.members if not member.bot and member != ctx.author]
    if not members:
        await ctx.send("No opponents available for PVP.")
        return

    # Select a random opponent
    opponent = random.choice(members)

    # Start the fight
    await ctx.send(f'{ctx.author.mention} is fighting {opponent.mention}!')


@bot.command(name='randomchar')
async def random_char(ctx):
    character = random.choice(characters)
    await ctx.send(f'Your character is {character}!')


# Retrieve the bot token from the environment variable
bot_token = os.environ.get('BOT_TOKEN')
if not bot_token:
    print("Error: The BOT_TOKEN environment variable is not set.")
    exit(1)

bot.run(bot_token)

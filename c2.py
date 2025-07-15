import discord
from discord.ext import commands
import asyncio

TOKEN = ''  # Replace with your bot token
CHANNEL_ID = 1394636742967164990  # Replace with your allowed channel ID
ROBLOX_FILE = 'roblox.txt'
TIKTOK_FILE = 'tiktok.txt'
COOLDOWN = 15  # 15 seconds cooldown per user

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

user_cooldowns = {}

def get_next_combo(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if not lines:
            return None
        combo = lines[0].strip()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines[1:])
        return combo
    except Exception as e:
        print(f'[ERROR] Reading file {file_path}: {e}')
        return None

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command(name='roblox')
async def roblox(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("❌ This command can only be used in the designated channel.")
        return

    user_id = ctx.author.id
    now = asyncio.get_event_loop().time()

    if user_id in user_cooldowns and now - user_cooldowns[user_id] < COOLDOWN:
        remaining = int(COOLDOWN - (now - user_cooldowns[user_id]))
        await ctx.reply(f'⏳ Please wait {remaining} seconds before using this command again.')
        return

    combo = get_next_combo(ROBLOX_FILE)
    if not combo:
        await ctx.reply('⚠️ No more Roblox combos available.')
        return

    if ':' not in combo:
        await ctx.reply('⚠️ Invalid combo format in Roblox file.')
        return

    username, password = combo.split(':', 1)

    embed = discord.Embed(
        title="🔐 Your Roblox Account",
        description=f"**User:** `{username}`\n**Pass:** `{password}`",
        color=discord.Color.green()
    )
    embed.set_footer(text="ACCOUNT MAY NOT WORK — https://www.roblox.com/login")

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f'✅ Roblox combo sent to {ctx.author.mention} via DM.')
        user_cooldowns[user_id] = now
    except discord.Forbidden:
        await ctx.send(f'❌ {ctx.author.mention}, I couldn’t DM you. Please enable DMs from server members.')

@bot.command(name='tiktok')
async def tiktok(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("❌ This command can only be used in the designated channel.")
        return

    user_id = ctx.author.id
    now = asyncio.get_event_loop().time()

    if user_id in user_cooldowns and now - user_cooldowns[user_id] < COOLDOWN:
        remaining = int(COOLDOWN - (now - user_cooldowns[user_id]))
        await ctx.reply(f'⏳ Please wait {remaining} seconds before using this command again.')
        return

    combo = get_next_combo(TIKTOK_FILE)
    if not combo:
        await ctx.reply('⚠️ No more TikTok combos available.')
        return

    if ':' not in combo:
        await ctx.reply('⚠️ Invalid combo format in TikTok file.')
        return

    username, password = combo.split(':', 1)

    embed = discord.Embed(
        title="🔍 TikTok Account",
        description=f"**User:** `{username}`\n**Pass:** `{password}`",
        color=discord.Color.blue()
    )
    embed.set_footer(text="ACCOUNT MAY NOT WORK — https://www.tiktok.com/login")

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f'✅ TikTok combo sent to {ctx.author.mention} via DM.')
        user_cooldowns[user_id] = now
    except discord.Forbidden:
        await ctx.send(f'❌ {ctx.author.mention}, I couldn’t DM you. Please enable DMs from server members.')

bot.run(TOKEN)

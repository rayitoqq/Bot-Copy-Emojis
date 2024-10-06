import discord
from discord.ext import commands
import aiohttp

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
@commands.has_permissions(manage_emojis=True)
async def stealemoji(ctx, emoji: discord.PartialEmoji, target_server_id: int):
    target_server = bot.get_guild(target_server_id)
    
    if not target_server:
        await ctx.send("Servidor de destino no encontrado.")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(str(emoji.url)) as response:
            if response.status != 200:
                await ctx.send("No se pudo descargar el emoji.")
                return
            emoji_data = await response.read()

    # Subir el emoji al servidor de destino
    await target_server.create_custom_emoji(name=emoji.name, image=emoji_data)
    await ctx.send(f'Emoji {emoji.name} copiado al servidor {target_server.name}.')

bot.run('Tu Token')

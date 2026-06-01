import discord
import os
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- BLOCO PARA MANTER ONLINE 24H ---
app = Flask('')
@app.route('/')
def home():
    return "Bot Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ------------------------------------

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} conectado com sucesso!')

@bot.command()
async def criar(ctx):
    guild = ctx.guild
    categoria = await guild.create_category("⚡ Servidor Automático")
    await guild.create_text_channel("💬-chat-geral", category=categoria)
    await guild.create_text_channel("📢-avisos", category=categoria)
    await guild.create_voice_channel("🔊-conversas", category=categoria)
    await ctx.send("✅ Estrutura do servidor criada com sucesso!")

# Ativa o servidor web e inicia o bot com segurança
keep_alive()
bot.run(os.environ.get('DISCORD_TOKEN'))

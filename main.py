import os
import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View
from flask import Flask
from threading import Thread

# ---------- CONFIGURAÇÃO DO SERVIDOR WEB (FLASK) ----------
app = Flask('')

@app.route('/')
def home():
    return "Bot Online 24/7 - Estruturas Massivas Prontas!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ---------- CONFIGURAÇÃO DO BOT DO DISCORD ----------
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- SISTEMA DE TICKET (BOTÃO DE SUPORTE) ----------
class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Abrir Atendimento", style=discord.ButtonStyle.blurple, custom_id="abrir_ticket_btn", emoji="🎫")
    async def button_callback(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = interaction.user
        
        cargo_suporte = discord.utils.get(guild.roles, name="🛠️ Suporte Técnico") or discord.utils.get(guild.roles, name="🔨 Moderador")
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
        }
        
        if cargo_suporte: 
            overwrites[cargo_suporte] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        nome_canal = f"🎫-{member.name}".lower()
        ticket_channel = await guild.create_text_channel(name=nome_canal, overwrites=overwrites)
        
        embed = discord.Embed(
            title="👋 Suporte Inicializado",
            description=f"Olá {member.mention}, nossa equipe de atendimento foi alertada.\n\nPara fechar o ticket, digite: `!fechar`",
            color=discord.Color.green()
        )
        await ticket_channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Ticket criado em {ticket_channel.mention}!", ephemeral=True)

# ---------- EVENTO ON_READY ----------
@bot.event
async def on_ready():
    bot.add_view(TicketView())
    print(f"[INFO] Bot {bot.user.name} está online no modo Ultra-Massivo!")

# Função auxiliar para limpar o servidor antes de recriar
async def limpar_servidor(ctx):
    await ctx.send("🧹 Limpando o servidor para aplicar a nova estrutura...")
    for channel in ctx.guild.channels:
        try: await channel.delete()
        except: pass
    for role in ctx.guild.roles:
        if role.name != "@everyone" and not role.managed:
            try: await role.delete()
            except: pass

# ---------- COMANDO 1: ULTRA NORMAL (Padrão/Amigos) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_normal(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Fundador", "🛡️ ADM", "💎 Vip", "👤 Amigos"]
    for nome_cargo in cargos: await ctx.guild.create_role(name=nome_cargo)
    
    cat_avisos = await ctx.guild.create_category("📌 ━━ ESSENCIAL ━━")
    await ctx.guild.create_text_channel("📢┃avisos", category=cat_avisos)
    await ctx.guild.create_text_channel("👋┃boas-vindas", category=cat_avisos)
    
    cat_resenha = await ctx.guild.create_category("💬 ━━ CONVERSA ━━")
    await ctx.guild.create_text_channel("💬┃chat-geral", category=cat_resenha)
    await ctx.guild.create_text_channel("🎭┃memes", category=cat_resenha)
    await ctx.guild.create_text_channel("📸┃midias-e-fotos", category=cat_resenha)
    await ctx.guild.create_text_channel("🤖┃comandos-bots", category=cat_resenha)
    
    cat_calls = await ctx.guild.create_category("🔊 ━━ CALLS ━━")
    await ctx.guild.create_voice_channel("🔊 Conversa Fiada", category=cat_calls)
    await ctx.guild.create_voice_channel("🍿 Sala de Cinema", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_calls)

# ---------- COMANDO 2: ULTRA LOJA (E-commerce/Vendas) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_loja(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Diretor", "💼 Gerente de Vendas", "🛠️ Suporte Técnico", "⭐ Cliente VIP", "🛒 Cliente"]
    for nome_cargo in cargos: await ctx.guild.create_role(name=nome_cargo)
    
    cat_institucional = await ctx.guild.create_category("🏢 ━━ INSTITUCIONAL ━━")
    await ctx.guild.create_text_channel("📢┃anúncios", category=cat_institucional)
    await ctx.guild.create_text_channel("📋┃termos-e-regras", category=cat_institucional)
    await ctx.guild.create_text_channel("🔗┃links-oficiais", category=cat_institucional)
    
    cat_vitrine = await ctx.guild.create_category("🛒 ━━ VITRINE DE PRODUTOS ━━")
    await ctx.guild.create_text_channel("💎┃produtos-vip", category=cat_vitrine)
    await ctx.guild.create_text_channel("🔥┃promoções", category=cat_vitrine)
    await ctx.guild.create_text_channel("📦┃estoque-atualizado", category=cat_vitrine)
    
    cat_confianca = await ctx.guild.create_category("✅ ━━ CONFIANÇA ━━")
    await ctx.guild.create_text_channel("💖┃avaliações", category=cat_confianca)
    await ctx.guild.create_text_channel("📈┃provas-de-entrega", category=cat_confianca)
    
    cat_suporte = await ctx.guild.create_category("🎫 ━━ ATENDIMENTO ━━")
    await ctx.guild.create_text_channel("🎫┃abrir-suporte", category=cat_suporte)
    await ctx.guild.create_text_channel("❓┃perguntas-frequentes", category=cat_suporte)

# ---------- COMANDO 3: ULTRA COMUNIDADE (Social/Grande) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_comunidade(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Dono", "🛡️ Admin", "🔨 Moderador", "💎 Membro Vip", "💬 Membro Ativo", "👤 Membro"]
    for nome_cargo in cargos: await ctx.guild.create_role(name=nome_cargo)
    
    cat_diretoria = await ctx.guild.create_category("👑 ━━ DIRETORIA (PRIVADO) ━━")
    await ctx.guild.create_text_channel("🔒┃chat-staff", category=cat_diretoria)
    await ctx.guild.create_text_channel("🤖┃logs-do-bot", category=cat_diretoria)
    
    cat_info = await ctx.guild.create_category("📌 ━━ INFORMAÇÕES ━━")
    await ctx.guild.create_text_channel("📋┃regras", category=cat_info)
    await ctx.guild.create_text_channel("📢┃avisos", category=cat_info)
    await ctx.guild.create_text_channel("🎉┃sorteios", category=cat_info)
    
    cat_welcome = await ctx.guild.create_category("👋 ━━ RECEPÇÃO ━━")
    await ctx.guild.create_text_channel("👋┃chegadas", category=cat_welcome)
    await ctx.guild.create_text_channel("🚪┃saídas", category=cat_welcome)
    
    cat_chat = await ctx.guild.create_category("💬 ━━ INTERAÇÃO GERAL ━━")
    await ctx.guild.create_text_channel("💬┃chat-geral", category=cat_chat)
    await ctx.guild.create_text_channel("🎭┃memes", category=cat_chat)
    await ctx.guild.create_text_channel("🤖┃comandos", category=cat_chat)
    
    cat_midia = await ctx.guild.create_category("📸 ━━ GALERIA MÍDIAS ━━")
    await ctx.guild.create_text_channel("📸┃mídias", category=cat_midia)
    await ctx.guild.create_text_channel("💻┃setups", category=cat_midia)
    
    cat_voz = await ctx.guild.create_category("🎙️ ━━ LOUNGES COLETIVOS ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🔊 Lounge {i:02d}", category=cat_voz)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_voz)

# ---------- COMANDO 4: ULTRA JOGOS (Gaming/FPS) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_jogos(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Dono", "🕹️ Staff Gamer", "💎 Vip Master", "🎥 Streamer", "🎮 Jogador"]
    for nome_cargo in cargos: await ctx.guild.create_role(name=nome_cargo)
    
    cat_comunidade = await ctx.guild.create_category("🎮 ━━ LOBBY GERAL ━━")
    await ctx.guild.create_text_channel("📢┃novidades", category=cat_comunidade)
    await ctx.guild.create_text_channel("💬┃chat-games", category=cat_comunidade)
    await ctx.guild.create_text_channel("🔍┃procurar-grupo", category=cat_comunidade)
    
    cat_comp = await ctx.guild.create_category("🏆 ━━ COMPETITIVO ━━")
    await ctx.guild.create_text_channel("🏆┃torneios", category=cat_comp)
    await ctx.guild.create_text_channel("📝┃inscrições", category=cat_comp)
    
    cat_fps = await ctx.guild.create_category("🔫 ━━ FPS ARENA ━━")
    await ctx.guild.create_text_channel("💣┃valorant", category=cat_fps)
    await ctx.guild.create_text_channel("🎯┃cs2", category=cat_fps)
    await ctx.guild.create_text_channel("👑┃warzone", category=cat_fps)
    
    cat_v_games = await ctx.guild.create_category("🔊 ━━ SALAS DE JOGO ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🎮 Squad {i:02d}", category=cat_v_games)

# ---------- COMANDOS AUXILIARES (TICKET) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    embed = discord.Embed(
        title="🎫 Central de Atendimento",
        description="Precisa de ajuda da nossa Staff ou quer realizar uma compra?\nClique no botão abaixo para abrir um ticket privado!",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketView())

@bot.command()
async def fechar(ctx):
    if "🎫-" in ctx.channel.name:
        await ctx.send("🔒 Fechando este ticket em 5 segundos...")
        await asyncio.sleep(5)
        await ctx.channel.delete()
    else:
        await ctx.send("❌ Este comando só pode ser usado dentro de um canal de ticket!")

# ---------- INICIALIZAÇÃO ASSÍNCRONA PARA O RENDER ----------
async def main():
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    if token is None:
        token = "SEU_TOKEN_AQUI"
    await bot.start(token)

if __name__ == "__main__":
    

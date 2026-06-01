import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from flask import Flask
from threading import Thread

# ---------- CONFIGURAÇÃO DO SERVIDOR WEB (FLASK) ----------
app = Flask('')

@app.route('/')
def home():
    return "Bot Online 24/7!"

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
        super().__init__(timeout=None) # Sem tempo limite para o botão funcionar para sempre

    @discord.ui.button(label="Abrir Ticket", style=discord.ButtonStyle.blurple, custom_id="abrir_ticket_btn", emoji="🎫")
    async def button_callback(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = interaction.user
        
        # Procura os cargos de suporte/gerente criados pelo bot
        cargo_suporte = discord.utils.get(guild.roles, name="Suporte")
        cargo_gerente = discord.utils.get(guild.roles, name="Gerente")
        
        # Configura as permissões do canal de ticket privado
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False), # Esconde de todos
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True), # Libera pro cliente
        }
        
        if cargo_suporte:
            overwrites[cargo_suporte] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        if cargo_gerente:
            overwrites[cargo_gerente] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        # Cria o canal de texto do ticket
        nome_canal = f"🎫-{member.name}".lower()
        ticket_channel = await guild.create_text_channel(name=nome_canal, overwrites=overwrites)
        
        # Envia mensagem inicial dentro do ticket
        embed = discord.Embed(
            title="👋 Atendimento Iniciado",
            description=f"Olá {member.mention}, nossa equipe já foi notificada e falará com você em breve.\n\nPara fechar este atendimento, use o comando: `!fechar`",
            color=discord.Color.green()
        )
        await ticket_channel.send(embed=embed)
        
        # Responde o clique do botão apenas para o usuário ver
        await interaction.response.send_message(f"✅ Seu ticket foi criado com sucesso em {ticket_channel.mention}!", ephemeral=True)

# ---------- EVENTO ON_READY ----------
@bot.event
async def on_ready():
    # Faz com que o botão continue funcionando mesmo se o bot reiniciar
    bot.add_view(TicketView())
    print(f"[INFO] discord.client: logging in using static token")
    print(f"[INFO] Bot {bot.user.name} está online com Sistema de Tickets!")

# Função auxiliar para limpar o servidor
async def limpar_servidor(ctx):
    await ctx.send("🧹 Limpando o servidor para aplicar o novo modelo...")
    for channel in ctx.guild.channels:
        try: await channel.delete()
        except: pass
    for role in ctx.guild.roles:
        if role.name != "@everyone" and not role.managed:
            try: await role.delete()
            except: pass

# ---------- COMANDOS ANTIGOS (COMUNIDADE, JOGOS, NORMAL) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_comunidade(ctx):
    await limpar_servidor(ctx)
    cargos = ["Dono", "Admin", "Moderador", "Membro Ativo", "Membro"]
    for nome_cargo in cargos: await ctx.guild.create_role(name=nome_cargo)
    cat_info = await ctx.guild.create_category("📌 INFORMAÇÕES")
    await ctx.guild.create_text_channel("📋-regras", category=cat_info)
    await ctx.guild.create_text_channel("📢-avisos", category=cat_info)
    await ctx.guild.create_text_channel("🎉-sorteios", category=cat_info)
    cat_chat = await ctx.guild.create_category("💬 CHAT GERAL")
    await ctx.guild.create_text_channel("💬-chat-geral", category=cat_chat)
    await ctx.guild.create_text_channel("📸-mídias", category=cat_chat)
    await ctx.guild.create_text_channel("🤖-comandos", category=cat_chat)
    cat_voz = await ctx.guild.create_category("🎙️ CALLS PÚBLICAS")
    await ctx.guild.create_voice_channel("🔊 Lounge 01", category=cat_voz)
    await ctx.guild.create_voice_channel("🔊 Lounge 02", category=cat_voz)
    await ctx.guild.create_voice_channel("🔊 Conversa Fiada", category=cat_voz)

@bot.command()
@commands.has_permissions(administrator=True)
async def criar_jogos(ctx):
    await limpar_servidor(ctx)
    cargos = ["Dono", "Staff", "Vip", "Streamer", "Jogador"]
    for nome_cargo in cargos: await ctx.guild.create_role(name=nome_cargo)
    cat_comunidade = await ctx.guild.create_category("🎮 COMUNIDADE")
    await ctx.guild.create_text_channel("📢-novidades", category=cat_comunidade)
    await ctx.guild.create_text_channel("💬-chat-games", category=cat_comunidade)
    await ctx.guild.create_text_channel("clips-e-lives", category=cat_comunidade)
    cat_squads = await ctx.guild.create_category("🔊 SQUADS (CALLS)")
    await ctx.guild.create_voice_channel("🔊 Squad Alpha (04)", category=cat_squads)
    await ctx.guild.create_voice_channel("🔊 Squad Bravo (04)", category=cat_squads)
    await ctx.guild.create_voice_channel("🔊 Duos", category=cat_squads)
    cat_comp = await ctx.guild.create_category("🏆 COMPETITIVO")
    await ctx.guild.create_text_channel("🏆-torneios", category=cat_comp)
    await ctx.guild.create_text_channel("🏅-resultados", category=cat_comp)

@bot.command()
@commands.has_permissions(administrator=True)
async def criar_normal(ctx):
    await limpar_servidor(ctx)
    cargos = ["Dono", "Staff", "Membro"]
    for nome_cargo in cargos: await ctx.guild.create_role(name=nome_cargo)
    cat_welcome = await ctx.guild.create_category("👋 BEM-VINDO")
    await ctx.guild.create_text_channel("regras", category=cat_welcome)
    await ctx.guild.create_text_channel("avisos", category=cat_welcome)
    cat_texto = await ctx.guild.create_category("💬 TEXTO")
    await ctx.guild.create_text_channel("chat-geral", category=cat_texto)
    await ctx.guild.create_text_channel("comandos", category=cat_texto)
    cat_voz = await ctx.guild.create_category("🔊 VOZ")
    await ctx.guild.create_voice_channel("Geral 1", category=cat_voz)
    await ctx.guild.create_voice_channel("Geral 2", category=cat_voz)

# ---------- COMANDO 3 COM TICKET INTEGRADO: LOJA ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_loja(ctx):
    await limpar_servidor(ctx)
    
    cargos = ["Dono", "Gerente", "Suporte", "Cliente Vip", "Cliente"]
    for nome_cargo in cargos: 
        await ctx.guild.create_role(name=nome_cargo)
        
    cat_vitrine = await ctx.guild.create_category("🛒 VITRINE")
    await ctx.guild.create_text_channel("📌-regras-da-loja", category=cat_vitrine)
    await ctx.guild.create_text_channel("💰-produtos", category=cat_vitrine)
    await ctx.guild.create_text_channel("⭐-avaliações", category=cat_vitrine)
    
    cat_atendimento = await ctx.guild.create_category("🎫 ATENDIMENTO")
    # Cria o canal de ticket normal
    canal_ticket = await ctx.guild.create_text_channel("🎫-abra-ticket", category=cat_atendimento)
    
    cat_entregas = await ctx.guild.create_category("📦 ENTREGAS")
    await ctx.guild.create_text_channel("✅-provas-de-entrega", category=cat_entregas)
    await ctx.guild.create_text_channel("📢-atualizações", category=cat_entregas)

    # Envia o Painel de Ticket Automático com botão no canal recém-criado
    embed = discord.Embed(
        title="💼 Central de Atendimento da Loja",
        description="Precisa tirar dúvidas ou comprar um produto?\nClique no botão abaixo para abrir um chat de suporte privado!",
        color=discord.Color.blue()
    )
    await canal_ticket.send(embed=embed, view=TicketView())

# ---------- COMANDO PARA FECHAR TICKET ----------
@bot.command()
@commands.has_permissions(manage_channels=True)
async def fechar(ctx):
    if ctx.channel.name.startswith("🎫-"):
        await ctx.send("🔒 Este ticket será fechado em 5 segundos...")
        import asyncio
        await asyncio.sleep(5)
        await ctx.channel.delete()
    else:
        await ctx.send("❌ Você só pode usar este comando dentro de um canal de ticket!")

# ---------- INICIALIZAÇÃO ----------
if __name__ == "__main__":
    keep_alive()
    token = os.environ.get("DISCORD_TOKEN")
    if token: bot.run(token)
    else: print("[ERRO] Variável DISCORD_TOKEN não encontrada!")

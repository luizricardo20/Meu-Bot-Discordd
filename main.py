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
    return "Bot Online 24/7 - Sistema Supremo de 12 Imperios Ativo!"

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
    print(f"[INFO] Bot {bot.user.name} online no modo Supremo de 12 Imperios!")

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

# ---------- COMANDO 1: MEGA NORMAL (Amigos) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_normal(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Fundador", "🛡️ ADM", "🔨 Moderador", "💎 Vip", "👤 Amigos"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_essencial = await ctx.guild.create_category("📌 ━━ ESSENCIAL ━━")
    await ctx.guild.create_text_channel("📢┃avisos", category=cat_essencial)
    await ctx.guild.create_text_channel("👋┃boas-vindas", category=cat_essencial)
    await ctx.guild.create_text_channel("🚪┃saidas", category=cat_essencial)
    await ctx.guild.create_text_channel("📋┃regras", category=cat_essencial)
    
    cat_resenha = await ctx.guild.create_category("💬 ━━ CONVERSA GERAL ━━")
    await ctx.guild.create_text_channel("💬┃chat-geral", category=cat_resenha)
    await ctx.guild.create_text_channel("🎭┃memes", category=cat_resenha)
    await ctx.guild.create_text_channel("📸┃midias-e-fotos", category=cat_resenha)
    await ctx.guild.create_text_channel("🎵┃recomende-musicas", category=cat_resenha)
    await ctx.guild.create_text_channel("💭┃desabafos", category=cat_resenha)
    await ctx.guild.create_text_channel("🤖┃comandos-bots", category=cat_resenha)
    
    cat_entrete = await ctx.guild.create_category("🧩 ━━ DIVERSÃO ━━")
    await ctx.guild.create_text_channel("🎰┃cassino", category=cat_entrete)
    await ctx.guild.create_text_channel("📈┃level-up", category=cat_entrete)
    await ctx.guild.create_text_channel("🎨┃artes-e-desenhos", category=cat_entrete)
    
    cat_calls = await ctx.guild.create_category("🔊 ━━ CALLS COLETIVAS ━━")
    await ctx.guild.create_voice_channel("🔊 Lounge 01", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 Lounge 02", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 Conversa Fiada", category=cat_calls)
    await ctx.guild.create_voice_channel("🍿 Sala de Cinema", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 Cantinho da Música", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_calls)
    # ---------- COMANDO 2: MEGA LOJA (Vendas) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_loja(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Diretor", "💼 Gerente de Vendas", "🛠️ Suporte Técnico", "⭐ Cliente VIP", "🛒 Cliente"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_inst = await ctx.guild.create_category("🏢 ━━ INSTITUCIONAL ━━")
    await ctx.guild.create_text_channel("📢┃anúncios", category=cat_inst)
    await ctx.guild.create_text_channel("📋┃termos-e-regras", category=cat_inst)
    await ctx.guild.create_text_channel("🔗┃links-oficiais", category=cat_inst)
    await ctx.guild.create_text_channel("🎉┃sorteios-loja", category=cat_inst)
    
    cat_vitrine = await ctx.guild.create_category("🛒 ━━ VITRINE DE PRODUTOS ━━")
    await ctx.guild.create_text_channel("💎┃produtos-vip", category=cat_vitrine)
    await ctx.guild.create_text_channel("🔥┃promoções-relampago", category=cat_vitrine)
    await ctx.guild.create_text_channel("📦┃estoque-atualizado", category=cat_vitrine)
    await ctx.guild.create_text_channel("💻┃contas-full-acesso", category=cat_vitrine)
    await ctx.guild.create_text_channel("🎁┃brindes-gratuitos", category=cat_vitrine)
    
    cat_confianca = await ctx.guild.create_category("✅ ━━ CONFIANÇA & FEEDBACK ━━")
    await ctx.guild.create_text_channel("💖┃avaliações-clientes", category=cat_confianca)
    await ctx.guild.create_text_channel("📈┃provas-de-entrega", category=cat_confianca)
    await ctx.guild.create_text_channel("🤝┃parcerias", category=cat_confianca)
    
    cat_suporte = await ctx.guild.create_category("🎫 ━━ ATENDIMENTO & AJUDA ━━")
    await ctx.guild.create_text_channel("🎫┃abrir-suporte", category=cat_suporte)
    await ctx.guild.create_text_channel("❓┃perguntas-frequentes", category=cat_suporte)
    await ctx.guild.create_text_channel("💵┃métodos-pagamento", category=cat_suporte)
    await ctx.guild.create_text_channel("🚨┃denuncias-e-reclamações", category=cat_suporte)

# ---------- COMANDO 3: MEGA COMUNIDADE (Social) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_comunidade(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Dono", "🛡️ Admin", "🔨 Moderador", "💎 Membro Vip", "💬 Membro Ativo", "👤 Membro"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_staff = await ctx.guild.create_category("👑 ━━ DIRETORIA (PRIVADO) ━━")
    await ctx.guild.create_text_channel("🔒┃chat-staff", category=cat_staff)
    await ctx.guild.create_text_channel("🚨┃alertas-e-punicoes", category=cat_staff)
    await ctx.guild.create_text_channel("🤖┃logs-do-bot", category=cat_staff)
    await ctx.guild.create_text_channel("💡┃ideias-staff", category=cat_staff)
    
    cat_info = await ctx.guild.create_category("📌 ━━ INFORMAÇÕES ━━")
    await ctx.guild.create_text_channel("📋┃regras", category=cat_info)
    await ctx.guild.create_text_channel("📢┃avisos", category=cat_info)
    await ctx.guild.create_text_channel("🎉┃sorteios", category=cat_info)
    await ctx.guild.create_text_channel("🎁┃eventos", category=cat_info)
    await ctx.guild.create_text_channel("🔗┃nossas-redes", category=cat_info)
    await ctx.guild.create_text_channel("🚀┃vantagens-booster", category=cat_info)
    
    cat_welcome = await ctx.guild.create_category("👋 ━━ RECEPÇÃO ━━")
    await ctx.guild.create_text_channel("👋┃chegadas", category=cat_welcome)
    await ctx.guild.create_text_channel("🚪┃saídas", category=cat_welcome)
    await ctx.guild.create_text_channel("🎂┃aniversários", category=cat_welcome)
    
    cat_chat = await ctx.guild.create_category("💬 ━━ INTERAÇÃO GERAL ━━")
    await ctx.guild.create_text_channel("💬┃chat-geral", category=cat_chat)
    await ctx.guild.create_text_channel("🧠┃debates", category=cat_chat)
    await ctx.guild.create_text_channel("🎭┃memes", category=cat_chat)
    await ctx.guild.create_text_channel("🤖┃comandos", category=cat_chat)
    await ctx.guild.create_text_channel("💭┃desabafos", category=cat_chat)
    
    cat_midia = await ctx.guild.create_category("📸 ━━ GALERIA MÍDIAS ━━")
    await ctx.guild.create_text_channel("📸┃mídias", category=cat_midia)
    await ctx.guild.create_text_channel("🎨┃arte-e-design", category=cat_midia)
    await ctx.guild.create_text_channel("🐱┃pets", category=cat_midia)
    await ctx.guild.create_text_channel("💻┃setups", category=cat_midia)
    
    cat_cultura = await ctx.guild.create_category("🏮 ━━ CULTURA POP ━━")
    await ctx.guild.create_text_channel("🍿┃filmes-e-séries", category=cat_cultura)
    await ctx.guild.create_text_channel("🏮┃animes-e-manga", category=cat_cultura)
    await ctx.guild.create_text_channel("🎵┃recomende-músicas", category=cat_cultura)
    
    cat_entrete = await ctx.guild.create_category("📈 ━━ ECONOMIA & GAMES ━━")
    await ctx.guild.create_text_channel("📈┃level-up", category=cat_entrete)
    await ctx.guild.create_text_channel("🎰┃cassino", category=cat_entrete)
    await ctx.guild.create_text_channel("🧩┃gincanas", category=cat_entrete)
    
    cat_voz = await ctx.guild.create_category("🎙️ ━━ LOUNGES COLETIVOS ━━")
    for i in range(1, 6): await ctx.guild.create_voice_channel(f"🔊 Lounge {i:02d}", category=cat_voz)
    await ctx.guild.create_voice_channel("🔊 Conversa Fiada", category=cat_voz)
    await ctx.guild.create_voice_channel("🔊 Cantinho da Música", category=cat_voz)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_voz)

# ---------- COMANDO 4: MEGA JOGOS (Gaming) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_jogos(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Dono", "🕹️ Staff Gamer", "💎 Vip Master", "🎥 Streamer", "🏆 Pro Player", "🎮 Jogador"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_comunidade = await ctx.guild.create_category("🎮 ━━ LOBBY GERAL ━━")
    await ctx.guild.create_text_channel("📢┃novidades", category=cat_comunidade)
    await ctx.guild.create_text_channel("💬┃chat-games", category=cat_comunidade)
    await ctx.guild.create_text_channel("🎥┃clips-e-lives", category=cat_comunidade)
    await ctx.guild.create_text_channel("🔍┃procurar-grupo", category=cat_comunidade)
    await ctx.guild.create_text_channel("🤖┃bots-games", category=cat_comunidade)
    
    cat_comp = await ctx.guild.create_category("🏆 ━━ COMPETITIVO ━━")
    await ctx.guild.create_text_channel("🏆┃torneios", category=cat_comp)
    await ctx.guild.create_text_channel("🏅┃resultados", category=cat_comp)
    await ctx.guild.create_text_channel("📝┃inscrições", category=cat_comp)
    await ctx.guild.create_text_channel("⚔️┃desafios-x1", category=cat_comp)
    await ctx.guild.create_text_channel("📋┃regras-campeonatos", category=cat_comp)
    
    cat_fps = await ctx.guild.create_category("🔫 ━━ FPS ARENA ━━")
    await ctx.guild.create_text_channel("💣┃valorant", category=cat_fps)
    await ctx.guild.create_text_channel("🎯┃cs2", category=cat_fps)
    await ctx.guild.create_text_channel("👑┃warzone", category=cat_fps)
    await ctx.guild.create_text_channel("🔥┃free-fire", category=cat_fps)
    await ctx.guild.create_text_channel("⛏️┃minecraft", category=cat_fps)
    await ctx.guild.create_text_channel("🚗┃gta-v-rp", category=cat_fps)
    
    cat_v_games = await ctx.guild.create_category("🔊 ━━ SQUADS & COMP ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🎮 Squad {i:02d}", category=cat_v_games)
    for i in range(1, 3): await ctx.guild.create_voice_channel(f"🔒 Duozinho {i:02d}", category=cat_v_games)
    await ctx.guild.create_voice_channel("📻 Rádio Gamer 24h", category=cat_v_games)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_v_games)
    # ---------- COMANDO 5: MEGA STREAMER (Criadores de Conteúdo) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_streamer(ctx):
    await limpar_servidor(ctx)
    cargos = ["🎥 Streamer", "🛠️ Moderador da Live", "💎 Sub Lendário", "💖 Subscriber (Sub)", "👤 Espectador"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_mural = await ctx.guild.create_category("📺 ━━ MURAL DA LIVE ━━")
    await ctx.guild.create_text_channel("🚨┃lives-on", category=cat_mural)
    await ctx.guild.create_text_channel("🎬┃videos-novos", category=cat_mural)
    await ctx.guild.create_text_channel("📅┃agenda-e-horarios", category=cat_mural)
    await ctx.guild.create_text_channel("📢┃avisos-gerais", category=cat_mural)
    
    cat_chat = await ctx.guild.create_category("💬 ━━ BATE PAPO ━━")
    await ctx.guild.create_text_channel("💬┃chat-da-comunidade", category=cat_chat)
    await ctx.guild.create_text_channel("🎭┃memes-da-live", category=cat_chat)
    await ctx.guild.create_text_channel("🤖┃comandos-bots", category=cat_chat)
    await ctx.guild.create_text_channel("🍿┃clips-da-live", category=cat_chat)
    
    cat_vip = await ctx.guild.create_category("💎 ━━ AREA DOS SUBS ━━")
    await ctx.guild.create_text_channel("💬┃sub-exclusive", category=cat_vip)
    await ctx.guild.create_text_channel("🔊┃call-dos-subs", category=cat_vip)
    await ctx.guild.create_text_channel("🎮┃jogar-com-streamer", category=cat_vip)
    
    cat_sugestao = await ctx.guild.create_category("💡 ━━ INTERAÇÃO ━━")
    await ctx.guild.create_text_channel("💡┃ideias-de-videos", category=cat_sugestao)
    await ctx.guild.create_text_channel("🎵┃sugestoes-musicas", category=cat_sugestao)
    await ctx.guild.create_text_channel("🎨┃fanarts-e-desenhos", category=cat_sugestao)
    
    cat_calls = await ctx.guild.create_category("🎙️ ━━ LIVE INTERACTION ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🔊 Jogando com Inscritos {i:02d}", category=cat_calls)
    await ctx.guild.create_voice_channel("🔒 Sala de Gravação", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_calls)

# ---------- COMANDO 6: MEGA DESENHO (Artes/Ilustração) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_desenho(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Mestre Supremo", "🖌️ Ilustrador Pro", "🎨 Desenhista", "📐 Aprendiz", "👤 Admirador"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_mural = await ctx.guild.create_category("📌 ━━ QUADRO DE AVISOS ━━")
    await ctx.guild.create_text_channel("📢┃avisos-e-eventos", category=cat_mural)
    await ctx.guild.create_text_channel("🏆┃desafios-de-desenho", category=cat_mural)
    
    cat_galeria = await ctx.guild.create_category("🎨 ━━ MEU PORTFÓLIO ━━")
    await ctx.guild.create_text_channel("🖼️┃galeria-de-artes", category=cat_galeria)
    await ctx.guild.create_text_channel("💻┃arte-digital", category=cat_galeria)
    await ctx.guild.create_text_channel("📝┃desenho-tradicional", category=cat_galeria)
    await ctx.guild.create_text_channel("✏️┃esboços-e-sketches", category=cat_galeria)
    
    cat_vendas = await ctx.guild.create_category("💼 ━━ COMISSÕES & VENDAS ━━")
    await ctx.guild.create_text_channel("🛒┃tabela-de-preços", category=cat_vendas)
    await ctx.guild.create_text_channel("🤝┃encomendas-abertas", category=cat_vendas)
    await ctx.guild.create_text_channel("✅┃clientes-satisfeitos", category=cat_vendas)
    
    cat_feed = await ctx.guild.create_category("💬 ━━ CONVERSA INTERAÇÃO ━━")
    await ctx.guild.create_text_channel("💬┃chat-artistas", category=cat_feed)
    await ctx.guild.create_text_channel("🔎┃criticas-e-feedback", category=cat_feed)
    await ctx.guild.create_text_channel("🎬┃tutoriais-e-dicas", category=cat_feed)
    await ctx.guild.create_text_channel("🎨┃colabs-e-parcerias", category=cat_feed)
    
    cat_calls = await ctx.guild.create_category("🎙️ ━━ CHAT DE VOZ ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🔊 Desenhe Comigo {i:02d}", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 Compartilhando Tela", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_calls)

# ---------- COMANDO 7: MEGA MARKETING (Dropshipping/PLR) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_marketing(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Infoprodutor Tubarão", "🚀 Trafego Pago VIP", "💼 Copywriter", "🛒 Dropper", "👤 Afiliado"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_mural = await ctx.guild.create_category("🎯 ━━ QUADRO GERAL ━━")
    await ctx.guild.create_text_channel("📢┃anuncios-e-insights", category=cat_mural)
    await ctx.guild.create_text_channel("📈┃escala-e-vendas", category=cat_mural)
    await ctx.guild.create_text_channel("📌┃regras-networking", category=cat_mural)
    
    cat_funil = await ctx.guild.create_category("🚀 ━━ FUNIL & COPY ━━")
    await ctx.guild.create_text_channel("💻┃trafego-pago-ads", category=cat_funil)
    await ctx.guild.create_text_channel("✍️┃copywriting-e-vsl", category=cat_funil)
    await ctx.guild.create_text_channel("📦┃dropshipping-e-plr", category=cat_funil)
    await ctx.guild.create_text_channel("🛠️┃ferramentas-uteis", category=cat_funil)
    
    cat_net = await ctx.guild.create_category("💬 ━━ NETWORKING ━━")
    await ctx.guild.create_text_channel("🤝┃achar-socios", category=cat_net)
    await ctx.guild.create_text_channel("💬┃chat-marketing", category=cat_net)
    await ctx.guild.create_text_channel("🏆┃resultados-diarios", category=cat_net)
    await ctx.guild.create_text_channel("🤖┃bots-e-automacoes", category=cat_net)
    
    cat_vip = await ctx.guild.create_category("👑 ━━ AREA PREMIUM VIP ━━")
    await ctx.guild.create_text_channel("🔒┃estrategias-secretas", category=cat_vip)
    await ctx.guild.create_text_channel("📈┃call-de-mentoria", category=cat_vip)
    
    cat_calls = await ctx.guild.create_category("🎙️ ━━ MASTERMIND CALLS ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🔊 Mastermind Geral {i:02d}", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 Call de Network", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_calls)

# ---------- COMANDO 8: MEGA DESIGN (Edição Visual) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_design(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Art Director", "🎬 Master Editor", "🎨 Designer", "📐 Freelancer", "👤 Aprendiz"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_av = await ctx.guild.create_category("📌 ━━ COMUNIDADE ART ━━")
    await ctx.guild.create_text_channel("📢┃anuncios-design", category=cat_av)
    await ctx.guild.create_text_channel("🏆┃batalhas-de-artes", category=cat_av)
    
    cat_mural = await ctx.guild.create_category("📸 ━━ SHOWROOM ━━")
    await ctx.guild.create_text_channel("🎨┃portfolios-membros", category=cat_mural)
    await ctx.guild.create_text_channel("📦┃packs-e-recursos", category=cat_mural)
    await ctx.guild.create_text_channel("🎬┃luts-e-presets", category=cat_mural)
    await ctx.guild.create_text_channel("🔤┃fontes-e-overlays", category=cat_mural)
    
    cat_trabalho = await ctx.guild.create_category("💼 ━━ MERCADO DESIGN ━━")
    await ctx.guild.create_text_channel("🛒┃encomendas-e-vendas", category=cat_trabalho)
    await ctx.guild.create_text_channel("🎯┃vagas-freelancer", category=cat_trabalho)
    await ctx.guild.create_text_channel("💳┃tabela-valores", category=cat_trabalho)
    
    cat_feed = await ctx.guild.create_category("💬 ━━ INTERAÇÃO ARTÍSTICA ━━")
    await ctx.guild.create_text_channel("💬┃chat-designers", category=cat_feed)
    await ctx.guild.create_text_channel("🔎┃critica-e-feedback", category=cat_feed)
    await ctx.guild.create_text_channel("💻┃setups-designers", category=cat_feed)
    
    cat_calls = await ctx.guild.create_category("🎙️ ━━ CREATIVE ROOMS ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🔊 Call Co-Working {i:02d}", category=cat_calls)
    await ctx.guild.create_voice_channel("🎬 Compartilhando Tela", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_calls)
    # ---------- COMANDO 9: MEGA TECNOLOGIA (Hardware/Setups) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_tecnologia(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Tech Guru", "🔌 Hardware Enthusiast", "💻 Pc Gamer", "📱 Mobile User", "👤 Novato"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_av = await ctx.guild.create_category("📌 ━━ QUADRO CENTRAL ━━")
    await ctx.guild.create_text_channel("📢┃avisos-tech", category=cat_av)
    await ctx.guild.create_text_channel("📰┃noticias-tecnologia", category=cat_av)
    
    cat_ofertas = await ctx.guild.create_category("🛒 ━━ MERCADO TECH ━━")
    await ctx.guild.create_text_channel("🔥┃promoções-do-dia", category=cat_ofertas)
    await ctx.guild.create_text_channel("💻┃setups-dos-membros", category=cat_ofertas)
    await ctx.guild.create_text_channel("⚙️┃perifericos-indicados", category=cat_ofertas)
    
    cat_suporte = await ctx.guild.create_category("🔧 ━━ SUPORTE & HARDWARE ━━")
    await ctx.guild.create_text_channel("🛠️┃ajuda-montar-pc", category=cat_suporte)
    await ctx.guild.create_text_channel("🚨┃resolvendo-problemas", category=cat_suporte)
    await ctx.guild.create_text_channel("🔵┃erros-e-tela-azul", category=cat_suporte)
    await ctx.guild.create_text_channel("💾┃drivers-e-bios", category=cat_suporte)
    
    cat_chat = await ctx.guild.create_category("💬 ━━ DISCUSSÕES ━━")
    await ctx.guild.create_text_channel("💬┃chat-tecnologia", category=cat_chat)
    await ctx.guild.create_text_channel("🎮┃consoles-e-games", category=cat_chat)
    await ctx.guild.create_text_channel("🍏┃ios-vs-android", category=cat_chat)
    
    cat_calls = await ctx.guild.create_category("🎙️ ━━ TECH VOICE ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🔊 Bancada de Testes {i:02d}", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 Assistência Remota", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_calls)

# ---------- COMANDO 10: MEGA CINEMA (Filmes/Séries) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_cinema(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Diretor de Cinema", "🍿 Crítico de TV", "🎬 Cinéfilo VIP", "📺 Maratoneiro", "👤 Espectador"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_av = await ctx.guild.create_category("📌 ━━ ESSENCIAL ━━")
    await ctx.guild.create_text_channel("📢┃avisos-cinema", category=cat_av)
    await ctx.guild.create_text_channel("🎉┃noite-de-estreia", category=cat_av)
    
    cat_mural = await ctx.guild.create_category("🍿 ━━ CARTAZ DO DIA ━━")
    await ctx.guild.create_text_channel("🎬┃trailers-e-novidades

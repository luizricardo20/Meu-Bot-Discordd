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
    return "Bot Online 24/7 - Imperio Supremo de 12 Modos Ativo!"

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
    print(f"[INFO] Bot {bot.user.name} online no modo Imperador de 12 Estruturas!")

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
                # ---------- COMANDO 1: ULTRA NORMAL (Amigos) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_normal(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Fundador", "🛡️ ADM", "🔨 Moderador", "💎 Vip", "👤 Amigos"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    c1 = await ctx.guild.create_category("📌 ━━ ESSENCIAL ━━")
    for ch in ["📢┃avisos", "📋┃regras", "🔗┃links-uteis", "📌┃diretrizes"]: await ctx.guild.create_text_channel(ch, category=c1)
    
    c2 = await ctx.guild.create_category("👋 ━━ RECEPÇÃO ━━")
    for ch in ["👋┃boas-vindas", "🚪┃saidas", "🎂┃aniversarios"]: await ctx.guild.create_text_channel(ch, category=c2)
    
    c3 = await ctx.guild.create_category("💬 ━━ CONVERSA GERAL ━━")
    for ch in ["💬┃chat-geral", "🎭┃memes", "📸┃midias-e-fotos", "💭┃desabafos", "🧠┃debates", "🔮┃filosofia"]: await ctx.guild.create_text_channel(ch, category=c3)
    
    c4 = await ctx.guild.create_category("🧩 ━━ DIVERSÃO & BOTS ━━")
    for ch in ["🎰┃cassino", "📈┃level-up", "🤖┃comandos-bots", "🎮┃minigames"]: await ctx.guild.create_text_channel(ch, category=c4)
    
    c5 = await ctx.guild.create_category("📸 ━━ GALERIA SOCIAL ━━")
    for ch in ["🐱┃pets-e-animais", "💻┃setups-membros", "🍔┃culinaria-fotos"]: await ctx.guild.create_text_channel(ch, category=c5)
    
    c6 = await ctx.guild.create_category("🔊 ━━ CALLS COLETIVAS ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🔊 Lounge {i:02d}", category=c6)
    await ctx.guild.create_voice_channel("🔊 Conversa Fiada", category=c6)
    await ctx.guild.create_voice_channel("🍿 Sala de Cinema", category=c6)
    await ctx.guild.create_voice_channel("🔊 Cantinho da Música", category=c6)
    
    c7 = await ctx.guild.create_category("🔒 ━━ CALLS PRIVADAS ━━")
    for i in range(1, 3): await ctx.guild.create_voice_channel(f"🔒 Duozinho {i:02d}", category=c7)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=c7)

# ---------- COMANDO 2: ULTRA LOJA (Vendas) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_loja(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Diretor", "💼 Gerente de Vendas", "🛠️ Suporte Técnico", "⭐ Cliente VIP", "🛒 Cliente"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    c1 = await ctx.guild.create_category("🏢 ━━ INSTITUCIONAL ━━")
    for ch in ["📢┃anúncios", "📋┃termos-e-regras", "🔗┃links-oficiais", "📢┃avisos-importantes"]: await ctx.guild.create_text_channel(ch, category=c1)
    
    c2 = await ctx.guild.create_category("🛒 ━━ VITRINE DE PRODUTOS ━━")
    for ch in ["💎┃produtos-vip", "🔥┃promoções-relampago", "📦┃estoque-atualizado", "💻┃contas-full-acesso", "🎁┃brindes-gratuitos"]: await ctx.guild.create_text_channel(ch, category=c2)
    
    c3 = await ctx.guild.create_category("✅ ━━ CONFIANÇA & FEEDBACK ━━")
    for ch in ["💖┃avaliações-clientes", "📈┃provas-de-entrega", "🤝┃parcerias", "📊┃nossos-numeros"]: await ctx.guild.create_text_channel(ch, category=c3)
    
    c4 = await ctx.guild.create_category("🎫 ━━ ATENDIMENTO & AJUDA ━━")
    for ch in ["🎫┃abrir-suporte", "❓┃perguntas-frequentes", "💵┃métodos-pagamento", "🚨┃denuncias-reclamações"]: await ctx.guild.create_text_channel(ch, category=c4)
    
    c5 = await ctx.guild.create_category("🎉 ━━ MARKETING & EVENTOS ━━")
    for ch in ["🎉┃sorteios-loja", "🎁┃eventos-comunidade", "🚀┃boost-vantagens"]: await ctx.guild.create_text_channel(ch, category=c5)
    
    c6 = await ctx.guild.create_category("💬 ━━ CHAT DE CLIENTES ━━")
    for ch in ["💬┃chat-geral", "🤖┃comandos-bots", "📸┃mídias-clientes"]: await ctx.guild.create_text_channel(ch, category=c6)
    
    c7 = await ctx.guild.create_category("🎙️ ━━ REUNIÕES & SUPORTE ━━")
    await ctx.guild.create_voice_channel("🔊 Suporte Via Voz 01", category=c7)
    await ctx.guild.create_voice_channel("🔊 Suporte Via Voz 02", category=c7)
    await ctx.guild.create_voice_channel("💼 Reunião de Vendas", category=c7)
    await ctx.guild.create_voice_channel("🔊 Sala de Espera", category=c7)
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
    await ctx.guild.create_text_channel("📈┃call-de-mentoria", category=vip) if 'vip' in locals() else await ctx.guild.create_text_channel("📈┃call-de-mentoria", category=cat_vip)
    
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
    await ctx.guild.create_text_channel("🎬┃trailers-e-novidades", category=cat_mural)
    await ctx.guild.create_text_channel("📰┃noticias-da-critica", category=cat_mural)
    await ctx.guild.create_text_channel("🗓️┃calendario-lançamentos", category=cat_mural)
    
    cat_resenha = await ctx.guild.create_category("💬 ━━ SALAS DE DEBATE ━━")
    await ctx.guild.create_text_channel("💬┃papo-de-cinema", category=cat_resenha)
    await ctx.guild.create_text_channel("🚨┃chat-com-spoiler", category=cat_resenha)
    await ctx.guild.create_text_channel("🤫┃chat-sem-spoiler", category=cat_resenha)
    await ctx.guild.create_text_channel("🧠┃teorias-e-finais", category=cat_resenha)
    await ctx.guild.create_text_channel("📺┃series-e-desenhos", category=cat_resenha)
    
    cat_indicacao = await ctx.guild.create_category("⭐ ━━ RECOMENDAÇÕES ━━")
    await ctx.guild.create_text_channel("💖┃filmes-favoritos", category=cat_indicacao)
    await ctx.guild.create_text_channel("💀┃terror-e-suspense", category=cat_indicacao)
    await ctx.guild.create_text_channel("🤖┃ficção-e-herois", category=cat_indicacao)
    
    cat_calls = await ctx.guild.create_category("🎙️ ━━ AUDITÓRIOS ━━")
        await ctx.guild.create_voice_channel("🍿 Cine Pipoca 01", category=cat_calls)
    await ctx.guild.create_voice_channel("🍿 Cine Pipoca 02", category=cat_calls)
    await ctx.guild.create_voice_channel("📺 Maratona de Séries", category=cat_calls)
    await ctx.guild.create_voice_channel("📻 Rádio Cinema 24h", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Inativo)", category=cat_calls)

# ---------- COMANDO 11: MEGA ANIME (Cultura Otaku) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_anime(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Hokage Mestre", "⛩️ Otaku Lendário", "🔮 Mangaká VIP", "🏮 Cosplayer Profissional", "🌸 Membro Otaku", "👤 Civil"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_mural = await ctx.guild.create_category("⛩️ ━━ QUADRO DE AVISOS ━━")
    await ctx.guild.create_text_channel("📢┃lançamentos-da-semana", category=cat_mural)
    await ctx.guild.create_text_channel("📌┃noticias-otaku", category=cat_mural)
    await ctx.guild.create_text_channel("🌸┃cantinho-cosplay", category=cat_mural)
    await ctx.guild.create_text_channel("🎨┃fanarts-da-comunidade", category=cat_mural)
    
    cat_conversas = await ctx.guild.create_category("💬 ━━ ALDEIA PRINCIPAL ━━")
    await ctx.guild.create_text_channel("💬┃chat-otaku", category=cat_conversas)
    await ctx.guild.create_text_channel("🤖┃comandos-bots", category=cat_conversas)
    await ctx.guild.create_text_channel("🔮┃recomendações-animes", category=cat_conversas)
    await ctx.guild.create_text_channel("📖┃mangas-e-webtoons", category=cat_conversas)
    await ctx.guild.create_text_channel("🎭┃memes-otaku", category=cat_conversas)
    
    cat_spoiler = await ctx.guild.create_category("🚨 ━━ SPOILER ZONE ━━")
    await ctx.guild.create_text_channel("💥┃mangas-capitulo-novo", category=cat_spoiler)
    await ctx.guild.create_text_channel("🎬┃episodio-da-semana", category=cat_spoiler)
    await ctx.guild.create_text_channel("🧠┃teorias-e-debates", category=cat_spoiler)
    
    cat_jogos = await ctx.guild.create_category("🎮 ━━ JOGOS ANIME ━━")
    await ctx.guild.create_text_channel("🃏┃genshin-e-honkai", category=cat_jogos)
    await ctx.guild.create_text_channel("⚔️┃anime-fighting-games", category=cat_jogos)
    await ctx.guild.create_text_channel("🤖┃mudae-e-minigames", category=cat_jogos)
    
    cat_calls = await ctx.guild.create_category("🎙️ ━━ LOUNGES JAPÃO ━━")
    for i in range(1, 4): await ctx.guild.create_voice_channel(f"🔊 Distrito Kawaii {i:02d}", category=cat_calls)
    await ctx.guild.create_voice_channel("🎵 Anime Openings (Música)", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Dormindo)", category=cat_calls)

# ---------- COMANDO 12: MEGA RPG (Guildas/Mesas) ----------
@bot.command()
@commands.has_permissions(administrator=True)
async def criar_rpg(ctx):
    await limpar_servidor(ctx)
    cargos = ["👑 Mestre Lendário", "🛡️ Paladino Veterano", "🔮 Mago Supremo", "🏹 Arqueiro", "🗡️ Ladino", "👤 Aventureiro"]
    for nc in cargos: await ctx.guild.create_role(name=nc)
    
    cat_mural = await ctx.guild.create_category("📜 ━━ MURAL DO REINO ━━")
    await ctx.guild.create_text_channel("📢┃anuncios-e-quests", category=cat_mural)
    await ctx.guild.create_text_channel("📋┃sistemas-e-regras", category=cat_mural)
    await ctx.guild.create_text_channel("📖┃historias-do-mundo", category=cat_mural)
    await ctx.guild.create_text_channel("🗺️┃mapas-e-cenarios", category=cat_mural)
    
    cat_aventura = await ctx.guild.create_category("🛡️ ━━ TAVERNA PRINCIPAL ━━")
    await ctx.guild.create_text_channel("💬┃chat-taverna", category=cat_aventura)
    await ctx.guild.create_text_channel("🎲┃fichas-e-dados", category=cat_aventura)
    await ctx.guild.create_text_channel("🎭┃memes-rpg", category=cat_aventura)
    await ctx.guild.create_text_channel("🤖┃bots-de-dados", category=cat_aventura)
    
    cat_mestre = await ctx.guild.create_category("🔒 ━━ CONSELHO DOS MESTRES ━━")
    await ctx.guild.create_text_channel("🔒┃chat-dos-mestres", category=cat_mestre)
    await ctx.guild.create_text_channel("💡┃ideias-de-campanhas", category=cat_mestre)
    await ctx.guild.create_text_channel("📦┃recursos-e-tokens", category=cat_mestre)
    
    cat_recruta = await ctx.guild.create_category("🔍 ━━ RECRUTAMENTO ━━")
    await ctx.guild.create_text_channel("🤝┃procuro-mesa", category=cat_recruta)
    await ctx.guild.create_text_channel("📜┃procuro-jogadores", category=cat_recruta)
    
    cat_calls = await ctx.guild.create_category("🎙️ ━━ MESAS DE ÁUDIO ━━")
    for i in range(1, 5): await ctx.guild.create_voice_channel(f"🎲 Mesa de RPG {i:02d}", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 Resenha pós-Sessão", category=cat_calls)
    await ctx.guild.create_voice_channel("🔊 💤 AFK (Desmaiado)", category=cat_calls)

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

# ---------- INICIALIZAÇÃO DIRETA PARA O RENDER ----------
async def main():
    keep_alive()
    token_secreto = os.getenv("DISCORD_TOKEN", "SEM_TOKEN")
    await bot.start(token_secreto)

if __name__ == "__main__":
    asyncio.run(main())

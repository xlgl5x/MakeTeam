# Importação de bibliotecas necessárias
from dotenv import load_dotenv  # Carrega variáveis de ambiente de um arquivo .env
import os  # Para acessar variáveis de ambiente do sistema
import random  # Para embaralhar a lista de jogadores
import discord  # Biblioteca principal do Discord
from discord.ext import commands  # Extensão para comandos personalizados

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Token do bot salvo em .env

# Define os intents para o bot (necessário para ler membros dos canais de voz)
intents = discord.Intents.all()
intents.members = True

# Inicializa o bot com prefixo "!" e intents definidos
client = commands.Bot(command_prefix="!", intents=intents)


# Evento disparado quando o bot está online
@client.event
async def on_ready():
    print("Bot MakeTeam está online!")


# Evento para capturar erros de comandos
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "Comando não encontrado. Use !comandos para ver a lista de comandos disponíveis."
        )
        await comandos(ctx)
    else:
        raise error


# Comando principal para criar os times
@client.command()
async def make(ctx, mix_type):
    # Define os canais de acordo com o tipo de mix
    if mix_type == "mix1":
        voice_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 1] - LOBBY"
        )
        team_1_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 1] - EQUIPE 1"
        )
        team_2_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 1] - EQUIPE 2"
        )
    elif mix_type == "mix2":
        voice_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 2] - LOBBY"
        )
        team_1_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 2] - EQUIPE 1"
        )
        team_2_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 2] - EQUIPE 2"
        )
    elif mix_type == "channels":
        await make_canais(ctx)
        return
    else:
        await ctx.send(
            "Comando inválido. Use !comandos para ver a lista de comandos disponíveis."
        )
        await comandos(ctx)
        return

    # Validação do canal principal
    if not voice_channel:
        await ctx.send(f'Canal de voz "{mix_type.upper()} - LOBBY" não encontrado')
        return

    # Lista os membros no canal de voz, ignorando bots
    members = [member for member in voice_channel.members if not member.bot]

    if len(members) < 2:
        await ctx.send(
            f'O canal "{mix_type.upper()} - LOBBY" precisa ter pelo menos 2 membros (excluindo bots) para formar equipes.'
        )
        return

    # Embaralha os membros e divide em dois times
    random.shuffle(members)
    team_1 = members[: len(members) // 2]
    team_2 = members[len(members) // 2 :]
    queue = []

    # Limita os times a 5 jogadores e coloca o restante na fila
    if len(team_1) > 5:
        queue.extend(team_1[5:])
        team_1 = team_1[:5]
    if len(team_2) > 5:
        queue.extend(team_2[5:])
        team_2 = team_2[:5]

    # Cria as strings com as menções
    team_1_mention = " ".join(member.mention for member in team_1)
    team_2_mention = " ".join(member.mention for member in team_2)
    queue_mention = " ".join(member.mention for member in queue)

    # Envia os times no chat
    await ctx.send(f"[MIX 1] - EQUIPE 1: {team_1_mention}")
    await ctx.send(f"[MIX 1] - EQUIPE 2: {team_2_mention}")
    if queue:
        await ctx.send(f"FILA DE ESPERA: {queue_mention}")

    # Valida os canais e move os membros
    if not team_1_channel or not team_2_channel:
        await ctx.send(
            f'Canal de voz "[MIX 1] - EQUIPE 1" ou "[MIX 1] - EQUIPE 2" não encontrado'
        )
        return

    for member in team_1:
        await member.move_to(team_1_channel)
    for member in team_2:
        await member.move_to(team_2_channel)

    # Move a fila, se necessário
    if queue:
        queue_channel = discord.utils.get(
            ctx.guild.voice_channels, name="FILA DE ESPERA"
        )
        if not queue_channel:
            await ctx.send('Canal de voz "FILA DE ESPERA" não encontrado')
            return
        for member in queue:
            await member.move_to(queue_channel)


# Comando para mover membros de volta ao lobby
@client.command()
async def move(ctx, mix_type):
    if mix_type == "mix1":
        team_1_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 1] - EQUIPE 1"
        )
        team_2_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 1] - EQUIPE 2"
        )
        mix_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 1] - LOBBY"
        )
    elif mix_type == "mix2":
        team_1_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 2] - EQUIPE 1"
        )
        team_2_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 2] - EQUIPE 2"
        )
        mix_channel = discord.utils.get(
            ctx.guild.voice_channels, name="[MIX 2] - LOBBY"
        )
    else:
        await ctx.send(
            "Comando inválido. Use !comandos para ver a lista de comandos disponíveis."
        )
        await comandos(ctx)
        return

    # Valida canais e move os membros
    if not mix_channel or not team_1_channel or not team_2_channel:
        await ctx.send("Canais de voz não encontrados.")
        return

    for member in team_1_channel.members + team_2_channel.members:
        if not member.bot:
            await member.move_to(mix_channel)

    await ctx.send(
        f'Todos os membros das equipes foram movidos para o canal "{mix_channel}".'
    )


# Comando que mostra a lista de comandos disponíveis
@client.command()
async def comandos(ctx):
    embed = discord.Embed(
        title="Comandos Disponíveis",
        description="Lista de comandos do bot",
        color=0x00FF00,
    )
    embed.add_field(
        name="!make mix1", value="Cria equipes no canal [MIX 1] - LOBBY", inline=False
    )
    embed.add_field(
        name="!make mix2", value="Cria equipes no canal [MIX 2] - LOBBY", inline=False
    )
    embed.add_field(
        name="!make channels", value="Cria ou atualiza os canais de voz dentro da categoria CS2 - Somente Admins", inline=False,
    )
    embed.add_field(
        name="!move mix1", value="Move todos para o lobby do MIX 1", inline=False
    )
    embed.add_field(
        name="!move mix2", value="Move todos para o lobby do MIX 2", inline=False
    )
    embed.add_field(
        name="!remove channels",
        value='Remove os canais e a categoria "Counter-Strike 2" - Somente Admins',
        inline=False,
    )
    embed.set_footer(text="MakeTeam v3.0.0 © 2023-2025 - by lgl5")
    await ctx.send(embed=embed)


# Comando único que cria a categoria e os canais necessários, renomeando os antigos se preciso
@client.command()
async def make_canais(ctx):
    # Verifica se o autor do comando tem permissão de administrador
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Você não tem permissão para executar este comando.")
        return

    guild = ctx.guild

    # Verifica se a categoria "Counter-Strike 2" já existe. Caso não, cria.
    category = discord.utils.get(guild.categories, name="Counter-Strike 2")
    if not category:
        category = await guild.create_category("Counter-Strike 2")
        await ctx.send('Categoria "Counter-Strike 2" criada.')

    # Mapeia nomes antigos para o novo padrão
    canais_renomear = {
        "MIX 1": "[MIX 1] - LOBBY",
        "EQUIPE 1": "[MIX 1] - EQUIPE 1",
        "EQUIPE 2": "[MIX 1] - EQUIPE 2",
        "MIX 2": "[MIX 2] - LOBBY",
        "TIME 1": "[MIX 2] - EQUIPE 1",
        "TIME 2": "[MIX 2] - EQUIPE 2",
    }

    # Renomeia canais antigos e move para a categoria correta
    for antigo, novo in canais_renomear.items():
        canal_antigo = discord.utils.get(guild.voice_channels, name=antigo)
        if canal_antigo:
            await canal_antigo.edit(name=novo, category=category)
            await ctx.send(
                f'Canal "{antigo}" renomeado para "{novo}" e movido para a categoria "Counter-Strike 2".'
            )

    # Lista de canais obrigatórios
    canais_necessarios = [
        "[MIX 1] - LOBBY",
        "[MIX 1] - EQUIPE 1",
        "[MIX 1] - EQUIPE 2",
        "FILA DE ESPERA",
        "[MIX 2] - LOBBY",
        "[MIX 2] - EQUIPE 1",
        "[MIX 2] - EQUIPE 2",
    ]

    # Verifica se cada canal existe e move ou cria se necessário
    for nome in canais_necessarios:
        canal = discord.utils.get(guild.voice_channels, name=nome)
        if canal:
            # Se já existe, move para a categoria se estiver fora
            if canal.category != category:
                await canal.edit(category=category)
                await ctx.send(
                    f'Canal "{nome}" movido para a categoria "Counter-Strike 2".'
                )
        else:
            # Cria canal se não existir
            await guild.create_voice_channel(nome, category=category)
            await ctx.send(
                f'Canal de voz "{nome}" criado na categoria "Counter-Strike 2".'
            )

    guild = ctx.guild

    # Verifica se a categoria "Counter-Strike 2" já existe. Caso não, cria.
    category = discord.utils.get(guild.categories, name="Counter-Strike 2")
    if not category:
        category = await guild.create_category("Counter-Strike 2")
        await ctx.send('Categoria "Counter-Strike 2" criada.')

    # Mapeia nomes antigos para o novo padrão
    canais_renomear = {
        "MIX 1": "[MIX 1] - LOBBY",
        "EQUIPE 1": "[MIX 1] - EQUIPE 1",
        "EQUIPE 2": "[MIX 1] - EQUIPE 2",
        "MIX 2": "[MIX 2] - LOBBY",
        "TIME 1": "[MIX 2] - EQUIPE 1",
        "TIME 2": "[MIX 2] - EQUIPE 2",
    }

    # Renomeia canais antigos e move para a categoria correta
    for antigo, novo in canais_renomear.items():
        canal_antigo = discord.utils.get(guild.voice_channels, name=antigo)
        if canal_antigo:
            await canal_antigo.edit(name=novo, category=category)
            await ctx.send(
                f'Canal "{antigo}" renomeado para "{novo}" e movido para a categoria "Counter-Strike 2".'
            )

    # Lista de canais obrigatórios
    canais_necessarios = [
        "[MIX 1] - LOBBY",
        "[MIX 1] - EQUIPE 1",
        "[MIX 1] - EQUIPE 2",
        "FILA DE ESPERA",
        "[MIX 2] - LOBBY",
        "[MIX 2] - EQUIPE 1",
        "[MIX 2] - EQUIPE 2",
    ]

    # Verifica se cada canal existe, e cria se não existir
    for nome in canais_necessarios:
        canal = discord.utils.get(guild.voice_channels, name=nome)
        if canal:
            # Move canal existente para a categoria correta, se necessário
            if canal.category != category:
                await canal.edit(category=category)
                await ctx.send(
                    f'Canal "{nome}" movido para a categoria "Counter-Strike 2".'
                )
        else:
            # Cria canal se não existir
            await guild.create_voice_channel(nome, category=category)
            await ctx.send(
                f'Canal de voz "{nome}" criado na categoria "Counter-Strike 2".'
            )

    guild = ctx.guild

    # Verifica se a categoria "Counter-Strike 2" já existe. Caso não, cria.
    category = discord.utils.get(guild.categories, name="Counter-Strike 2")
    if not category:
        category = await guild.create_category("Counter-Strike 2")
        await ctx.send('Categoria "Counter-Strike 2" criada.')

    # Mapeia nomes antigos para o novo padrão
    canais_renomear = {
        "MIX 1": "[MIX 1] - LOBBY",
        "EQUIPE 1": "[MIX 1] - EQUIPE 1",
        "EQUIPE 2": "[MIX 1] - EQUIPE 2",
        "MIX 2": "[MIX 2] - LOBBY",
        "TIME 1": "[MIX 2] - EQUIPE 1",
        "TIME 2": "[MIX 2] - EQUIPE 2",
    }

    for antigo, novo in canais_renomear.items():
        canal_antigo = discord.utils.get(guild.voice_channels, name=antigo)
        if canal_antigo:
            await canal_antigo.edit(name=novo, category=category)
            await ctx.send(f'Canal "{antigo}" renomeado para "{novo}".')

    # Lista de canais obrigatórios
    canais_necessarios = [
        "[MIX 1] - LOBBY",
        "[MIX 1] - EQUIPE 1",
        "[MIX 1] - EQUIPE 2",
        "FILA DE ESPERA",
        "[MIX 2] - LOBBY",
        "[MIX 2] - EQUIPE 1",
        "[MIX 2] - EQUIPE 2",
    ]

    # Verifica e cria os canais que ainda não existem
    for nome in canais_necessarios:
        existente = discord.utils.get(guild.voice_channels, name=nome)
        if not existente:
            await guild.create_voice_channel(nome, category=category)
            await ctx.send(
                f'Canal de voz "{nome}" criado na categoria "Counter-Strike 2".'
            )


# Comando para remover os canais e a categoria "Counter-Strike 2"
@client.command(name="remove")
async def remove_channels(ctx, opcao):
    # Verifica se o autor do comando tem permissão de administrador
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("Você não tem permissão para executar este comando.")
        return

    # Valida se o parâmetro está correto
    if opcao != "channels":
        await ctx.send("Uso incorreto. Tente: `!remove channels`")
        return

    guild = ctx.guild

    # Lista dos canais a serem removidos
    canais_a_remover = [
        "[MIX 1] - LOBBY",
        "[MIX 1] - EQUIPE 1",
        "[MIX 1] - EQUIPE 2",
        "FILA DE ESPERA",
        "[MIX 2] - LOBBY",
        "[MIX 2] - EQUIPE 1",
        "[MIX 2] - EQUIPE 2",
    ]

    removidos = []

    # Remove canais existentes da lista
    for nome in canais_a_remover:
        canal = discord.utils.get(guild.voice_channels, name=nome)
        if canal:
            await canal.delete()
            removidos.append(nome)

    # Envia mensagem com canais removidos
    if removidos:
        await ctx.send(f'Canais removidos: {", ".join(removidos)}')
    else:
        await ctx.send("Nenhum dos canais padrão foi encontrado para remover.")

    # Se a categoria estiver vazia após a remoção, exclui ela
    categoria = discord.utils.get(guild.categories, name="Counter-Strike 2")
    if categoria and len(categoria.channels) == 0:
        await categoria.delete()
        await ctx.send('Categoria "Counter-Strike 2" removida, pois ficou vazia.')

    if opcao != "channels":
        await ctx.send("Uso incorreto. Tente: `!remove channels`")
        return

    guild = ctx.guild
    canais_a_remover = [
        "[MIX 1] - LOBBY",
        "[MIX 1] - EQUIPE 1",
        "[MIX 1] - EQUIPE 2",
        "FILA DE ESPERA",
        "[MIX 2] - LOBBY",
        "[MIX 2] - EQUIPE 1",
        "[MIX 2] - EQUIPE 2",
    ]

    removidos = []
    for nome in canais_a_remover:
        canal = discord.utils.get(guild.voice_channels, name=nome)
        if canal:
            await canal.delete()
            removidos.append(nome)

    if removidos:
        await ctx.send(f'Canais removidos: {", ".join(removidos)}')
    else:
        await ctx.send("Nenhum dos canais padrão foi encontrado para remover.")

    # Verifica se a categoria ficou vazia e deleta
    categoria = discord.utils.get(guild.categories, name="Counter-Strike 2")
    if categoria and len(categoria.channels) == 0:
        await categoria.delete()
        await ctx.send('Categoria "Counter-Strike 2" removida, pois ficou vazia.')


# Inicia o bot com o token do arquivo .env
client.run(TOKEN)

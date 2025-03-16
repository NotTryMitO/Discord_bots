import discord
from discord.ext import commands, tasks
import asyncio
import random
from discord import app_commands

id_do_servidor = 1252372709627924480
id_cargo_atendente = 1258496138856894566
CANAL_PERMITIDO_ID = 1258531535359971368
CANAL_PERMITIDO = 1271454813464428596
REQUIRED_ROLE_ID = 1258493164524666901
member_role = 1303727367901941822
REQUIRED_ROLE_ID2 = 1303726904569892884

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = True
intents.presences = True
intents.reactions = True
intents.integrations = True

bot1_token = '' #NTM BOT DEV
bot2_token = '' #NTM TICKET
bot3_token = '' #NTM MODS BOT
bot4_token = '' #GK COMMUNITY
bot6_token = '' #+SHOP
bot1 = commands.Bot(command_prefix="001", intents=intents) #NTM BOT DEV
bot2 = commands.Bot(command_prefix="22", intents=intents) #NTM TICKET
bot3 = commands.Bot(command_prefix='0001', intents=intents) #NTM MODS BOT
bot4 = commands.Bot(command_prefix='0001', intents=intents,) #GK Community
bot6 = commands.Bot(command_prefix="0001", intents=intents) #+SHOP

#NTM MODS BOT
emojis_cargos = {
    '⚙️': 'Updates',
    '✉️': 'Leaks',
    '📩': 'News',
}

emoji_cargo_verificar = {
    '✅': '⭐MEMBER',
}

def get_random_emoji():
    emojis = ['😀', '😃', '😄', '😁', '😆']
    return random.choice(emojis)


class TicketButton(discord.ui.Button):
    def __init__(self, label, ticket_option=None, image_url=None, ticket_text=None):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.ticket_option = ticket_option
        self.image_url = image_url
        self.ticket_text = ticket_text

    async def callback(self, interaction: discord.Interaction):
        if self.ticket_option:
            ticket_name = f"{self.ticket_option}"
            role_to_mention = discord.utils.get(interaction.guild.roles, name="NTM DEV")
            role_mention = role_to_mention.mention
            user = interaction.user
            guild = interaction.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                role_to_mention: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            ticket_channel = await guild.create_text_channel(ticket_name, overwrites=overwrites)
            ticket_message = f"📩 **|** Hi {user.mention}! You opened the ticket {self.ticket_option}. Send all possible information about your case and wait until the {role_mention} reply."
            if self.ticket_text:
                ticket_message += f"\n\n{self.ticket_text}"
            if self.image_url:
                ticket_message += f"\n{self.image_url}"
            await ticket_channel.send(ticket_message)
            await interaction.response.send_message(f"You opened the ticket {self.ticket_option} in {ticket_channel.mention}", ephemeral=True)
            view = discord.ui.View()
            close_button = CloseButton("Close", ticket_channel.id)
            view.add_item(close_button)
            await ticket_channel.send("Click the button below to close this ticket:", view=view)
        else:
            await interaction.response.send_message("Invalid ticket option.", ephemeral=True)

class CloseButton(discord.ui.Button):
    def __init__(self, label, channel_id):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        ticket_channel = interaction.guild.get_channel(self.channel_id)
        if ticket_channel:
            await ticket_channel.delete()
            await interaction.response.send_message("The ticket was closed successfully.", ephemeral=True)
        else:
            await interaction.response.send_message("Unable to find ticket channel.", ephemeral=True)

@bot3.event
async def on_message(message):
    if isinstance(message.channel, discord.TextChannel):
        message_limit = 5
        message_interval = 1
        user_message_count = 0
        
        async for msg in message.channel.history(limit=message_limit, oldest_first=False):
            if msg.author == message.author and (message.created_at - msg.created_at).total_seconds() <= message_interval:
                user_message_count += 1
        
        if user_message_count >= message_limit:
            role = discord.utils.get(message.guild.roles, name="🪑Punished")
            await message.author.add_roles(role)
            await message.channel.send(f"{message.author.mention} was punished 10 minutes for spamming.")

            await asyncio.sleep(600)
            await message.author.remove_roles(role)
            await message.channel.send(f"The temporary mute of {message.author.mention} has expired.")

    await bot3.process_commands(message)

@bot3.event
async def on_guild_channel_create(channel):
    role_castigado = discord.utils.get(channel.guild.roles, name="🪑Punished")
    if role_castigado:
        await channel.set_permissions(role_castigado, send_messages=False)

@bot3.tree.command(name="members", description="Get the number of members in the server")
async def members(interaction: discord.Interaction):
    guild = interaction.guild
    
    if not guild:
        await interaction.response.send_message("Could not retrieve member count.", ephemeral=True)
        return
    
    # Get the member who triggered the interaction
    member = guild.get_member(interaction.user.id)
    
    if member.bot:
        return
    
    member_count = guild.member_count
    await interaction.response.send_message(f"The server has {member_count} members.")


@bot3.command()
async def verificar(ctx, interaction: discord.Interaction):
    
    if any(role.id == REQUIRED_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message("You have access to this command!")
    else:
        await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)
    
    role_to_mention = discord.utils.get(ctx.guild.roles, name="⭐MEMBER")
    role_mention = role_to_mention.mention if role_to_mention else "role not found"
    
    embed = discord.Embed(
        title="**NTM MODS | Verification System**",
        description=":arrow_right: Welcome to NTM MODS! Don't forget to check https://discord.com/channels/1252372709627924480/1258527704781688842 to avoid being punished!",
        color=0xff0000
    )
    embed.add_field(
        name="",
        value=":arrow_right: If you have any questions, we are here to help! Contact a staff member in https://discord.com/channels/1252372709627924480/1258533480975958126",
        inline=False
    )
    embed.add_field(
        name="",
        value=f":arrow_right: After verification, you will be given the {role_mention} role to access the discord!",
        inline=False
    )
    embed.add_field(
        name="",
        value="To verify yourself, react with :white_check_mark: to this message!",
        inline=False
    )
    image_url = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXp2djJobWtzcHBrYmJiMTVndW02N2w4cmZjdXhlamw2dW56a3B5aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vbXFnr3tDWojRKXf72/giphy.gif"
    embed.set_image(url=image_url)
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')

@bot3.tree.command(name="helpme", description="Command that lists all commands")
async def helpme(interaction: discord.Interaction):
    embed = discord.Embed(
        title="**Command List**",
        description="Here are all available commands and their functions:",
        color=0xff0000
    )
    embed.add_field(name="/members", value="Shows the number of members on the server.", inline=False)
    embed.add_field(name="/delete [quantity]", value="Deletes a specific number of messages in the channel (only for users with message management permissions).", inline=False)
    embed.add_field(name="/suggestion [text]", value="Send a suggestion to the suggestions channel. https://discord.com/channels/1252372709627924480/1258531535359971368", inline=False)
    await interaction.response.send_message(embed=embed)

@bot3.tree.command(name="delete", description="Command to delete messages")
async def delete(interaction: discord.Interaction, amount: int):
    if interaction.user.guild_permissions.manage_messages:
        if 0 < amount <= 100:
            await interaction.response.defer(ephemeral=True)  # Defer the response to avoid timeout
            await interaction.channel.purge(limit=amount + 1)
            await interaction.followup.send(f"{amount} messages were deleted.", ephemeral=True)
        else:
            await interaction.response.send_message("The number of messages to delete must be between 1 and 100.", ephemeral=True)
    else:
        await interaction.response.send_message("You are not allowed to delete messages on this server.", ephemeral=True)
    if any(role.id == REQUIRED_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message("You have access to this command!")
    else:
        await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)

@bot3.command(name="suggestion", description="Command to send your suggestions")
async def suggestion(ctx, *, texto: str):
    if ctx.channel.id != CANAL_PERMITIDO_ID:
        await ctx.message.delete()
        await ctx.send("This command can only be used on the allowed channel.", delete_after=5)
        return
    embed = discord.Embed(
        title="Suggestion",
        description=texto,
        color=discord.Color.yellow()
    )
    if isinstance(ctx.author, discord.Member):
        user = ctx.author
        embed.set_author(name=user.display_name)
        if user.avatar:
            embed.set_author(name=user.display_name, icon_url=user.avatar.url)
    await ctx.send(embed=embed)
    await ctx.message.delete()

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="shopping", label="Shopping", emoji="🛒"),
            discord.SelectOption(value="support", label="Support", emoji="💳"),
            discord.SelectOption(value="doubts", label="Doubts", emoji="❔"),
            discord.SelectOption(value="bugs", label="Bugs", emoji="🐌")
        ]
        super().__init__(
            placeholder="Select an option...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] in ["shopping", "support", "doubts", "bugs"]:
            selected_option = self.values[0]
            await interaction.response.defer()
            view = discord.ui.View()
            open_button = TicketButton(label=f"Open {selected_option} Ticket", ticket_option=selected_option)
            view.add_item(open_button)
            await interaction.followup.send(content=f"Press the button below to open a {selected_option} ticket", view=view, ephemeral=True)

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

@bot3.command()
async def setup(ctx, interaction: discord.Interaction):
    embed = discord.Embed(
        title="**SERVICE**",
        description="➡️ - To open a ticket, select one of the options below:",
        color=0xff0000
    )
    embed.add_field(name="", value="```ㅤㅤㅤㅤ! 𝘽𝙀𝙁𝙊𝙍𝙀 𝙊𝙋𝙀𝙉𝙄𝙉𝙂 !ㅤㅤㅤ```", inline=False)
    embed.add_field(name="", value="➡️ - Do not open a ticket without **NECESSITY**", inline=False)
    embed.add_field(name="", value="➡️ - Don't tag the MODERATORS, they are aware of your ticket", inline=False)
    embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXp2djJobWtzcHBrYmJiMTVndW02N2w4cmZjdXhlamw2dW56a3B5aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vbXFnr3tDWojRKXf72/giphy.gif")
    message = await ctx.send(embed=embed)
    await ctx.send("", view=PersistentView())
    
    if any(role.id == REQUIRED_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message("You have access to this command!")
    else:
        await interaction.response.send_message("You do not have the required role to use this command.", ephemeral=True)

@bot3.event
async def on_raw_reaction_add(payload):
    guild = bot3.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member.bot:
        return

    if payload.message_id == 1264350629284024444:
        emoji = str(payload.emoji)
        if emoji in emojis_cargos:
            cargo_nome = emojis_cargos[emoji]
            cargo = discord.utils.get(guild.roles, name=cargo_nome)
            if cargo:
                await member.add_roles(cargo)
                print(f'{member.name} recebeu o cargo {cargo_nome}.')

@bot3.event
async def on_raw_reaction_add(payload):
    guild = bot3.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member.bot:
        return

    if payload.message_id == 1263597231961931796:
        emoji = str(payload.emoji)
        if emoji in emoji_cargo_verificar:
            cargo_nome = emoji_cargo_verificar[emoji]
            cargo = discord.utils.get(guild.roles, name=cargo_nome)
            if cargo:
                await member.add_roles(cargo)
                print(f'{member.name} recebeu o cargo {cargo_nome}.')

@bot3.event
async def on_ready():
    bot3.add_view(PersistentView())
    print("Persistent view has been added.")
    print(f'Logged in as {bot3.user}')
    try:
        synced = await bot3.tree.sync()  # Register slash commands
        print(f'Successfully synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    await bot3.change_presence(activity=discord.Game(name="The Empyrium"))

@bot3.tree.command(name="hi", description="Hi!")
async def hi(interaction: discord.Interaction):
    await interaction.response.send_message('Hi! ' + get_random_emoji())

@bot3.tree.command(name="empyrium", description="Download The Empyrium!")
async def empyrium(interaction: discord.Interaction):
    if interaction.channel.id != CANAL_PERMITIDO:
        await interaction.response.send_message("This command can only be used in the allowed channel.", ephemeral=True)
        return

    await interaction.response.send_message('Go to https://discord.com/channels/1252372709627924480/1258810686948118658')

@bot3.tree.command(name='website', description='Official website of NTM MODS')
async def website(interaction:discord.Interaction):
    if interaction.channel.id != CANAL_PERMITIDO:
        await interaction.response.send_message("This command can only be used in the allowed channel.", ephemeral=True)
        return

    await interaction.response.send_message('https://nottrymito.github.io/ntm-mods/#home')

'''NTM DEV BOT'''

#role automatica
@bot1.event
async def on_member_join(member):
    ROLE_ID = 1303727367901941822
    guild = member.guild
    role = guild.get_role(ROLE_ID)
    
    if role:
        try:
            await member.add_roles(role)
            print('-----------------------------------')
            print(f'Adicionada a role "{role.name}" ao membro {member.name}.')
            print('-----------------------------------')
        except discord.Forbidden:
            print(f"Permissão insuficiente para adicionar a role '{role.name}' ao membro {member.name}.")
        except discord.HTTPException as e:
            print(f"Erro ao tentar adicionar a role: {e}")
    else:
        print(f"Role com ID {ROLE_ID} não encontrada no servidor {guild.name}.")

#contadores
@tasks.loop(seconds=30)
async def atualizar_canal_members():
    CANAL_ID = 1303520594649677894
    try:
        canal = bot1.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            membros_reais = [m for m in guild.members if not m.bot]
            numero_membros_reais = len(membros_reais)
            novo_nome = f'members-{numero_membros_reais}'
            await canal.edit(name=novo_nome)
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

@tasks.loop(seconds=30)
async def atualizar_canal_clients():
    CANAL_ID = 1303719327601655828
    ROLE_ID = 1303727484965224509
    try:
        canal = bot1.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            role = guild.get_role(ROLE_ID)
            if role:
                numero_membros_com_role = len(role.members)
                novo_nome = f'clients-{numero_membros_com_role}'
                await canal.edit(name=novo_nome)
            else:
                print(f"Role com ID {ROLE_ID} não encontrada no servidor {guild.name}.")
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

@tasks.loop(seconds=30)
async def atualizar_canal_bots():
    CANAL_ID = 1307465880745017366
    try:
        canal = bot1.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            bots = [m for m in guild.members if m.bot]
            numero_bots = len(bots)
            novo_nome = f'bots-{numero_bots}'
            await canal.edit(name=novo_nome)
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

#bot1 on_ready
@bot1.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="™ NTM DEV")
    print(f'Logged in as {bot1.user}')
    try:
        synced = await bot1.tree.sync()
        print(f'{bot1.user} synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    await bot1.change_presence(activity=activity)
    atualizar_canal_members.start()
    atualizar_canal_clients.start()
    atualizar_canal_bots.start()

'''NTM TICKET'''

#bot2 on_ready
@bot2.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="Desenvolvido por NTM DEV")
    print(f'Logged in as {bot2.user}')
    try:
        synced = await bot2.tree.sync()
        print(f'{bot2.user} synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    await bot2.change_presence(activity=activity)
    ticket_setup.start()

#ticket
class TicketButton(discord.ui.Button):
    def __init__(self, label, ticket_option=None, image_url=None, ticket_text=None):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.ticket_option = ticket_option
        self.image_url = image_url
        self.ticket_text = ticket_text

    async def callback(self, interaction: discord.Interaction):
        if self.ticket_option:
            ticket_name = f"{self.ticket_option}"
            role_to_mention = discord.utils.get(interaction.guild.roles, name="NTM DEV")
            role_mention = role_to_mention.mention
            user = interaction.user
            guild = interaction.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                role_to_mention: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            ticket_channel = await guild.create_text_channel(ticket_name, overwrites=overwrites)
            ticket_message = f"📩 **|** Hi {user.mention}! You opened the ticket {self.ticket_option}. Send all possible information about your case and wait until the {role_mention} reply."
            if self.ticket_text:
                ticket_message += f"\n\n{self.ticket_text}"
            if self.image_url:
                ticket_message += f"\n{self.image_url}"
            await ticket_channel.send(ticket_message)
            await interaction.response.send_message(f"You opened the ticket {self.ticket_option} in {ticket_channel.mention}", ephemeral=True)
            view = discord.ui.View()
            close_button = CloseButton("Close", ticket_channel.id)
            view.add_item(close_button)
            await ticket_channel.send("Click the button below to close this ticket:", view=view)
        else:
            await interaction.response.send_message("Invalid ticket option.", ephemeral=True)

class CloseButton(discord.ui.Button):
    def __init__(self, label, channel_id):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        ticket_channel = interaction.guild.get_channel(self.channel_id)
        if ticket_channel:
            await ticket_channel.delete()
            await interaction.response.send_message("The ticket was closed successfully.", ephemeral=True)
        else:
            await interaction.response.send_message("Unable to find ticket channel.", ephemeral=True)

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="shopping", label="Shopping", emoji="🛒", description='Ticket for shopping'),
            discord.SelectOption(value="support", label="Support", emoji="💳", description='Ticket for support'),
            discord.SelectOption(value="doubts", label="Doubts", emoji="❔", description='Ticket for doubts'),
            discord.SelectOption(value="bugs", label="Bugs", emoji="🐌", description='Ticket for bugs'),
            discord.SelectOption(value='partners', label='Partners', emoji='🤝', description='Ticket to close partnership')
        ]
        super().__init__(
            placeholder="Select an option...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] in ["shopping", "support", "doubts", "bugs", 'partners']:
            selected_option = self.values[0]
            await interaction.response.defer()
            view = discord.ui.View()
            open_button = TicketButton(label=f"Open {selected_option} Ticket", ticket_option=selected_option)
            view.add_item(open_button)
            await interaction.followup.send(content=f"Press the button below to open a {selected_option} ticket", view=view, ephemeral=True)

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

@tasks.loop(minutes=5)
async def ticket_setup():
    channel = bot2.get_channel(1303725153934381090)
    if channel:
        try:
            await channel.purge(limit=None)
            print("Canal  do ticket apagado")
            
            embed = discord.Embed(
            title="**SERVICE**",
            description="➡️ - To open a ticket, select one of the options below:",
            color=0x2f336b
            )
            embed.add_field(name="", value="```ㅤㅤㅤㅤㅤㅤㅤㅤ! 𝘽𝙀𝙁𝙊𝙍𝙀 𝙊𝙋𝙀𝙉𝙄𝙉𝙂 !ㅤㅤㅤ```", inline=False)
            embed.add_field(name="", value="➡️ - Do not open a ticket without **NECESSITY**", inline=False)
            embed.add_field(name="", value="➡️ - Don't tag the MODERATORS, they are aware of your ticket", inline=False)
            embed.set_image(url="https://i.imgur.com/FSpYE9u.png")
         
            await channel.send(embed=embed, view=PersistentView())
    
        except Exception as e:
            print(f"Error: {e}")

'''bot ticket - bot2 - ends'''

'''GK community'''

@bot4.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="GK Community")
    print(f'Logged in as {bot4.user}')
    try:
        synced = await bot4.tree.sync()
        print(f'{bot4.user} synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    await bot4.change_presence(activity=activity)

'''+SHOP'''
@bot6.event
async def on_ready():
    bot6.add_view(PersistentView())
    print("Persistent view has been added.")
    print(f'Logged in as {bot6.user}')
    try:
        synced = await bot6.tree.sync()
        print(f'Successfully synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    bot6.loop.create_task(alternar_presenca())
    atualizar_canal_members.start()
    atualizar_canal_clients.start()

#presença
async def alternar_presenca():
    guild_id = 1290074291047632919
    role_id = 1303727367901941822

    while True:
        # Alterna entre diferentes presenças
        activity = discord.Activity(type=discord.ActivityType.listening, name="what you need")
        await bot6.change_presence(activity=activity)
        await asyncio.sleep(5)

        activity = discord.Game(name="+SHOP")
        await bot6.change_presence(activity=activity)
        await asyncio.sleep(5)

        # Obtém a contagem de membros com a role
        count_membros = count_members_with_role(guild_id, role_id)
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"CLIENTS - 15")
        await bot6.change_presence(activity=activity)
        await asyncio.sleep(5)

def count_members_with_role(guild_id, role_id):
    guild = bot6.get_guild(guild_id)

    if not guild:
        print(f"Guild with ID {guild_id} not found.")
        return 0

    role = discord.utils.get(guild.roles, id=1307361645911085138)  # Substitua pelo ID da role

    if not role:
        print(f"Role with ID {role_id} not found in guild {guild.name}.")
        return 0

    members_with_role = [member for member in guild.members if role in member.roles]
    return len(members_with_role)

#canais de informações
#members
@tasks.loop(seconds=30)
async def atualizar_canal_members():
    CANAL_ID = 1311348717986648204
    try:
        canal = bot6.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            membros_reais = [m for m in guild.members if not m.bot]
            numero_membros_reais = len(membros_reais)
            novo_nome = f'members-{numero_membros_reais}'
            await canal.edit(name=novo_nome)
            print('-----------------------------------')
            print(f'Canal atualizado para: {novo_nome}')
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

#clients
@tasks.loop(seconds=30)
async def atualizar_canal_clients():
    CANAL_ID = 1311348837092298822
    ROLE_ID = 1307361645911085138
    try:
        canal = bot6.get_channel(CANAL_ID)
        if canal:
            guild = canal.guild
            role = guild.get_role(ROLE_ID)
            if role:
                numero_membros_com_role = len(role.members)
                novo_nome = f'clients-{numero_membros_com_role}'
                await canal.edit(name=novo_nome)
                print(f'Canal atualizado para: {novo_nome}')
            else:
                print(f"Role com ID {ROLE_ID} não encontrada no servidor {guild.name}.")
        else:
            print(f"Canal com ID {CANAL_ID} não encontrado.")
    except Exception as e:
        print(f"Erro ao tentar atualizar o canal: {e}")

#ticket command
class TicketButton(discord.ui.Button):
    def __init__(self, label, ticket_option=None, image_url=None, ticket_text=None):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.ticket_option = ticket_option
        self.image_url = image_url
        self.ticket_text = ticket_text

    async def callback(self, interaction: discord.Interaction):
        if self.ticket_option:
            ticket_name = f"{self.ticket_option}"
            role_to_mention = discord.utils.get(interaction.guild.roles, name="Owners")
            role_mention = role_to_mention.mention
            user = interaction.user
            guild = interaction.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                role_to_mention: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            ticket_channel = await guild.create_text_channel(ticket_name, overwrites=overwrites)
            ticket_message = f"📩 **|** Hi {user.mention}! You opened the ticket {self.ticket_option}. Send all possible information about your case and wait until the {role_mention} reply."
            if self.ticket_text:
                ticket_message += f"\n\n{self.ticket_text}"
            if self.image_url:
                ticket_message += f"\n{self.image_url}"
            await ticket_channel.send(ticket_message)
            await interaction.response.send_message(f"You opened the ticket {self.ticket_option} in {ticket_channel.mention}", ephemeral=True)
            view = discord.ui.View()
            close_button = CloseButton("Close", ticket_channel.id)
            view.add_item(close_button)
            await ticket_channel.send("Click the button below to close this ticket:", view=view)
        else:
            await interaction.response.send_message("Invalid ticket option.", ephemeral=True)

class CloseButton(discord.ui.Button):
    def __init__(self, label, channel_id):
        super().__init__(style=discord.ButtonStyle.grey, label=label)
        self.channel_id = channel_id

    async def callback(self, interaction: discord.Interaction):
        ticket_channel = interaction.guild.get_channel(self.channel_id)
        if ticket_channel:
            await ticket_channel.delete()
            await interaction.response.send_message("The ticket was closed successfully.", ephemeral=True)
        else:
            await interaction.response.send_message("Unable to find ticket channel.", ephemeral=True)

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value="shopping", label="Shopping", emoji="🛒"),
            discord.SelectOption(value="support", label="Support", emoji="💳"),
            discord.SelectOption(value="doubts", label="Doubts", emoji="❔"),
        ]
        super().__init__(
            placeholder="Select an option...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] in ["shopping", "support", "doubts"]:
            selected_option = self.values[0]
            await interaction.response.defer()
            view = discord.ui.View()
            open_button = TicketButton(label=f"Open {selected_option} Ticket", ticket_option=selected_option)
            view.add_item(open_button)
            await interaction.followup.send(content=f"Press the button below to open a {selected_option} ticket", view=view, ephemeral=True)

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

@bot6.command()
async def setup(ctx):
    required_role_id = 1307359126967291975
    
    if not any(role.id == required_role_id for role in ctx.author.roles):
        await ctx.send("You do not have the required role to use this command.", delete_after=5)
        return

    embed = discord.Embed(
        title="**TICKET**",
        description="➡️ - To open a ticket, select one of the options below:",
        color=0x00FFFF
    )
    embed.add_field(name="", value="```ㅤㅤㅤㅤ! 𝘽𝙀𝙁𝙊𝙍𝙀 𝙊𝙋𝙀𝙉𝙄𝙉𝙂 !ㅤㅤㅤ```", inline=False)
    embed.add_field(name="", value="➡️ - Do not open a ticket without **NECESSITY**", inline=False)
    embed.add_field(name="", value="➡️ - Don't tag the MODERATORS, they are aware of your ticket", inline=False)
    embed.set_image(url="https://i.imgur.com/gZVmjvJ.png")

    await ctx.send(embed=embed)
    await ctx.send(view=PersistentView())

#help command
@bot6.tree.command(name="helpme", description="Command that lists all commands")
async def helpme(interaction: discord.Interaction):
    embed = discord.Embed(
        title="**Command List**",
        description="Here are all available commands and their functions:",
        color=0x00FFFF
    )
    embed.add_field(name="/delete [quantity]", value="Deletes a specific number of messages in the channel (only for users with message management permissions).", inline=False)
    embed.add_field(name=".suggestion [text]", value="Send a suggestion to the suggestions channel. https://discord.com/channels/1307354161737629696/1311346394195300523", inline=False)
    await interaction.response.send_message(embed=embed)

#delete command
@bot6.tree.command(name="delete", description="Command to delete messages")
async def delete(interaction: discord.Interaction, amount: int):
    required_role_id = 1307359126967291975

    if not any(role.id == required_role_id for role in interaction.user.roles):
        await interaction.response.send_message("You have access to this command!", ephemeral=True)
        return
    
    if interaction.user.guild_permissions.manage_messages:
        if 0 < amount <= 100:
            await interaction.response.defer(ephemeral=True)  # Defer the response to avoid timeout
            await interaction.channel.purge(limit=amount + 1)
            await interaction.followup.send(f"{amount} messages were deleted.", ephemeral=True)
        else:
            await interaction.response.send_message("The number of messages to delete must be between 1 and 100.", ephemeral=True)
    else:
        await interaction.response.send_message("You are not allowed to delete messages on this server.", ephemeral=True)

#suggestion command
@bot6.command(name="suggestion", description="Command to send your suggestions")
async def suggestion(ctx, *, texto: str):
    if ctx.channel.id != 1311346394195300523:
        await ctx.message.delete()
        await ctx.send("This command can only be used on the allowed channel.", delete_after=5)
        return
    embed = discord.Embed(
        title="Suggestion",
        description=texto,
        color=discord.Color.yellow()
    )
    if isinstance(ctx.author, discord.Member):
        user = ctx.author
        embed.set_author(name=user.display_name)
        if user.avatar:
            embed.set_author(name=user.display_name, icon_url=user.avatar.url)
    await ctx.send(embed=embed)
    await ctx.message.delete()

#safe control
SAFE_USERS = 1307359126967291975

@bot6.event
async def on_guild_channel_delete(channel):
    """Detecta exclusão de canais em massa"""
    guild = channel.guild
    logs = await guild.audit_logs(limit=2, action=discord.AuditLogAction.channel_delete).flatten()
    if logs:
        log_entry = logs[0]
        user = log_entry.user

        if user.id not in SAFE_USERS:
            await guild.ban(user, reason="Possível ataque Nuke: exclusão de canais.")
            print(f"Usuário {user} banido por exclusão de canais!")
            # Reconstruir o canal
            await guild.create_text_channel(channel.name)

@bot6.event
async def on_member_remove(member):
    """Detecta remoções em massa de membros"""
    guild = member.guild
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
    if logs:
        log_entry = logs[0]
        user = log_entry.user

        if user.id not in SAFE_USERS:
            await guild.ban(user, reason="Possível ataque Nuke: remoção de membros.")
            print(f"Usuário {user} banido por remoção de membros!")

@bot6.event
async def on_audit_log_entry_create(entry):
    """Monitora ações suspeitas nos logs"""
    actions_to_monitor = [discord.AuditLogAction.kick, discord.AuditLogAction.ban]
    if entry.action in actions_to_monitor:
        if entry.user.id not in SAFE_USERS:
            guild = entry.target.guild
            await guild.ban(entry.user, reason="Possível ataque Nuke: ações suspeitas.")
            print(f"Usuário {entry.user} banido por ações suspeitas!")

@bot6.command()
async def whitelist(ctx, user: discord.Member):
    """Adiciona um usuário à lista de confiança"""
    if ctx.author.id not in SAFE_USERS:
        await ctx.send("Você não tem permissão para executar este comando!")
        return

    SAFE_USERS.append(user.id)
    await ctx.send(f"Usuário {user.mention} adicionado à lista de confiança.")

@bot6.command()
async def unwhitelist(ctx, user: discord.Member):
    """Remove um usuário da lista de confiança"""
    if ctx.author.id not in SAFE_USERS:
        await ctx.send("Você não tem permissão para executar este comando!")
        return

    if user.id in SAFE_USERS:
        SAFE_USERS.remove(user.id)
        await ctx.send(f"Usuário {user.mention} removido da lista de confiança.")
    else:
        await ctx.send(f"O usuário {user.mention} não está na lista de confiança.")

@bot6.command()
async def lock(ctx):
    """Bloqueia o servidor (modo de emergência)"""
    if ctx.author.id not in SAFE_USERS:
        await ctx.send("Você não tem permissão para executar este comando!")
        return

    guild = ctx.guild
    for channel in guild.channels:
        await channel.set_permissions(guild.default_role, send_messages=False)
    await ctx.send("Servidor bloqueado! Nenhum membro pode enviar mensagens.")

@bot6.command()
async def unlock(ctx):
    """Desbloqueia o servidor"""
    if ctx.author.id not in SAFE_USERS:
        await ctx.send("Você não tem permissão para executar este comando!")
        return

    guild = ctx.guild
    for channel in guild.channels:
        await channel.set_permissions(guild.default_role, send_messages=True)
    await ctx.send("Servidor desbloqueado! Mensagens permitidas novamente.")

async def main():
    await asyncio.gather(
        bot1.start(bot1_token),
        bot2.start(bot2_token),
        bot3.start(bot3_token),
        bot4.start(bot4_token),
        bot5.start(bot6_token),
    )

if __name__ == "__main__":
    asyncio.run(main())

import discord
from discord.ext import commands
import os
import platform
import aiohttp
from pystyle import Colors, Colorate, Center


def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def print_welcome_message():
    print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter("""
    
░█████╗░░█████╗░░██████╗░█████╗░  ░█████╗░██╗░░░░░░█████╗░███╗░░██╗███████╗██████╗░
██╔══██╗██╔══██╗██╔════╝██╔══██╗  ██╔══██╗██║░░░░░██╔══██╗████╗░██║██╔════╝██╔══██╗
██║░░╚═╝███████║╚█████╗░███████║  ██║░░╚═╝██║░░░░░██║░░██║██╔██╗██║█████╗░░██████╔╝
██║░░██╗██╔══██║░╚═══██╗██╔══██║  ██║░░██╗██║░░░░░██║░░██║██║╚████║██╔══╝░░██╔══██╗
╚█████╔╝██║░░██║██████╔╝██║░░██║  ╚█████╔╝███████╗╚█████╔╝██║░╚███║███████╗██║░░██║
░╚════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝  ░╚════╝░╚══════╝░╚════╝░╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
                          Developed by Script:Code
    """)))


async def download_server_icon(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
    return None


async def delete_all_channels(guild):
    for channel in guild.channels:
        await channel.delete()


async def delete_all_roles(guild):
    for role in guild.roles:
        if role.name != "@everyone":  
            try:
                await role.delete()
            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_black, f"Errore nell'eliminare il ruolo {role.name}: {e}"))


async def copy_server(source_guild, target_guild):
    
    await target_guild.edit(name=source_guild.name)

    
    if source_guild.icon is not None:
        icon_url = source_guild.icon.url if isinstance(source_guild.icon, discord.Asset) else None
        if icon_url:
            icon_data = await download_server_icon(icon_url)
            if icon_data:
                await target_guild.edit(icon=icon_data)
    
    e
    await delete_all_channels(target_guild)
    
    
    await delete_all_roles(target_guild)
    
    
    for category in source_guild.categories:
        new_category = await target_guild.create_category(name=category.name, position=category.position)
        for channel in category.channels:
            if isinstance(channel, discord.TextChannel):
                await target_guild.create_text_channel(name=channel.name, category=new_category, position=channel.position, topic=channel.topic, nsfw=channel.nsfw, slowmode_delay=channel.slowmode_delay)
            elif isinstance(channel, discord.VoiceChannel):
                await target_guild.create_voice_channel(name=channel.name, category=new_category, position=channel.position, bitrate=channel.bitrate, user_limit=channel.user_limit)

    
    for channel in source_guild.channels:
        if isinstance(channel, discord.TextChannel) and channel.category is None:
            await target_guild.create_text_channel(name=channel.name, position=channel.position, topic=channel.topic, nsfw=channel.nsfw, slowmode_delay=channel.slowmode_delay)
        elif isinstance(channel, discord.VoiceChannel) and channel.category is None:
            await target_guild.create_voice_channel(name=channel.name, position=channel.position, bitrate=channel.bitrate, user_limit=channel.user_limit)

    
    for role in source_guild.roles[::-1]:  
        if role.name != "@everyone":  
            try:
                await target_guild.create_role(name=role.name, permissions=role.permissions, colour=role.colour, hoist=role.hoist, mentionable=role.mentionable)
            except Exception as e:
                print(Colorate.Horizontal(Colors.red_to_black, f"Errore nella creazione del ruolo {role.name}: {e}"))


intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def start_cloning():
    clear_console()  
    print_welcome_message()
    
    
    source_guild_id = input(Colorate.Horizontal(Colors.red_to_yellow, "Inserisci l'ID del server da copiare: "))
    target_guild_id = input(Colorate.Horizontal(Colors.red_to_yellow, "Inserisci l'ID del server di destinazione: "))

    source_guild = bot.get_guild(int(source_guild_id))
    target_guild = bot.get_guild(int(target_guild_id))

    if source_guild is None or target_guild is None:
        print(Colorate.Horizontal(Colors.red_to_black, "Server non trovati. Assicurati che il bot sia nei server e abbia i permessi necessari."))
        input(Colorate.Horizontal(Colors.blue_to_white, "\nPremi Enter per continuare..."))  
        await start_cloning()  
        return

    print(Colorate.Horizontal(Colors.blue_to_green, f"Sto copiando il server '{source_guild.name}' nel server '{target_guild.name}'..."))

    try:
        await copy_server(source_guild, target_guild)
        print(Colorate.Horizontal(Colors.green_to_white, "Copia del server completata con successo!"))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_black, f"Errore durante la copia del server: {e}"))
        input(Colorate.Horizontal(Colors.blue_to_white, "\nPremi Enter per continuare..."))  
        await start_cloning()  
        return

    input(Colorate.Horizontal(Colors.blue_to_white, "\nPremi Enter per continuare..."))  
    await start_cloning()  

@bot.event
async def on_ready():
    await start_cloning()  


if __name__ == "__main__":
    clear_console()  
    print_welcome_message()
    token = input(Colorate.Horizontal(Colors.blue_to_purple, "Inserisci il token del bot: "))
    bot.run(token)

















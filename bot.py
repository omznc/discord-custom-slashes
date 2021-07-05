import discord
from discord.ext import commands
import re
import json
import os
import sys
import pathlib
import time
import shutil
from discord_slash import SlashCommand, SlashContext # Importing the newly installed library.
from discord_slash.utils.manage_commands import create_permission, create_option, create_choice, remove_slash_command, get_all_commands
from discord_slash.model import SlashCommandPermissionType
# pip install git+https://github.com/eunwoo1104/discord-py-slash-command --force

TOKEN = "REPLACE_THIS"
client = commands.Bot(intents=discord.Intents.all(), command_prefix="!")
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload= True) # Declares slash commands through the client.
guild_ids= [REPLACE_THIS]
admin_role_id = [REPLACE THIS]
@client.event
async def on_ready():
    print("Ready!")

@slash.slash(name="reload", description="[ADMIN ONLY] Reloaduj komande.", guild_ids=guild_ids)
@slash.permission(guild_id=guild_ids[0], permissions=[create_permission(admin_role_id, SlashCommandPermissionType.ROLE, True), create_permission(guild_ids[0], SlashCommandPermissionType.ROLE, False)])
async def function(ctx):
    await ctx.send(f"Reloadano {len(os.listdir('./cogs'))} komandi.", hidden= True)
    os.execv(sys.executable, ['python'] + sys.argv)

@slash.slash(name="list", description="Lista komandi.", guild_ids=guild_ids)
async def function(ctx):
    embed=discord.Embed(title="Lista Komandi", description="Komande koje mozete koristiti su:", color=0x34c5ef)
    embed.set_thumbnail(url="https://i.imgur.com/Ogtw9Xo.png")
    information = {}
    for j in pathlib.Path('./cogs').iterdir():
        if j.is_file():
            with open(j, "r") as fuck:
                try:
                    information[str(j)[5:-3]] = str(re.findall('(?<=description=").*(?<=")', fuck.read())[0])[:-1]
                except:
                    information[str(j)[5:-3]] = "empty"
    del information["default"]
    for key, desc in information.items():
        embed.add_field(name=key, value=desc, inline=True)
    embed.set_footer(text="https://github.com/omznc/discord-custom-slashes/")
    await ctx.send(embed=embed, hidden=True)
        
@slash.permission(guild_id=guild_ids[0], permissions=[create_permission(admin_role_id, SlashCommandPermissionType.ROLE, True), create_permission(guild_ids[0], SlashCommandPermissionType.ROLE, False)])
@slash.slash(name="command", description="[ADMIN ONLY] Manipuliraj komandama | Add i Edit trebaju sve parametre a Remove treba name.", guild_ids=guild_ids, options=[
               create_option(
                 name="operator",
                 description="Add, Remove, ili Edit",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="add",
                    value="Add"
                  ),
                  create_choice(
                    name="remove",
                    value="Remove"
                  ),
                  create_choice(
                    name= "edit",
                    value= "Edit")
                ]
               ), 
               create_option(name="name", description="Ime nove komande | Primjer: zdravo postaje /zdravo",option_type=3, required=False),
               create_option(name="send", description="Output komande",option_type=3, required=False),
               create_option(name="description", description="Opis komande | Ovo je vidljivo kada neko napise /imeovekomande",option_type=3, required=False)
             ])
@slash.permission(guild_id=guild_ids[0], permissions=[create_permission(admin_role_id, SlashCommandPermissionType.ROLE, True), create_permission(guild_ids[0], SlashCommandPermissionType.ROLE, False)])
async def edit(ctx: SlashContext, operator:str, name=None, send=None, description=None):
    print(operator)
    if operator == "Edit":
        if name == None or send == None or description == None or not name.islower():
            await ctx.send(f"Niste includali sva 3 parametra ili ste koristili caps.", hidden= True)
        else:
            shutil.copy("./cogs/default.py", f"./cogs/{name}.py")
            with open(f'./cogs/{name}.py', 'r+') as f:
                data = f.readlines()
                data[9] = f'    @cog_ext.cog_slash(name="{name}", description="{description}", guild_ids=guild_ids) \n'
                data[11] = f'       await ctx.send("{send}") \n'
            with open(f'./cogs/{name}.py', 'r+') as f:
                f.writelines(data)
            await ctx.send(f'Komanda `{name}` editovana.', hidden= True)
            os.execv(sys.executable, ['python'] + sys.argv)
            
    if operator == "Add":
        if name == None or send == None or description == None or not name.islower():
            await ctx.send(f"Niste includali sva 3 parametra ili ste koristili caps.", hidden= True)
        else:
            exists = False
            for filename in os.listdir('./cogs'):
                if filename.startswith(name):
                    exists = True
            if exists:
                await ctx.send('Komanda vec postoji.', hidden= True)
            else:
                shutil.copy("./cogs/default.py", f"./cogs/{name}.py")
                with open(f'./cogs/{name}.py', 'r+') as f:
                    data = f.readlines()
                    data[9] = f'    @cog_ext.cog_slash(name="{name}", description="{description}", guild_ids=guild_ids) \n'
                    data[11] = f'       await ctx.send("{send}") \n'
                with open(f'./cogs/{name}.py', 'r+') as f:
                    f.writelines(data)
                await ctx.send(f'Komanda `{name}` napravljena.', hidden=True)
                os.execv(sys.executable, ['python'] + sys.argv)
    if operator == "Remove":
        if name == None:
            await ctx.send(f"Niste includali ime komande koju zelite ukloniti", hidden= True)
        else:
            try:
                os.remove(f'./cogs/{name}.py')
                await ctx.send(f"Komanda `{name}` je uklonjena.", hidden= True)
                os.execv(sys.executable, ['python'] + sys.argv)
            except Exception as E:
                await ctx.send(f"Komanda ne postoji.", hidden= True)

        
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('default'):
        client.load_extension(f'cogs.{filename[:-3]}')
        

client.run(TOKEN)

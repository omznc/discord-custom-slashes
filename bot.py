import discord
from discord.ext import commands
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

@client.event
async def on_ready():
    print("Ready!")

@slash.slash(name="reload", description="Reloads all commands.", guild_ids=guild_ids)
async def function(ctx):
    await ctx.send(f"Reloadano {len(os.listdir('./cogs'))} komandi.", hidden= True)
    os.execv(sys.executable, ['python'] + sys.argv)
        
@slash.slash(name="command", description="Manipuliraj komandama | Add treba sve parametre, Remove treba name, List ne treba nista.", guild_ids=guild_ids, options=[
               create_option(
                 name="operator",
                 description="Add, Remove, List",
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
                    name="list",
                    value="List"
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
            await ctx.send(f'Komanda `{name}` editovana.', hidden=True)
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
    if operator == "List":
        f = []
        for p in pathlib.Path('./cogs').iterdir():
            if p.is_file():
                f.append(p)
        f = [str(e) for e in f]
        f = [e[5:-3] for e in f]
        f.remove('default')
        output = "`"+"`, `".join(f) +"`"
        await ctx.send(f"Lista svih komandi: {output}", hidden= True)
        
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('default'):
        client.load_extension(f'cogs.{filename[:-3]}')
        

client.run(TOKEN)
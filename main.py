#Bot is incomplete still in process
import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re
import random
import asyncio
import aiohttp
from PIL import Image
from io import BytesIO
intents = discord.Intents.default()
intents.members = True
from PIL import ImageFont
from PIL import ImageDraw 
import json
WEBHOOK_URL = "<redacted>"

from aiohttp import ClientSession
bot = commands.Bot(command_prefix='s-', intents=intents)

bot.remove_command('help')
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Valorant Customs", url=""))
    print('Bot Ready')

@bot.command('ValCustoms')
async def ValCustoms(ctx):
  channel = bot.get_channel(763588828615147524)
  Moji = await channel.send("Choose Your Position")
  reaction1 = "<:Players:863975801044992063>"
  reaction2 = "<:Spectators:863975801509511238>"
  reaction3 = "<:Subs:863975801808748575>"
  reaction4 = "❌"
  await Moji.add_reaction(emoji=reaction1)
  await Moji.add_reaction(emoji=reaction2)
  await Moji.add_reaction(emoji=reaction3)
  await Moji.add_reaction(emoji=reaction4)
attendersList = []

@bot.event
async def on_reaction_add(reaction, user : discord.Member):
  if user.bot:
        return
  else:
    playersRole = discord.utils.get(user.guild.roles, name="ValPlayers")
    if not playersRole:
        playersRole = await user.guild.create_role(name="ValPlayers")
    spectatorsRole = discord.utils.get(user.guild.roles, name="ValSpectators")
    if not spectatorsRole:
        spectatorsRole = await user.guild.create_role(name="ValSpectators")
    substitutesRole = discord.utils.get(user.guild.roles, name="ValSubstitutes")
    if not substitutesRole:
        substitutesRole = await user.guild.create_role(name="ValSubstitutes")
    channel = bot.get_channel(763588828615147524)
    members = reaction.users
    for member in members:
        attendersList.append(f"{member.display_name}#{member.discriminator}")
    await channel.send('\n'.join(attendersList))
    if str(reaction.emoji) == "<:Players:863975801044992063>":
      RolePlayers = discord.utils.get(user.guild.roles, name="ValPlayers")
      role = RolePlayers
      if role in user.roles:
          await user.remove_roles(role) #removes the role if user already has
          await channel.send(f"Removed {role} from {user.mention}")
      else:
          await user.add_roles(role) #adds role if not already has it
          await channel.send(f"Added {role} to {user.mention}")
    if str(reaction.emoji) == "<:Spectators:863975801509511238>":
      RoleSpectators = discord.utils.get(user.guild.roles, name="ValSpectators")
      role2 = RoleSpectators
      if role2 in user.roles:
          await user.remove_roles(role2) #removes the role if user already has
          await channel.send(f"Removed {role2} from {user.mention}")
      else:
          await user.add_roles(role2) #adds role if not already has it
          await channel.send(f"Added {role2} to {user.mention}") 
    if str(reaction.emoji) == "<:Subs:863975801808748575>":
      RoleSubstitutes = discord.utils.get(user.guild.roles, name="ValSubstitutes")
      role3 = RoleSubstitutes
      if role3 in user.roles:
          await user.remove_roles(role3) #removes the role if user already has
          await channel.send(f"Removed {role3} from {user.mention}")
      else:
          await user.add_roles(role3) #adds role if not already has it
          await channel.send(f"Added {role3} to {user.mention}") 
    if str(reaction.emoji) == "❌":
      RoleValPlayers = discord.utils.get(user.guild.roles, name="ValPlayers")
      role = RoleValPlayers
      RoleValSpectators = discord.utils.get(user.guild.roles, name="ValSpectators")
      role2 = RoleValSpectators
      RoleValSubstitutes = discord.utils.get(user.guild.roles, name="ValSubstitutes")
      role3 = RoleValSubstitutes
      if role or role2 in user.roles:
          if role in user.roles:
            await user.remove_roles(role) #removes the role if user already has
            await channel.send(f"Removed {role} from {user.mention}")
          if role2 in user.roles:
            await user.remove_roles(role2) #removes the role if user already has
            await channel.send(f"Removed {role2} from {user.mention}")
          if role3 in user.roles:
            await user.remove_roles(role3) #removes the role if user already has
            await channel.send(f"Removed {role3} from {user.mention}")
      else:
          await channel.send(f"{user.mention} does not have any ValCustoms roles ") 

@bot.command(pass_context=True)
async def host(ctx):
  embed=discord.Embed(color=0xa64dfb)
  embed.set_author(name="Valorant Customs")
  embed.set_thumbnail(url="https://i.ibb.co/fC7DPr3/valcustoms.png")
  embed.add_field(name="Attackers", value="attackersList", inline=True)
  embed.add_field(name="Defenders", value="defendersList", inline=True)
  embed.set_footer(text="Scheduled for: Hosted by:")
  await ctx.send(embed=embed)

@bot.command()
async def join(ctx):
    member = ctx.message.author
    with open('customs.json', 'r') as f:
        lines = json.loads(f.read())
        lines['allies'].append(member.id)
    with open('customs.json', 'w') as f:
        f.write(json.dumps(lines))
    
@bot.command('role')
@commands.has_permissions(administrator=True) #permissions
async def role(ctx, user : discord.Member, *, role : discord.Role):
  if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
    return await ctx.send('**:x: | That role is above your top role!**') 
  if role in user.roles:
      await user.remove_roles(role) #removes the role if user already has
      await ctx.send(f"Removed {role} from {user.mention}")
  else:
      await user.add_roles(role) #adds role if not already has it
      await ctx.send(f"Added {role} to {user.mention}") 

@bot.event
async def on_reaction_add(reaction, user):
  ChID = 763588828615147524
  if reaction.message.channel.id != ChID:
    return
  if reaction.emoji == "<:ValAttackers:861815904630341652>":
    RoleValAttackers = discord.utils.get(user.server.roles, name="ValAttackers")
    await bot.add_roles(user, RoleValAttackers)
  if reaction.emoji == "<:ValDefenders:861815904891174972>":
    RoleValDefenders = discord.utils.get(user.server.roles, name="ValDefenders")
    await bot.add_roles(user, RoleValDefenders)







bot.run("TOKEN")
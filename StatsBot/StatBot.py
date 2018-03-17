import json
import urllib.request
import string
import discord
import planetside
#import overwatch
#overwatch API non-existent, depreciated feature.
from discord.ext import commands


bot = commands.Bot(command_prefix="!", description="Test Bot Python")

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)

@bot.command()
#Test Shenanigans
async def hello():
    await bot.say('Hello')


@bot.command()
#Cause fuck rarity
async def Tired():
    await bot.say("Fuck Off")


@bot.command()
async def PS2Summary(character):
    charSummary,charObject = planetside.returnCharacter(character)
    if int(charObject.charID) > 0:
        await bot.say(charSummary)
    else:
        await bot.say("Invalid Character")

@bot.command()
async def PS2Stat(character,stat):
    requestedStat, charObject = planetside.returnStat(character,stat)
    if requestedStat == "Invalid":
        await bot.say("That is not a valid stat")
    elif int(charObject.charID) > 0:
        await bot.say("Character: " + charObject.name)
        await bot.say(requestedStat)
    else:
        await bot.say("Invalid Character")
        
@bot.command()
#Give the list of PS2 Stats Supported
async def PS2StatOptions():
    await bot.say("""
Please choose a stat to look up from this list
=============
[0] Name
[1] Faction
[2] CreationDate
[3] LastSave
[4] LastLogin
[5] PercentToCert
[6] PlayTime
[7] EarnedCerts
[8] GiftedCerts
[9] CurrentCerts 
[10] SpentCerts
[11] BattleRank
[12] DailyRibbons
[13] CharacterID
[14] Kills
[15] Deaths
[16] KD
[17] Accuracy - Currently Highly Innacurate
=============
""")
    
@bot.command()
async def PS2Help():
    await bot.say('''
For a single stat:
!PS2Stat [Char Name] [Stat]

For a summary of a player:
!PS2Summary [Char Name]

For a list of stat choices:
!PS2StatOptions
''')


bot.run("NDE5MjY3NjkxMTE5OTAyNzIx.DXt2eQ.DMgoAgR63bfWPA3-0Zz3MUyzLcs")


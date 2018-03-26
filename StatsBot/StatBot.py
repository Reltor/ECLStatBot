import json
import urllib.request
import string
import discord
import planetside
from discord.ext import commands

# Dependecies:
# - discord.py
# - planetside.py

bot = commands.Bot(command_prefix="!", description="Test Bot Python")

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)


#########################
# Generic Commands #
#########################

@bot.command()
#Test Shenanigans
async def hello():
    await bot.say('Hello')


@bot.command()
#Cause fuck rarity
async def Tired():
    await bot.say("Fuck Off")

#########################
# Planetside 2 Statistics - Help Commands #
#########################

@bot.command()
async def PS2Help():
    embedContent = '''
For a single stat:
!PS2Stat [Char Name] [Stat]

For a summary of a player:
!PS2Summary [Char Name]

For a list of stat choices:
!PS2StatOptions

For links to several useful stat sites
!PS2StatSites [Char Name]
'''
    helpEmbed = discord.Embed(title="Commands",description = embedContent)
    await bot.say(embed=helpEmbed)

@bot.command()
#Give the list of PS2 Stats Supported
async def PS2StatOptions():
    embedContent = """
Please choose a stat to look up from this list
=============
[0] Name
[1] Factio
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
"""
    statEmbed = discord.Embed(title="Commands",description=embedContent)

    await bot.say(embed=statEmbed)
    

#########################
# Planetside 2 Statistics - Functional Commands #
#########################
    
@bot.command()
async def PS2Summary(character):
    charSummary,charObject = planetside.returnCharacter(character)
    NCLogo = "https://cdn.discordapp.com/emojis/383872674826551296.png?v=1"
    VSLogo = NCLogo
    TRLogo = NCLogo
    if int(charObject.charID) > 0:
        if charObject.faction ==  "Terran Republic":
            embedImage = TRLogo
        elif charObject.faction == "Vanu Sovereignty":
            embedImage  = VSLogo
        elif charObject.faction == "New Conglomerate":
            embedImage = NCLogo
        summaryEmbed = discord.Embed(description = charSummary,icon_url=embedImage)
        summaryEmbed.set_author(name="Summary",icon_url=VSLogo)
        await bot.say(embed = summaryEmbed)
    else:
        await bot.say("Invalid Character")

@bot.command()
async def PS2Stat(character,stat):
    requestedStat, charObject = planetside.returnStat(character,stat)
    if requestedStat == "Invalid":
        await bot.say("That is not a valid stat")
    elif int(charObject.charID) > 0:
        requestEmbed = discord.Embed(title = "Character: " + charObject.name, description = requestedStat)
        await bot.say(embed = requestEmbed)
    else:
       await bot.say("Invalid Character")

@bot.command()
async def PS2StatSites(charName):
    goodName, daLink, fisuLink, planetstatsLink = planetside.characterSites(charName)
    messageBody = ("Character Name: " + charName + "\n" +
                   "Dasanfall: " + daLink + "\n" +
                   "Fisu: " + fisuLink + "\n" +
                   "Planetstats.net: " + planetstatsLink + "\n")
    if goodName == True:
        siteEmbed = discord.Embed(title="Stat Sites", description = "")
        siteEmbed.add_field(name="Fisu",value="[" + fisuLink + "](http://" + fisuLink + ")")
        siteEmbed.add_field(name="Dasanfall",value="[" + daLink + "](http://" + daLink + ")")
        siteEmbed.add_field(name="PlanetStats.net",value="[" + planetstatsLink + "](http://" + planetstatsLink + ")")
        await bot.say(embed=siteEmbed)
    else:
        await bot.say("That is not a valid character, enjoy Therum's stats instead")
        siteEmbed = discord.Embed(title="Stat Sites", description = messageBody)
        await bot.say(embed=siteEmbed)
        
        
@bot.command()
async def outfit(tag):
    if len(tag) <5 and len(tag) > 0:
        try:
            str(tag)
            summary = planetside.outfitSummary(tag)
            outfitEmbed = discord.Embed(description = summary)
            await bot.say(embed = outfitEmbed)
        except ValueError:
            await bot.say("Invalid Tag")


bot.run("NDE5MjY3NjkxMTE5OTAyNzIx.DXt2eQ.DMgoAgR63bfWPA3-0Zz3MUyzLcs")


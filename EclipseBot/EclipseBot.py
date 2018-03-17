import discord
from discord.ext import commands
import logging
logging.basicConfig(level=logging.INFO)

#To add this bot paste the URL: https://discordapp.com/oauth2/authorize?client_id=421878199224369152&scope=bot&permissions=0

bot = commands.Bot(command_prefix="?", description="EclipseBot")

@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)


@bot.command()
async def ECLGames():
    await bot.say('''
Terran Eclipse plays numerous games including:
- Warframe (PvE MMO Shooter)
- Overwatch (PvP Arena Shooter)
- Stellaris (Sci-Fi 4x Strategy Game)

Others of note are:
- Space Engineers
- PUBG
- Ashes of Creation (currently in closed Alpha)
''')

@bot.command()
async def ECLLeaders():
    await bot.say('''
ECL has two overall leads:
- Reltor (@Reltor#3675)
- MadMatt (@MadMatt#2481)

ECL also has four officers:
- LRS (@LRS#8135)
- Warlord Mike (@Warlord Mike#8387)
- LilMissRarity (@LilMissRarity#3959)
- BlueBrr (@BlueBrr#8700)
''')


@bot.command()
async def ECLRanks():
    await bot.say('''
The Ranks in our community are as follows (lowest to highest)

1) Trial Member: Entry Rank, subject to removal for inactivity

2) Member: Requires one month of active participation in the community

3) Veteran: Requires 5 months from the date you become a full member

4) Pillar of the Community: This is a subjectively chosen rank, selected based on longtime members
we feel represent everything we are looking for in a member, fully and consistently.
You must also have been a member for at least a year.

5) Officer: Another subjective rank, chosen as needed to fill specific roles.

6) Outfit Lead: Consists of the Outfits Founder (Reltor) and the XO MadMatt

* The Founder rank is only given to the first 4 months or so of members from our founding.
''')

@bot.command()
async def reltorTime(timeEST):
    try:
        hour = int(timeEST[:2])
        minute = int(timeEST[-2:])
        if timeEST[2] == ":" and len(timeEST) == 5 and hour >= 0 and hour <= 24 and minute >= 0 and minute <= 60:
            timePST = str(hour - 3) + ":" + str(minute)
            timeMT = str(hour - 2) + ":" + str(minute)
            timeCST = str(hour -1) + ":" + str(minute)
            await bot.say("Time EST: " + timeEST + "\n" +
                          "Time CST: " + timeCST + "\n" +
                          "Time MT: " + timeMT + "\n" +
                          "Time PST: " + timePST)
        else:
            await bot.say("Invalid Time")
    except IndexError:
        await bot.say("Invalid Time")
    

                 
                


bot.run("NDIxODc4MTk5MjI0MzY5MTUy.DYTojw.EnUT9ZIIh4WwMc8H_SvHrwuwEC8")

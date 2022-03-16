import discord
import keepBotAlive
import os
import logging
from playerStatsQueryFunction import playerStatsQuery
from teamStatsQueryFunction import teamStatsQuery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from ohmysportsfeedspy import MySportsFeeds

msf = MySportsFeeds(version="2.0")

msfToken = os.environ['MSF_TOKEN']
msf.authenticate(msfToken, "MYSPORTSFEEDS")

errorMessage = "Sorry I didn't understand that. Format commands like <!stats firstname-lastname stat> or <!stats lastname stat>. If a player's name has a space in it don't use spaces. A list of stats you can call are available at dingerstats.com/discordbot"

teamList = ['bal','bos','nyy','tb','tor','cws','cle','det','kc','min',
'hou','laa','oak','sea','tex','atl','mia','nym','phi','was','chc','cin',
'mil','pit','stl','ari','col','lad','sd','sf']

def pStatsQuery(playerName, stat):
  "Queries MSF to get requested stat for requested player."
  output = msf.msf_get_data(version='2.0',
                           league='mlb',
                           season='2021-regular',
                           feed = 'seasonal_player_stats',
                           player=playerName,
                           stats=stat,
                           format = 'json')
  return output;

def tStatsQuery(team, stat):
  "Queries MSF to get requested stat for requested player."
  output = msf.msf_get_data(version='2.0',
                           league='mlb',
                           season='2021-regular',
                           feed = 'seasonal_team_stats',
                           team=team,
                           stats=stat,
                           format = 'json')
  return output;



keepBotAlive.awake()#so bot doesn't leave server when under inactivity
client = discord.Client()

@client.event

async def on_ready():
    print('We have logged in as '+str(client)) #Once bot is established in the server, let us know!

@client.event
async def on_message(message):
    if message.author == client.user: #dont respond to a message sent by the bot. 
        return
    if(message.content.startswith('!stats')):
        author = message.author
        guild = message.guild
        content = message.content
        logger.info(guild)
        logger.info(author)
        logger.info(content)

        # split the messsage into pieces. the message should
        # be written !stats [player] [stat]
        msgSplit = message.content.split()
        if len(msgSplit) <= 2:
          resp = errorMessage
        else:
          if any([i == str.lower(msgSplit[1]) for i in teamList]):
            msfReturn = tStatsQuery(msgSplit[1], msgSplit[2])
            resp = teamStatsQuery(msfReturn, errorMessage)
          else:
            msfReturn = pStatsQuery(msgSplit[1], msgSplit[2])
            resp = playerStatsQuery(msfReturn, errorMessage)
          # do playerStatsQuery return a resp
          #resp = playerStatsQuery(msfReturn, errorMessage)
          #resp = msfReturn
 #removes the identifier numbers that discord adds to your username 
        await message.channel.send(resp)
        
client.run(os.getenv('DISCORD_TOKEN')) #used to keep your bot token safe from other users

"""
This boilerplate code can be used for any python discord bot.
It even has a couple of nifty features!:
    -A keep alive function to make sure your bot doesn't leave your server . (activate by using @mat1 pinger website: https://ping.matdoes.dev/)
    -Environement Variable to keep your data safe.
Enjoy!
"""
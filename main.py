import discord
import keepBotAlive
import os
import logging
from playerStatsQueryFunction import playerStatsQuery
from teamStatsQueryFunction import teamStatsQuery
from replit import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

from ohmysportsfeedspy import MySportsFeeds

msf = MySportsFeeds(version="2.0")

msfToken = os.environ['MSF_TOKEN']
msf.authenticate(msfToken, "MYSPORTSFEEDS")

errorMessage = "Stat unavailable. For more information visit https://dingerstats.com/discordbot"

db['link'] = 'https://img1.wsimg.com/isteam/ip/6e90862e-61a0-4f91-bbf9-dff00ad964ee/20220418all_games-0002.png/:/cr=t:0%25,l:0%25,w:100%25,h:100%25/rs=w:1280'

teamList = ['bal','bos','nyy','tb','tor','cws','cle','det','kc','min',
'hou','laa','oak','sea','tex','atl','mia','nym','phi','was','chc','cin',
'mil','pit','stl','ari','col','lad','sd','sf']

def pStatsQuery(playerName, stat):
  "Queries MSF to get requested stat for requested player."
  output = msf.msf_get_data(version='2.1',
                           league='mlb',
                           season='2022-regular',
                           feed = 'seasonal_player_stats',
                           player=playerName,
                           stats=stat,
                           format = 'json')
  return output;

def tStatsQuery(team, stat):
  "Queries MSF to get requested stat for requested player."
  output = msf.msf_get_data(version='2.1',
                           league='mlb',
                           season='2022-regular',
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


    if(message.content.startswith('!123!@#qweQWEasdASD')):
      author = message.author
      guild = message.guild
      content = message.content
      logger.info(guild)
      logger.info(author)
      logger.info(content)
      msgSplit = message.content.split()
      db['link'] = msgSplit[1]
      
    if(message.content.startswith('!dingerstats')):
      resp = db['link']
      author = message.author
      guild = message.guild
      content = message.content
      logger.info(guild)
      logger.info(author)
      logger.info(content)
      await message.channel.send(resp)




client.run(os.getenv('DISCORD_TOKEN')) #used to keep your bot token safe from other users

"""
This boilerplate code can be used for any python discord bot.
It even has a couple of nifty features!:
    -A keep alive function to make sure your bot doesn't leave your server . (activate by using @mat1 pinger website: https://ping.matdoes.dev/)
    -Environement Variable to keep your data safe.
Enjoy!
"""
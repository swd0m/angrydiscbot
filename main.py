import discord
import os
import requests
import json
import random
from replit import db
from keepalive import keepalive


client= discord.Client()

positive_word=["happy","nice","sweet","good"]

pissing_message=[
  "Fuck Off!",
  "Such a bitch!",
  "Little Prick.",
  "Son of a bitch.",
  "Jerk Off!"
]

greetings=[
  "Hey there punk!",
  "Someone fucked a stary dog or what?",
  "Why u smell like piss?",
  "Someone give me a sleep mask!!",
  "What, your dick is lost?",
  "What the fuck you want?"
]

if "Responding" in db.keys():
  db["Responding"] = True

helplist="Press >hello to get a greet.\nPress >insult to get a insult.\nPress >cnjoke to get a Chuck Norris Joke.\nPress >new to add a new User Piss Txt.\nPress >del to delete a User Piss Txt"

#function to get a quote
def get_quote():
  response=requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
  json_data=response.json()
  insult=json_data["insult"]
  return(insult)

#function to get a chucknorris joke
def get_jokes():
  result=requests.get('http://api.icndb.com/jokes/random')
  data = json.loads(result.text)
  return(data["value"]["joke"])

def update_pisslist(vulg_txt):
  if "pissing" in db.keys():
    pissing= db["pissing"]
    pissing.append(vulg_txt)
    db["pissing"]=pissing

  else:
    db["pissing"]=[vulg_txt]

def delete_pisslist(index):
  pissing= db["pissing"]
  if len(pissing)>index:
    del pissing[index]
    db["pissing"]=pissing

#default on ready message
@client.event
async def on_ready():
  print('Currently logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return


  #a default greet
  if message.content.startswith('>hello'):
    await message.channel.send(random.choice(greetings))


  if message.content.startswith('>help'):
    await message.channel.send(helplist)


  #here comes the funny part
  if message.content.startswith('>insult'):
    insult=get_quote()
    await message.channel.send(insult)


  #here comes more fun
  if message.content.startswith('>cnjoke'):
    reply= get_jokes()
    await message.channel.send(reply)

  # if db["Responding"]:
  choices = pissing_message
  if "pissing" in db.keys():
    choices.extend(db["pissing"])

  #code for pisslist trigger
  if any (word in message.content for word in positive_word):
    await message.channel.send(random.choice(choices))


  if message.content.startswith('>new'):
    vulg_txt = message.content.split(">new ",1)[1]
    update_pisslist(vulg_txt)
    await message.channel.send("Entry Accepted!")


  if message.content.startswith('>del'):
    pissing=[]
    if "pissing" in db.keys():
      index=int(message.content.split(">del ",1)[1])
      delete_pisslist(index)
      pissing = db["pissing"]

    await message.channel.send(pissing)


  # if message.content.startswith(">Switch"):
  #   value= message.content.split(">Switch ",1)[1]

  #   if value.lower()== "true":
  #     db["Responding"]= True
  #     await message.channel.send("Responding Is On!!")

  #   else:
  #     db["Responding"]= False
  #     await message.channel.send("Responding Is Off!!")

keepalive()

client.run(os.getenv('rc1token'))

# some required libraries - use: pip install discord.py python-dotenv requests beautifulsoup4 tzlocal
import os, discord, asyncio as aio, random as rand
from cryptoPrice import prices # ./cryptoPrice.py
from walletFile import save, load # ./walletFile.py
from time import sleep
from os.path import dirname
from datetime import datetime as datet
from timeit import default_timer as dt
from dotenv import dotenv_values as dev

intents=discord.Intents.all()
client=discord.Client(intents=intents,max_messages=1024)
token=dict(dev(".env"))["token"]

@client.event
async def on_ready():
    print(f"Loading client-wide vars...")
    # client-wide variables
    client.mServer=client.get_guild(907747101029593098) # the management server
    client.logChannel=client.mServer.get_channel(907747101029593101) # log channel
    client.wallets=load() # this bot uses a json file to store members' wallets (e.g. {123456:{"bitcoin":"<addr>", "ethereum":"0x<addr>", ...}})
    
    # an awful way of aggregating all currencies
    client.currencies=[]
    for userWallet in client.wallets:
        for currency in userWallet:
            if currency not in client.currencies:
                client.currencies+=[currency]

    # bot statistics
    servers=client.guilds
    memberList=[]
    for server in servers:
        for member in server.members:
            if member.id not in memberList and not member.bot:
                memberList+=[member.id]

    print(f"Sucessfully connected to {len(servers)} servers!\nServing {len(memberList)} unique members!\nStarting main loop...")

    while 1:
        try:
            dt_=datet.now().strftime("%m/%d/%Y %H:%M:%S")
            client.currentPrices=prices(client.currencies)

            await aio.sleep(30)
        except:
            print(f"Encountered an error at {dt_}, sleeping for 60s...")
            await aio.sleep(60)

    return

@client.event
async def on_message(message: discord.Message):
    channel_=message.channel
    author_=message.author
    dt_=datet.now().strftime("%m/%d/%Y %H:%M:%S") # get current time/date

    if author_.bot: return # prevents the bot from interacting with other bots

    if message.content.startswith('!'):
        command=message.content[1:].split(" ") # extract the command word for word

        if message.guild==client.mServer:
            if command[0]=="test":
                await channel_.send(f"Sucessfully tested!")
                return

            elif command[0].startswith("disco"):
                # !disco(nnect) - disconnects all bot clients that may be running on the token
                await client.logChannel.send(f"```{dt_} - disconnected```")
                return
        
        else:
            if command=="wallet":
                # !wallet [add/remove] [currency] [address] - adds or removes a crypto wallet via public key
                # !wallet ? - queries all of the user's wallets
                if len(command)<4 or command[1]!='?':
                    await message.reply(f"Invalid command usage. Expected `!wallet [add/remove] [currency] [address]` or `!wallet ?`", mention_author=False)
                else:
                    if command[1]=='?' and author_.id in client.wallets:
                        # outputs a list of currencies in the user's wallet 
                        query="\n".join("{currency} : ${client.currencies[currency]}" for currency in client.wallets[author_.id])
                        await message.reply(f"Here you are, {author_.display_name}```\n{query}```", mention_author=False)
                    elif command[1]=="add":
                        pass
                    elif command[1]=="remove":
                        pass
                    else:
                        await message.reply(f"You do not have any wallets linked. Please use `!wallet add [currency] [address]`", mention_author=False)


client.run(token)

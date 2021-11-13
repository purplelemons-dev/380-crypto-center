# some required libraries - use: pip install discord.py python-dotenv requests beautifulsoup4 tzlocal
import os, discord, asyncio as aio, random as rand
from cryptoPrice import prices # ./cryptoPrice.py
from walletFile import save, load # ./walletFile.py
from cryptoAddressResolver import addrRes, priceToInt
from datetime import datetime as datet
from timeit import default_timer as dt
from dotenv import dotenv_values as dev

intents=discord.Intents.all()
client=discord.Client(intents=intents)
token=dict(dev(".env"))["3cctoken"]

@client.event
async def on_ready():
    print(f"Loading client-wide vars...")
    # client-wide variables
    client.mServer=client.get_guild(907747101029593098) # the management server
    client.logChannel=client.mServer.get_channel(907747101029593101) # log channel
    client.wallets=load() # this bot uses a json file to store members' wallets (e.g. {123456:{"bitcoin":"<addr>", "ethereum":"0x<addr>", ...}})
    client.mainActive=True

    # an awful way of aggregating all currencies
    client.currencies=[]
    for userWallet in client.wallets:
        for currency in client.wallets[userWallet]:
            if currency not in client.currencies:
                client.currencies+=[currency]

    # bot statistics
    servers=client.guilds
    memberList=[]
    for server in servers:
        for member in server.members:
            if member.id not in memberList and not member.bot:
                memberList+=[member.id]

    # sucess message
    print(f"Sucessfully connected to {len(servers)} servers!\nServing {len(memberList)} unique members!\nMain loop...")

    # main loop that catches errors - this is a bit tricky to escape out of--especially when `client.close()` is called
    while client.mainActive:
        
        try:
            # print statement below used for debugging
            dt_=datet.now().strftime("%m/%d/%Y %H:%M:%S")
            client.currentPrices=prices(client.currencies)

            # sleep so as to not anger blockchair.com for ddosing them
            await aio.sleep(20)
        except:
            print(f"Encountered an error at {dt_}, sleeping for 60s...")
            await aio.sleep(60)

    # disconnect bot
    save(client.wallets)
    dt_=datet.now().strftime("%m/%d/%Y %H:%M:%S")
    await client.logChannel.send(f"```{dt_} - disconnected```")
    await client.close()


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
                # usage:
                # - !test - very useful, helps identify how many clients are running and can help with debugging.
                await channel_.send(f"Sucessfully tested!")
                return

            elif command[0].startswith("disco"):
                # usage:
                # - !disco(nnect) - disconnects all bot clients that may be running on the token

                await client.logChannel.send(f"```{dt_} - preparing to disconnect...```")
                print("Preparing to disconnect...")
                client.mainActive=False
                return

        if command[0]=="wallet":
            # usage:
            # - !wallet [add/remove] [currency] [address] - adds or removes a crypto wallet via public key
            # - !wallet ? - queries all of the user's wallets
            if command[1]=='?' and author_.id in client.wallets:
                m=await message.reply(f"{author_.display_name}, working on that for you...", mention_author=False)
                # outputs a list of currencies in the user's wallet
                    
                # create a temporary price dictionary
                tempPrices={currency:addrRes(client.wallets[author_.id][currency],currency) for currency in client.wallets[author_.id]}
                # append 
                query="\n".join(f"{currency} : ${tempPrices[currency]}" for currency in tempPrices)

                # total wallet balance... very long line of code...
                #print(client.currentPrices['ethereum'])
                total=sum(priceToInt(tempPrices[currency]) for currency in tempPrices)
                query+=f"\nTOTAL : ${total}"
                        
                await m.edit(content=f"Here you are, {author_.display_name}```\n{query}```",allowed_mentions=discord.AllowedMentions.none())
            
            elif command[1]=="add":
                m=await message.reply(f"{author_.display_name}, working on that for you...", mention_author=False)
                # extracts the currency
                cur=message.content.split("add")[-1].strip().split(" ")[0]
                # extracts the address
                addr=message.content.split("add")[-1].split(" ")[-1]

                client.wallets[author_.id][cur]=addr

                await m.edit(content=f"{author_.display_name}, your wallet at address `{addr}` from the \"{cur}\" currency is worth `${addrRes(addr,cur)}`\nIf that's not correct, check your spelling and issue the command again.",allowed_mentions=discord.AllowedMentions.none())

            elif command[1]=="remove" and len(command)==3:
                m=await message.reply(f"{author_.display_name}, working on that for you...", mention_author=False)
                # extracts the currency
                cur=message.content.split("remove")[-1].strip().split(" ")[0]

                # removes the listed currency from the wallet
                client.wallets[author_.id].pop(cur)

                await m.edit(content=f"Removed {cur} from your list of wallets.",allowed_mentions=discord.AllowedMentions.none())

            elif len(client.wallets[author_.id])==0:
                await message.reply(f"You do not have any wallets linked. Please use `!wallet add [currency] [address]`", mention_author=False)
            
            else:
                await message.reply(f"Invalid command usage. Expected `!wallet [add/remove] [currency] [address]` or `!wallet ?`", mention_author=False)


# run bot until there is either an external interupt or an internal disconnect request.
client.run(token)

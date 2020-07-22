# bot.py
import os
import json
import datetime
import asyncio
import discord
import discord.ext
from dotenv import load_dotenv

load_dotenv()
# Use TESTING_BOT for the bot user dedicated to testing
# and DISCORD_TOKEN for the real bot user
TOKEN = os.getenv('DISCORD_TOKEN')
# Use CHANNEL_ID_TEST for test channel
# and CHANNEL_ID for real channel
CHANNEL_ID = os.getenv('CHANNEL_ID')
client = discord.Client()


async def check_birthday():
    await client.wait_until_ready()
    bd_channel = client.get_channel(int(CHANNEL_ID))

    #if curhour == int(9):
    while not client.is_closed():
        now = datetime.datetime.now()
        curmonth = int(now.strftime("%m"))
        curday = int(now.strftime("%d"))
        curhour = now.strftime("%H")
        curmin = now.strftime("%M")

        if int(curhour) == 9:
            with open("birthdays.json") as file:
                data = json.load(file)
                for element in data:
                    month = data[element]['month']
                    day = data[element]['day']
                    if month == curmonth and day == curday:
                        pass
                        await bd_channel.send(f"It's <@{element}>'s birthday today!")
            print('Birthday checked!')
            await asyncio.sleep(864390)  # task runs every day
        else:
            print(f"Process 'check birthday' ran command at {curhour}:{curmin}")
            await asyncio.sleep(3600)  # wait for an hour before checking again 'if int(curhour)' again


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('birthday feature added, use bbset {mm/dd} to add your birthday'))
    print(f'{client.user} has connected to Discord!')

client.loop.create_task(check_birthday())
# await asyncio.sleep(86400) # task runs every day


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(msg):
    if msg.content.startswith('whenbd'):
        msgsender = msg.author.id
        with open("birthdays.json") as file:
            data = json.load(file)
            try:
                sender = data[str(msgsender)]
                month = sender['month']
                day = sender['day']
                await msg.channel.send(f"<@{msgsender}>'s birthday is on {month}/{day}")
            except KeyError:
                await msg.channel.send("ID doesn't exist")
            file.close()

    if msg.content.startswith('bbset'):
        await msg.channel.send('`setting...`')

        try:
            liszt = msg.content.split()
            date = liszt[1].split('/')
            month = int(date[0])
            day = int(date[1])

            if month > 13 or month < 1:
                await msg.channel.send(f"`Exception error occurred.\nAborting...`")
                await msg.channel.send('Correct usage is: bbset {mm/dd}')
                return
            else:
                pass

            if month in (1, 3, 5, 7, 8, 10, 12):
                if day > 31 or day < 1:
                    await msg.channel.send(f"`Exception error occurred.\nAborting...`")
                    await msg.channel.send('Correct usage is: bbset {mm/dd}')
                    return
                else:
                    pass
            elif month in (4, 6, 9, 11):
                if day > 30 or day < 1:
                    await msg.channel.send(f"`Exception error occurred.\nAborting...`")
                    await msg.channel.send('Correct usage is: bbset {mm/dd}')
                    return
                else:
                    pass
            elif month == 2:
                if day > 29 or day < 1:
                    await msg.channel.send(f"`Exception error occurred.\nAborting...`")
                    await msg.channel.send('Correct usage is: bbset {mm/dd}')
                    return
                else:
                    pass
            else:
                await msg.channel.send(f"`Exception error occurred.\nAborting...`")
                await msg.channel.send('Correct usage is: bbset {mm/dd}')
                return
        except:
            await msg.channel.send(f"`Exception error occurred.\nAborting...`")
            await msg.channel.send('Correct usage is: bbset {mm/dd}')
            return

        msgsender = msg.author.id
        await msg.channel.send(f"<@{msgsender}>`Success!`\nBirthday was set on {month}/{day}.")

        data = {}
        data[msgsender] = []
        data[msgsender].append({
            'month': month,
            'day': day
        })

        with open("birthdays.json", "r+") as file:
            data = json.load(file)
            data[str(msgsender)] = {"month": month, "day": day}
            file.close()
            file = open("birthdays.json", "w")
            json.dump(data, file)

client.run(TOKEN)

# client.loop.create_task(search_submissions())
# if __name__ == "__main__":
#    client.run(TOKEN)
#    client.bg_task = client.loop.create_task(client.check_for_birthday())
#    print('loop started')


# bot.py
import os
import json
import datetime
import asyncio
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


async def check_birthday():
    await client.wait_until_ready()

    while not client.is_closed():
        now = datetime.datetime.now()
        curmonth = int(now.strftime("%m"))
        curday = int(now.strftime("%d"))
        curhour = now.strftime("%H")
        curmin = now.strftime("%M")

        if int(curhour) == 20:
            print(f"Process 'check_birthday' ran command at {curhour}:{curmin}")
            with open("birthdays.json") as file:
                data = json.load(file)
                for servers, users in data.items():
                    print(servers)
                    for user in users:
                        print(user)
                        month = data[servers][user]['month']
                        day = data[servers][user]['day']
                        if month == curmonth and day == curday:
                            channel_id = data[servers]['announce']['id']
                            bb_channel = client.get_channel(channel_id)
                            await bb_channel.send(f"It's <@{user}>'s birthday today!")
            print('Birthday checked!')
            await asyncio.sleep(864390)  # task runs every day
        else:
            print(f"Process 'check_birthday' ran command at {curhour}:{curmin}")
            await asyncio.sleep(3600)  # wait for an hour before checking again 'if int(curhour)' again


@client.event
async def on_ready():
    # await client.change_presence(status=discord.Status.online,
    #                     activity=discord.Game('birthday feature added, use bbset {mm/dd} to add your birthday'))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="EEEEEEEEEEEEEEE"))
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
    msgsender = msg.author.id
    server_id = msg.guild.id
    if msg.content.startswith('whenbd'):
        with open("birthdays.json") as file:
            data = json.load(file)
            try:
                sender = data[str(server_id)][str(msgsender)]
                month = sender['month']
                day = sender['day']
                await msg.channel.send(f"<@{msgsender}>'s birthday is on {month}/{day}")
            except KeyError:
                await msg.channel.send("ID doesn't exist")
            file.close()

        if msg.content.startswith('+whenbd'):
        # print(msg.author)
        liszt = msg.content.split()
        with open("birthdays.json") as file:
            try:
                if liszt[1] is not None:
                    try:
                        msgsender = msg.mentions[0].id
                        try:
                            if msg.mentions[1] is not None:
                                await msg.channel.send(f'<@{msg.author.id}>, you can only @ping 1 person at a time!')
                                return
                        except IndexError:
                            pass
                    except IndexError:
                        await msg.channel.send('`Exception error occurred, Server member not found.`'
                                               '\nPlease enter valid @username.')
                        return
            except IndexError:
                msgsender = msg.author.id
            data = json.load(file)
            try:
                sender = data[str(server_id)][str(msgsender)]
                month = sender['month']
                day = sender['day']
                await msg.channel.send(f"<@{msgsender}>'s birthday is on {month}/{day}")
            except KeyError:
                await msg.channel.send("Member doesn't exist in database. They haven't set their birthday yet.")
            file.close()

    if msg.content.startswith('+setbbchannel'):
        await msg.channel.send('`setting...`')
        channel_id = msg.channel.id

        with open("birthdays.json", "r+") as file:
            data = json.load(file)
            srvid = str(server_id)
            if srvid not in data:
                data[srvid] = {}
            data[srvid]['announce'] = {"id": channel_id, "month": 0, "day": 0}
            file.close()
            file = open("birthdays.json", "w")
            json.dump(data, file)
            await msg.channel.send(f'Successfully set **#{msg.channel.name}** as announcement channel.')

    if msg.content.startswith('+bbset'):
        await msg.channel.send('`setting...`')

        try:
            liszt = msg.content.split()
            date = liszt[1].split('/')
            month = int(date[0])
            day = int(date[1])

            if month > 13 or month < 1:
                await msg.channel.send(f"`Exception error occurred.`")
                await msg.channel.send('Correct usage is: bbset mm/dd {@another_person}')
                return
            else:
                pass
            if month in (1, 3, 5, 7, 8, 10, 12):
                if day > 31 or day < 1:
                    await msg.channel.send(f"`Exception error occurred.`")
                    await msg.channel.send('Correct usage is: bbset mm/dd {@another_person}')
                    return
                else:
                    pass
            elif month in (4, 6, 9, 11):
                if day > 30 or day < 1:
                    await msg.channel.send(f"`Exception error occurred.`")
                    await msg.channel.send('Correct usage is: bbset mm/dd {@another_person}')
                    return
                else:
                    pass
            elif month == 2:
                if day > 29 or day < 1:
                    await msg.channel.send(f"`Exception error occurred.`")
                    await msg.channel.send('Correct usage is: bbset mm/dd {@another_person}')
                    return
                else:
                    pass
            else:
                await msg.channel.send(f"`Exception error occurred.`")
                await msg.channel.send('Correct usage is: bbset mm/dd {@another_person}')
                return
        except:
            await msg.channel.send(f"`Exception error occurred.`")
            await msg.channel.send('Correct usage is: bbset mm/dd {@another_person}')
            return

        with open("birthdays.json", "r+") as file:
            data = json.load(file)
            srvid = str(server_id)
            if srvid not in data:
                data[srvid] = {}
            try:
                if liszt[2] is not None:
                    try:
                        msgsender = msg.mentions[0].id
                        try:
                            if msg.mentions[1] is not None:
                                await msg.channel.send(f'<@{msg.author.id}>, you can only @ping 1 person at a time!')
                                return
                        except IndexError:
                            pass
                    except IndexError:
                        await msg.channel.send('`Exception error occurred, Server member not found.`'
                                               '\nPlease enter valid @username.')
                        return
                    data[srvid][str(msgsender)] = {"month": month, "day": day}
            except IndexError:
                msgsender = msg.author.id
                data[srvid][str(msgsender)] = {"month": month, "day": day}
            file.close()
            file = open("birthdays.json", "w")
            json.dump(data, file)
            await msg.channel.send(f"`Success!`\nBirthday was set on **{month}/{day}** for <@{msgsender}>.")
            
            if msg.content.startswith('+help'):
                await msg.channel.send('`( {} = optional )`\n'
                               '`+bbset mm/dd {@another_person}` - to set your birthday\n'
                               '`+setbbchannel` - to set channel as birthday announcements channel\n'
                               '`+whenbd {@another_person}` - to view your registered birth date\n')

client.run(TOKEN)

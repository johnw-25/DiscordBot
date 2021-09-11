# Load os module to operate on files in project directory
import os
# Import python discord API and create client
import discord
from discord.ext import commands
import ParsingFunctions as parse

client = commands.Bot(command_prefix='!')
guild = discord.Guild

# import sqlite for database management
import DatabaseFuncs
from DatabaseFuncs import sqlite_insert

# establish connection to discord database
conn = DatabaseFuncs.connect_discord('discordDB.db')

# dot-env for grabbing global venv vars
from dotenv import load_dotenv

load_dotenv()

# Extract token from .env
botToken = os.getenv('TOKEN')
myServer = os.getenv('SERVER')


# create event
@client.event
# async function executes no matter what WHEN bot is ready
async def on_ready():
    print('Bot ready!')
    #Code block to run commands from command line
    while not client.is_closed():
        c = input("do a command\n")
        if "read_all_quotes" in c:
            command = client.get_command("read_all_quotes")
            await command()

def insert_query(message, table):
    if table == 'testTable':
        query = 'INSERT INTO ' + table + ' VALUES(' + "'" + str(69) + "'" + ',' + "'" + str(
            message.author) + "'" + ',' + "'" + str(message.created_at) + "'" + ')'
        DatabaseFuncs.write_to_table(conn, query)
        conn.commit()
        print(query)
    elif table == 'QuoteWall':
        print('worked')
    else:
        print('Undefined table. Check spelling.')


# handle event for person joining server
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


@client.event
async def on_message(message):
    message_str = str(message.content)
    if message.author != client.user:
        await client.process_commands(message)
        if message_str[0] == ' " ':
            insert_query(message, 'testTable')
        print(str(message.content) + "," + str(message.author) + "," + str(message.channel))
        return
    else:
        return


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def read_all_quotes():
    # get quote wall channel
    channel = client.get_channel(846874701003358248)
    messages = await channel.history(limit = 1000).flatten()
    for message in messages:
        context = parse.get_author(str(message.content))
        quote = parse.get_quote(str(message.content))
        date = str(message.created_at)
        quotee = str(message.author)

        # Handle case where context/author is returned empty, quote is not valid if condition met
        if not context:
            continue
        else:
            row = {'quotee': quotee, 'author': context, 'date': date, 'quote': quote}
        DatabaseFuncs.sqlite_insert(conn, 'QuoteWall', row)
    print('wrote new quotes to database')

client.run(botToken)

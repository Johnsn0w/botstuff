import discord
from discord.ext import commands
import sqlite3
import os
import requests
import io

#set up database
conn = sqlite3.connect('example.db')
csr = conn.cursor()

def check_table_exists():
    csr.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='reacts'""")
    #test = csr.fetchone()
    #print(test)
    if csr.fetchone()!=None:
        print("table exists")
    else:
        print("no table exists, creating")
        csr.execute('''CREATE TABLE reacts
                    (alias text, url text, file blob)
                    ''')

def insert_text_to_db(alias, url):
    csr.execute('''INSERT INTO reacts
    (alias, url) VALUES
    (?,?)
    ''',(alias, url))

def retrieve_from_db(alias):
    csr.execute("""SELECT alias, url, file FROM reacts WHERE alias = ?""",(alias,))
    db_result = csr.fetchall()
    if db_result == []:
        result = False
    elif db_result[0][2] != None: #if not empty
        result = db_result[0][2]
    else:
        result = db_result[0][1]
    return result

def check_exists_in_db(alias):
    """return true if exists"""
    csr.execute("""SELECT alias, url FROM reacts WHERE alias = ?""", (alias,))
    result = csr.fetchall()
    if result == []:
        return False
    else:
        return True

def check_message_type(message): #check if embed, attachment, both, or neither
    attach = message.attachments
    embed = message.embeds
    if (embed == []) and (attach == []):
        result = "nothing"
    elif (embed != []) and (attach != []):
        result = "both"
    elif embed != []:
        result = "embed"
    elif attach != []:
        result = "attachment"
    return result

def get_message_attachment(message):
    file_url = message.attachments[0].url
    request = requests.get(file_url)
    file_data = request.content
    return file_data

def insert_blob_to_db(alias, file_data):
    csr.execute("""INSERT INTO reacts
    (alias, file) VALUES
    (?, ?)
    """,(alias, file_data))


async def add_url(ctx, *args):
    """.add <keyword> <url> . Will bind the <keyword> with the <url>. Summon using .gif"""
    """add alias-string to database of space-separated alias-string pairs. only accept one space as space is the delimiter
    only allow unique entries, detect spaces greater or less than 1. return error messages when spaced format incorrect
    """
    found = False
    added_string = " ".join(args)#put all arges into one string, for the case of multiple words
    space_count = added_string.count(" ") #count spaces in added_string
    added_string_alias = added_string.split(" ")[0]  # get word before space
    if space_count > 1:
        await ctx.send("error: excess spaces. use only one space. format: <alias> <space> <string>")
    elif space_count == 0:
        await ctx.send("no space detected, please use format: <alias> <space> <string>")
    elif check_exists_in_db(added_string_alias):
        await ctx.send("alias already exists, nothing added")
    else:
        added_string_url = added_string.split(" ")[1]  # get word after the first space
        insert_text_to_db(added_string_alias, added_string_url)
        conn.commit()  # write changes to db
        await ctx.send("alias added")
    return

async def add_file(ctx, *args):
    """.add <keyword> <url> . Will bind the <keyword> with the <url>. Summon using .gif"""
    """add alias-string or alias-blob to database of alias-string and alias-blob pairs. For urls only accept one space as space is the delimiter
    only allow unique entries, detect spaces greater or less than 1. return error messages when spaced format incorrect
    """
    found = False
    added_string = " ".join(args)  # put all args into one string, for the case of multiple words
    space_count = added_string.count(" ") #count spaces in added_string
    if space_count > 0:
        await ctx.send("error: try again without extra spaces. example: .add funnycat")
    elif check_exists_in_db(added_string):
        await ctx.send("alias already exists, nothing added")
    else:
        file_data = get_message_attachment(ctx.message)
        if len(file_data) > 5000000:
            await ctx.send("File larger than max filesize of 5MB")
        elif len(file_data) < 5000:
            await ctx.send("File smaller than minimum size of 5KB")
        else:
            insert_blob_to_db(added_string, file_data)
            conn.commit()  # write changes to db
            await ctx.send("alias added")
    return

check_table_exists() #check table exists otherwise create one

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    channel = client.get_channel(671911325579870210) #specific channel
    await channel.send("React bot ready")
    print("logged in")

@client.command()
async def ping(ctx):
    """Bot says 'hi'"""
    await ctx.send("React_bot: pong")

@client.command()
async def add(ctx, *args):
    if check_message_type(ctx.message) == "nothing":
        await ctx.send("No image attachment or image url detected")
    elif check_message_type(ctx.message) == "both":
        await ctx.send("Image attachment AND url BOTH detected, please use one or the other. Not both.")
    elif check_message_type(ctx.message) == "embed":
        await add_url(ctx, *args)
    elif check_message_type(ctx.message) == "attachment":
        await add_file(ctx, *args)

@client.command()
async def gif(ctx, *args):
    """.gif <keyword>. Will return the associated url."""
    """SINCE CHANGED compare words before space in db file, return string that matches find_string"""
    find_string = " ".join(args)
    if find_string.count(" ") != 0:#check for spaces
        await ctx.send("error please omit spaces")
        return
    if check_exists_in_db(find_string) == False:
        await ctx.send("alias not found")
        return
    found_alias = retrieve_from_db(find_string)
    if isinstance(found_alias, str): #if it's a url aka string
        await ctx.send(found_alias)
    elif isinstance(found_alias, bytes):#if it's bytes aka a picture file
        filelike_object = io.BytesIO(found_alias) #convert to a object similar to a file
        discord_file_object = discord.File(filelike_object, "react.gif")
        await ctx.send(file=discord_file_object)
# @client.command()
# async def help2(ctx):
#     await ctx.send("Two modules currently."
#                    "As you may have noticed it deletes all your messages except the last one"
#                    "There's also the react module with two commands:"
#                    ".add <keyword> <url>"
#                    "This will link the <keyword> with the <url> which can then be summoned with:"
#                    ".gif <keyword>")





client.run('NjcwNDE3NDYwMjEzNzEwODc5.XiuVDA.PkxhMSP--Df3b2xyHOqF5hGEezg')
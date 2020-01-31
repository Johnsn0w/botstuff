import discord
from discord.ext import commands
import sqlite3
import os

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
                    (alias text, url text)
                    ''')

def insert(alias, url):
    csr.execute('''INSERT INTO reacts
    (alias, url) VALUES
    (?,?)
    ''',(alias, url))

def retrieve(alias):
    csr.execute("""SELECT alias, url FROM reacts WHERE alias = ?""",(alias,))
    result = csr.fetchall()
    if result == []:
        return False
    else:
        return result[0][1]

def check_exists(alias):
    """return true if exists"""
    csr.execute("""SELECT alias, url FROM reacts WHERE alias = ?""", (alias,))
    result = csr.fetchall()
    if result == []:
        return False
    else:
        return True

check_table_exists()

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("logged in")

@client.command()
async def summon(ctx):
    """Bot says 'hi'"""
    await ctx.send("hi")

@client.command()
async def parrot(ctx, *args):
    """It's a parrot"""
    await ctx.send(" ".join(args))

@client.command()
async def add(ctx, *args):
    """.add <keyword> <url> . Will bind the <keyword> with the <url>. Summon using .gif"""
    """add alias-string to database of space-separated alias-string pairs. only accept one space as space is the delimiter
    only allow unique entries, detect spaces greater or less than 1. return error messages when spaced format incorrect
    """
    found = False
    added_string = " ".join(args)#put all arges into one string, for the case of multiple words
    space_count = added_string.count(" ") #count spaces in added_string
    added_string_alias = added_string.split(" ")[0]  # get word before space
    added_string_url = added_string.split(" ")[1]

    if space_count > 1:
        await ctx.send("error: excess spaces. use only one space. format: <alias> <space> <string>")
        return
    elif space_count == 0:
        await ctx.send("no space detected, please use format: <alias> <space> <string>")
        return
    elif check_exists(added_string_alias) == True:
        await ctx.send("alias already exists, nothing added")
        return
    else:
        insert(added_string_alias, added_string_url)
        conn.commit()  # write changes to db
        await ctx.send("alias added")
        return

@client.command()
async def gif(ctx, *args):
    """.gif <keyword>. Will return the associated url."""
    """SINCE CHANGED compare words before space in db file, return string that matches find_string"""
    find_string = " ".join(args)
    if find_string.count(" ") != 0:#check for spaces
        await ctx.send("error please omit spaces")
        return
    if check_exists(find_string) == False:
        await ctx.send("alias not found")
        return
    else:
        found_alias = retrieve(find_string)
        await ctx.send(found_alias)

# @client.command()
# async def help2(ctx):
#     await ctx.send("Two modules currently."
#                    "As you may have noticed it deletes all your messages except the last one"
#                    "There's also the react module with two commands:"
#                    ".add <keyword> <url>"
#                    "This will link the <keyword> with the <url> which can then be summoned with:"
#                    ".gif <keyword>")





client.run('NjcwNDE3NDYwMjEzNzEwODc5.XiuVDA.PkxhMSP--Df3b2xyHOqF5hGEezg')
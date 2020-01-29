import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("logged in")

@client.command()
async def summon(ctx):
    await ctx.send("yo, what up")

@client.command()
async def parrot(ctx, *args):
    await ctx.send(" ".join(args))

@client.command()
async def add(ctx, *args):
    """add alias-string to database of space-separated alias-string pairs. only accept one space as space is the delimiter
    only allow unique entries, detect spaces greater or less than 1. return error messages when spaced format incorrect
    """
    found = False
    added_string = " ".join(args)
    space_count = added_string.count(" ")

    if space_count > 1:
        await ctx.send("error: excess spaces. use only one space. format: <alias> <space> <string>")
        return
    elif space_count == 0:
        await ctx.send("no space detected, please use format: <alias> <space> <string>")
        return
    else:
        with open("db.txt", "r") as db_file:
            for s in db_file.readlines():
                s = s.rstrip()  # strip newline characters
                first_word = s.split(" ")[0]  # get word before space
                added_string_first_word = added_string.split(" ")[0] # get word before space
                if added_string_first_word == first_word:  # if first word matches then return 'error alias already exists'
                    await ctx.send("alias already exists, nothing added")
                    return
    db_file = open("db.txt", "a")
    db_file.write(added_string + "\n")
    await ctx.send("alias added")

@client.command()
async def gif(ctx, *args):
    """SINCE CHANGED compare words before space in db file, return string that matches find_string"""
    find_string = " ".join(args)
    if find_string.count(" ") != 0:
        await ctx.send("error please omit spaces")
        return
    with open("db.txt", "r") as db_file:
       for s in db_file.readlines():
           s = s.rstrip() #strip newline characters
           first_word = s.split(" ")[0] #get word before space
           if find_string == first_word: #if first word matches then return second word
               await ctx.send(s.split(" ")[1])
               return
    await ctx.send("alias not found")




client.run('NjcwNDE3NDYwMjEzNzEwODc5.XiuVDA.PkxhMSP--Df3b2xyHOqF5hGEezg')
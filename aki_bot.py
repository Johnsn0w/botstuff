import akinator
import discord
from discord.ext import commands
import asyncio

client = commands.Bot(command_prefix = '.')

users_currently_running = []

@client.command()
async def aki(ctx, *args):
    """.aki - start a akinator game"""
    """akinator bot. Guesses what thing you're thinking of"""
    aki = akinator.Akinator() #?create akinator object
    question = aki.start_game() #start the game and store first question in "question" variable
    user_answer = ""
    acceptable_answers = ["yes", "no", "y", "n"]
    quit_commands = ["quit", "exit", "q"]
    global users_currently_running
    if ctx.author in users_currently_running: #check if user is already running aki
        await ctx.send(f"Akinator already running for {ctx.author}")
        return
    users_currently_running.append(ctx.author) #add user to list keeping track of who is currently running aki
    def check_author(message_author, op_author=ctx):
        return message_author.author == op_author.author
    while aki.progression <= 80: #progression tracks how close akinator is to narrowing down the answer
        await ctx.send(f"{ctx.author}: {question}") #print to terminal the <question>, store user input in answer
        answer_count = 0
        while user_answer not in acceptable_answers:  # wait for acceptable input
            if (answer_count >= 3) or (user_answer in quit_commands): #if too many answer attempts then quit
                await ctx.send(f"{ctx.author}: Game exited")
                users_currently_running.remove(ctx.author) #exiting, so remove user from currently running list
                return
            if user_answer != "": #check if it's the first time round, second time round indicates wrong input
                await ctx.send("please use 'yes' 'no'")
            answer_count += 1 #keep tabs on how many answer attempts
            try:
                user_answer = await client.wait_for('message', check=check_author,timeout=90)
                user_answer = str(user_answer.content).lower() #get the message text
            except:
                await ctx.send(f"{ctx.author}: Timed out (90 seconds), game exited.")
                users_currently_running.remove(ctx.author)  # exiting, so remove user from currently running list
                return
        question = aki.answer(user_answer) #feed akinator your answer and redefine "question" as the next question
        user_answer = ""
    aki.win() #function runs and adds akinators best guess as "name", "description", and "picture" variables accessible in the "aki" class
    await ctx.send(f"{ctx.author}: I know!, It's {aki.name}") #akibot sends its deduced guess
    users_currently_running.remove(ctx.author)  # exiting, so remove user from currently running list

async def yes_no():
    pass

@client.event
async def on_ready():
    print("logged in")

# @client.command()
# async def game(ctx, *args):
#     while "I know" not in aki_game():
#         pass



client.run('NjcwNDE3NDYwMjEzNzEwODc5.XiuVDA.PkxhMSP--Df3b2xyHOqF5hGEezg')
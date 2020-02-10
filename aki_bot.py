import akinator
import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = '.')
users_currently_running = []


@client.command()
async def aki_enable(ctx, *args):
    user_command = " ".join(args).lower()
    if "on" in user_command:
        aki_state = True
        await ctx.send("aki on")
    elif "off" in user_command:
        aki_state = False
        await ctx.send("aki off")

@client.command()
async def aki(ctx, *args):
    """.aki - start a akinator game"""
    """akinator bot. Guesses what thing you're thinking of"""
    aki = akinator.Akinator() #?create akinator object
    question = aki.start_game() #start the game and store first question in "question" variable
    user_answer = ""
    global users_currently_running
    """
    global aki_state
    if aki_state == False:
        await ctx.send("Akibot is disabled")
        return
    if aki_state == False:
        print("aki state false")
    """
    def parse_answer(answer):
        result = "invalid" #if function doesn't alter this default value then answer must be invalid
        acceptable_answers = ["yes", "no", "y", "n", "idk", "i dont know", "i don't know", "probably", "p", "probably not", "pn"]
        convertible_answers = {"yes": ["yess", "ye", "yep"],
                               "no": ["nope", "nah", "noo"],
                               "i dont know": ["not sure", "unsure", "don't know", "dont know", "maybe", "m"],
                               "probably": ["likely"],
                               "probably not": ["unlikely"]
                               }
        quit_commands = ["quit", "exit", "q"]
        if answer in acceptable_answers:
            result = answer
        elif answer in quit_commands:
            result = "quit"
        else:
            for t in convertible_answers.items():
                if answer in t[1]:#looking through each dicts respective list for matching words
                    result = t[0] #if word matches value then set result as key
        return result

    def check_author(message_author, op_author=ctx):
        return message_author.author == op_author.author

    if ctx.author in users_currently_running: #check if user is already running aki
        await ctx.send(f"Akinator already running for {ctx.author}")
        return
    users_currently_running.append(ctx.author) #add user to list keeping track of who is currently running aki

    while aki.progression <= 80: #progression tracks how close akinator is to narrowing down the answer
        await ctx.send(f"{ctx.author}: {question}") #print to terminal the <question>, store user input in answer
        answer_count = 0 #set variable to track failed answer attempts
        while (user_answer == "") or (user_answer == "invalid"):  # wait for acceptable input. empty string is first iteration. run again if answer is invalid
            try:#timeout
                user_answer = await client.wait_for('message', check=check_author,timeout=90)
                user_answer = str(user_answer.content).lower() #get the message text
                user_answer = parse_answer(user_answer)
                answer_count += 1  # keep tabs on how many answer attempts
            except:
                await ctx.send(f"{ctx.author}: Timed out (90 seconds), game exited.")
                users_currently_running.remove(ctx.author)  # exiting, so remove user from currently running list
                return
            if (answer_count >= 3) or (user_answer == "quit"): #if too many answer attempts then quit
                await ctx.send(f"{ctx.author}: Game exited")
                users_currently_running.remove(ctx.author) #exiting, so remove user from currently running list
                return
            if user_answer == "invalid": #check if parse_answer has flagged the answer as invalid
                await ctx.send("please use 'yes' 'no' 'maybe' 'probably' 'probably not' \n 'y' 'n' 'm' 'p' 'pn'")
        question = aki.answer(user_answer) #feed akinator your answer and redefine "question" as the next question
        user_answer = ""
    aki.win() #function runs and adds akinators best guess as "name", "description", and "picture" variables accessible in the "aki" class
    await ctx.send(f"{ctx.author}: I know!, It's {aki.name}") #akibot sends its deduced guess
    users_currently_running.remove(ctx.author)  # exiting as end of game, so remove user from currently running list

@client.command()
async def ping(ctx):
    await ctx.send("aki_bot:pong")

@client.event
async def on_ready():
    channel = client.get_channel(671911325579870210)
    await channel.send("Aki bot ready")
    print("logged in")

# @client.command()
# async def game(ctx, *args):
#     while "I know" not in aki_game():
#         pass

token = os.getenv("JIMBOT_TOKEN")

client.run('token')

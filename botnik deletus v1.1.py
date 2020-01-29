import discord

class MyClient(discord.Client):#?create MyClient class using the discord.import ?module
    async def on_ready(self): #event when bot is ready to do stuff
        """Print notification when logged in and ready"""
        print('Logged in')

    async def on_message(self, message):
        """
        Delete all users messages except the very last message they sent.
        When a message is received event is triggered, take message_id and author of said message
        loop through each message in the channel, if message doesn't match the message that triggered the event then
        compare with author, if it belongs to the same author then delete that message.
        """
        print(message.content)
        channel = message.channel
        member_current = message.author
        message_current = message.id
        async for m in channel.history(limit=200):
            if m.id != message_current:
                if m.author == member_current:
                    print(m.id)
                    print(message_current)
                    await m.delete()

client = MyClient()
client.run('NjcwNDE3NDYwMjEzNzEwODc5.XiuVDA.PkxhMSP--Df3b2xyHOqF5hGEezg')

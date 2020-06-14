
So this is a disarray of scripts I'm halfassedly working on as a novice learning programming. Most of these ideas have probably been made by someone else already, but I made these to learn not to be original.

There's a lot wrong with my syntax, commenting, and everything else. I have tried to make it fairly coherent but the excessive comments inline are basically just an tool for my learning and I'm sure violate basic style guidelines.

# aki_bot.py

Basically takes akinator.py and interfaces it as a bot via discord.py as a bot so users can play akinator.com in Discord.

**Start game.**


```.aki```

**Responding to bot questions during game.**


```
yes, y
no, no, n
maybe, m, i don't know, unsure, don't know
probably, p, likely
probably not, pn, unlikely
quit, q, exit
```


**Function**

Game exits via 'quit' commend, after third invalid input, or after 90 seconds timeout.

Game only takes responses from the person who started the game. This means multiple games can run at the same time.


# deletus.py

So uh careful with this one because it'll delete your entire message history.

Basically it deletes every message on the channel except the very last message you sent. 
The result being that each user only ever has one message on the server at a time.

# react.py


This is a bot designed to store images with an alias, and return those images when someone commands the bot using said alias.
It will accept a url or an attachment. Attachments are stored in sql database as binary, urls are stored as strings.
So it's purpose was for gifs, but you could use it for whatever.
 
 For example:

![react bot example](https://cdn.discordapp.com/attachments/671999623459504138/675235631105966100/gifbot_explain.png)




.  


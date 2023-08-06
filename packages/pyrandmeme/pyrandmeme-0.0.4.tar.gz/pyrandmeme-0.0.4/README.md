A simple library that gives you randomized memes. This is useful for discord.py or anything else included with bots.

For discord.py your code would look like this:

```
from discord.ext import commands
from pyrandmeme import *


client = commands.Bot(command_prefix="(Add prefix here)")


@client.command()
async def meme(ctx):
    await ctx.send(embed=await pyrandmeme())

client.run(token)
```

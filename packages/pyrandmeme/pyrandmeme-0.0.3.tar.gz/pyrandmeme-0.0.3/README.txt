A simple library that gives you randomized memes. This is useful for discord.py or anything else included with bots.

For discord.py your code would look like this:

@client.command(pass_context=True)
async def teste(ctx):
    await ctx.send(embed=pymeme)
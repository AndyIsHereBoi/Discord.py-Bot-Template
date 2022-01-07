import json
import os
import platform
import random
import sys

import nextcord
from nextcord.ext import tasks, commands
from nextcord.ext.commands import Bot

import exceptions

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)
intents = nextcord.Intents.default()

bot = Bot(command_prefix=config["prefix"], intents=intents)


# The code in this even is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()


# Setup the game status task of the bot
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["with you!", "with Krypton!", "with humans!"]
    await bot.change_presence(activity=nextcord.Game(random.choice(statuses)))



# bot.remove_command("help")



@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


# The code in this event is executed every time a normal valid command catches an error
@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = nextcord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = nextcord.Embed(title="Error!", description="You are missing the permission(s) `" + ", ".join(error.missing_permissions) + "` to execute this command!", color
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = nextcord.Embed(title="Error!", description=str(error).capitalize(), color=0xE02B2B)
        await context.send(embed=embed)
    raise 


# Run the bot with the token
bot.run(config["token"])

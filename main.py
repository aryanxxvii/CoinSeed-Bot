import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
client = commands.Bot(command_prefix="cc", intents=intents)

@client.event
async def on_ready():
    print("Bot is ready")

@client.command(aliased=[" ping"])
async def ping(ctx):
    await ctx.send(f"pong {round(client.latency * 1000)}")

@client.command()
async def server(ctx):
    await ctx.send(ctx.guild.name)
    await ctx.send(ctx.guild.icon_url)
    for member in ctx.guild.members:
        await ctx.send(str(member.name) + " " + str(member.id) + " " + str(member.avatar_url))
#test
@client.command()
async def profile(ctx, user: discord.User = None):
    if user == None:
        embedVar = discord.Embed(
        title=str(ctx.author.name), description="", color = 0x5ceb48
        )
        embedVar.set_thumbnail(url=ctx.author.avatar_url)
        embedVar.add_field(name="UU Balance :coin:: ", value="3200", inline=False)
        embedVar.add_field(name="Current Bets :money_with_wings::", value="`England | 2 - 1 | 300 UU`\n`Tie | 1 - 1 | 300 UU`", inline=False)
        embedVar.add_field(name="Bets Won :thumbsup:: ", value="1", inline=False)
        embedVar.add_field(name="Euro Cup Favorite :trophy::", value="Germany:flag_de:", inline=False)
        await ctx.send(embed=embedVar)
    elif user != None:
        embedVar = discord.Embed(
        title=str(user.name), description="", color = 0x5ceb48
        )
        embedVar.set_thumbnail(url=user.avatar_url)
        embedVar.add_field(name="UU Balance :coin:: ", value="3200", inline=False)
        embedVar.add_field(name="Current Bets :money_with_wings::", value="`England | 2 - 1 | 300 UU`\n`Tie | 1 - 1 | 300 UU`", inline=False)
        embedVar.add_field(name="Bets Won :thumbsup:: ", value="1", inline=False)
        embedVar.add_field(name="Euro Cup Favorite :trophy::", value="Germany:flag_de:", inline=False)
        
        #embedVar.add_field(name="Rating :star::", value=str(score)+"/10", inline=True)
        await ctx.send(embed=embedVar)


@client.command()
async def bet(ctx):
    await ctx.send("Today's Match: A vs B\nWhich team do you want to bet on?")
    try:
        team = await client.wait_for(
            "message",
            timeout=30,
            check=lambda message: message.author == ctx.author and message.channel == ctx.channel
            )
        teamcon = team.content
        if teamcon.upper() in ["A", "B", "TIE"]:
            try:
                await ctx.send("What's your score prediction? [3 - 2]")
                score = await client.wait_for(
                    "message",
                    timeout=30,
                    check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                    )
                scorecon = score.content
                lscore = scorecon.split("-")
                ascore = int(lscore[0])
                bscore = int(lscore[1])
                try:
                    await ctx.send("Alright, how much do you want to bet? (in UU)")  #dont hardcore symbol
                    betamt = await client.wait_for(
                        "message",
                        timeout=30,
                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                        ) #check is balance is there
                    betamtcon = betamt.content
                    betinpup = betamtcon.upper()
                    betinplist = betinpup.split("UU")
                    intbetamt = int(betinplist[0])
                    await ctx.send(f"`Your Bet:{str(teamcon).capitalize()} | {str(ascore)} - {str(bscore)} | {str(intbetamt)} UU`")
                    
                except ZeroDivisionError:
                    await ctx.send("You gave wrong input \:(")

                    
                    
                    
                    
            except TypeError:
                await ctx.send("You gave wrong input \:(")

                
                
                        
                
            
    except asyncio.TimeoutError:
            await ctx.send("You did not respond.")
    


        
        
        



client.run("ODUzNTcwMjg0OTE2NTcyMTcw.YMXTRg.yVOUfaAivE9oe9hCfOx9S4aFObc")


















    

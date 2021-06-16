import discord
from discord.ext import commands
import asyncio
from sqlfunc import *
import random
from datetime import datetime, timedelta
import emoji


bot_prefix = "cc ", "<@853570284916572170> ", "<@!853570284916572170> "
intents = discord.Intents.all()
client = commands.Bot(command_prefix=bot_prefix, intents=intents)

class colors:
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5


@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def ping(ctx):
    await ctx.send(f"pong {round(client.latency * 1000)}")



@client.command()
async def server(ctx):
    await ctx.send(ctx.guild.name)
    await ctx.send(ctx.guild.icon_url)
    for member in ctx.guild.members:
        await ctx.send(str(member.name) + " " + str(member.id) + " " + str(member.avatar_url))




#-------------------------------------------------------------------------------

# [x]PERSONAL ACC CREATION
# [x]GUILD ACC CREATION
# [ ]BAL CHECK
# [x]PROFILE
# [x]DAILY
# [ ]LOANS
# [ ]CHANGE SERVER
# [ ]CHANGE SYMBOL/NAME
# [ ]TIPS

#-------------------------------------------------------------------------------


@client.event
async def on_ready():
    print("Bot is ready")
    


# AUTO GUILD ACC CREATION
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        #IF MESSAGE PERM,  TYPE THIS...
        if channel.permissions_for(guild.me).send_messages:
            await channel.send("I have joined and created this server's account.")
        break

    #CHECK IF GUILD IS IN DGUILDS
    guildexists = sql_check_exist("DGUILDS", guild.id)
    #IF EXISTS
    if guildexists:
        #PASS
        pass
    #ELSE
    elif not guildexists:
        #ADD GUILD
        sql_add("DGUILDS", guild.id, ["SeedCoin", ":coin:"])
            


# ACC CREATION
@client.command()
async def addme(ctx, *, attr=None):
    if attr == None:
        #IF MESSAGE GUILD IN DGUILDS
            userexists = sql_check_exist("DUSERS", ctx.author.id)
            if userexists:
                allcheckwhich = sql_search("DUSERS", ctx.author.id)
                #FIND USER GUILD IN DUSERS
                try:
                    userguild = allcheckwhich[0][1]
                except:
                    userguild = allcheckwhich[1]
                if userguild == ctx.guild.id:
                    await ctx.send('You have already registered your account in this server.')
                else:
                    await ctx.send("You have already registered in another server. To change your server type `cc changeserver`.")

            elif not userexists:
                try:
                    #WAIT FOR CONFIRMATION
                    await ctx.send("Are you sure you want to create your account in this server? You can only have your account registered with ONE server at a time. Type `Y` or `y` if you want to proceed.")
                    answer = await client.wait_for(
                        "message",
                        timeout=30,
                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                        )
                    ans = answer.content
                    #IF CONFIRMED
                    if ans in ["Y", 'y']:
                        now = datetime.now()
                        doc = now.strftime("%Y-%m-%d %H:%M:%S") #input
                        #CREATE ACCOUNT
                        sql_add("DUSERS", ctx.author.id, [ctx.guild.id, doc, 0, "2000-01-01 12:00:00"])
                        await ctx.send("Your account was succesfully created.")
                    else:
                        await ctx.send("Your account was not created.")
                #CHECK FOR TIMEOUT ERROR
                except asyncio.TimeoutError:
                    await ctx.send("You did not respond.")

                    
    elif attr == "bet":
        await ctx.send("This will create your betting account")




@client.command()
async def daily(ctx):
    #CHECK TIME
    try:
        fetchdata = sql_search("DUSERS", ctx.author.id)
        duid, guid, doc, cbal, cdc = fetchdata
        if ctx.guild.id == guid:
            dt_storedtime = cdc
            nextdaily = dt_storedtime + timedelta(hours=24)
            nowtime = datetime.now()
            if nowtime > nextdaily:
                amount = random.randrange(100, 600) 
                sql_addbal(ctx.author.id, amount)
                if amount in range(100, 250):
                    await ctx.send("**+{}** :coin: have been added to your account.".format(amount))
                elif amount in range(250, 450):
                    await ctx.send("Nice! **+{}** :coin: have been added to your account!".format(amount))
                elif amount in range(450, 600):
                    await ctx.send("AWESOME! **+{}** :coin: have been added to your account!!".format(amount))
                
                st_now = nowtime.strftime("%Y-%m-%d %H:%M:%S")
                sql_update_date(ctx.author.id, st_now)
                
            else:
                waittime = nextdaily - nowtime
                acttime = str(waittime).split(".")[0]
                dt_acttime = datetime.strptime(acttime, "%H:%M:%S")
                str_waittime_hour = dt_acttime.strftime("%H")
                str_waittime_min = dt_acttime.strftime("%M")
                await ctx.send("You have to wait another **{} hours {} minutes**".format(str_waittime_hour, str_waittime_min))
            
        else:
            await ctx.send("You do not have an account in this server.")
    except:
        await ctx.send("You don't have an account yet! Type `cc addme` to create one!")
    
    #IF TIME NOW GREATER THAN 24 + OL
        #ADD RANDOM BALANCE BW 100 to 500



@commands.has_permissions(ban_members=True, kick_members=True) 


@client.command(aliases=["csi"])
async def changeserverinfo(ctx):
    if ctx.author.guild_permissions.manage_guild:
        try:
            duid, guid, doc, cbal, cdc = sql_search("DUSERS", ctx.author.id)
            if guid == ctx.guild.id:
                guid, cnam, csym = sql_search("DGUILDS", ctx.guild.id)
                await ctx.send("Current Coin-Name: {}\nCurrent Coin-Symbol: {}".format(cnam, csym))
                await ctx.send("What do you want your Server's **new** Coin-Name to be?")
                try:
                    coin_inp = await client.wait_for(
                        "message",
                        timeout=30,
                        check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                        )
                    coinname = coin_inp.content
                    try:
                        await ctx.send("Alright, what do you want your Server's **new** Coin-Symbol to be?")
                        sym_inp = await client.wait_for(
                            "message",
                            timeout=30,
                            check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                            )
                        coinsym = sym_inp.content
                        
                        try:
                            st_coinsym = emoji.demojize(coinsym)
                        except:
                            st_coinsym = coinsym
                            
                        sql_guild_cngcoin(guid, coinname, st_coinsym)

                        guid, cnam, csym = sql_search("DGUILDS", ctx.guild.id)
                        servname = ctx.guild.name
                        icon_url = ctx.guild.icon_url
                       
                        
                        embedVar = discord.Embed(
                        title="{}'s Coin System Changed!".format(servname), description="", color = colors.green
                        )
                        embedVar.set_thumbnail(url=icon_url)
                        embedVar.add_field(name="New Coin-Name", value=str(cnam), inline=False)
                        embedVar.add_field(name="New Coin-Symbol", value=csym, inline=False)
                        await ctx.send(embed=embedVar)
                        
                    except asyncio.TimeoutError:
                        await ctx.send("You did not respond.")
                        
                except asyncio.TimeoutError:
                    await ctx.send("You did not respond.")                  
        except:
            await ctx.send("You don't have an account in this server!")
    else:
        await ctx.send("Sorry! You don't have the permissions!")
                    




@client.command()
async def tables(ctx, table):
    f_all = sql_show_table(table)
    for f_one in f_all:
        st_f_one = []
        for c in f_one:
            st_f_one.append(str(c))
        st_f = " | ".join(st_f_one)
        await ctx.send("`"+st_f+"`")
       

    

@client.command()
async def profile(ctx, user: discord.User = None): #ADD LOANS
    #CHECK IF USER EXISTS FIRST !!!
    if user == None:
        try:
            user_data_all = sql_search("DUSERS", ctx.author.id)
            duid, guid, doc, cbal, cdc = user_data_all
            if guid == ctx.guild.id:
                dt_storedtime = cdc
                st_doc = doc.strftime("%d-%m-%Y")
                nextdaily = dt_storedtime + timedelta(hours=24)
                nowtime = datetime.now()
                waittime = nextdaily - nowtime
                acttime = str(waittime).split(".")[0]
                dt_acttime = datetime.strptime(acttime, "%H:%M:%S")
                str_waittime_hour = dt_acttime.strftime("%H")
                str_waittime_min = dt_acttime.strftime("%M")

                name = ctx.author.name
                avatar_url = ctx.author.avatar_url
                
                embedVar = discord.Embed(
                title="{}'s profile".format(name), description="Created on {}".format(st_doc), color = colors.green
                )
                embedVar.set_thumbnail(url=avatar_url)
                embedVar.add_field(name="Coin Balance :coin:: ", value=str(cbal), inline=False)
                embedVar.add_field(name="Next Daily in :calendar:: ", value="{}h {}m".format(str_waittime_hour, str_waittime_min), inline=False)
                await ctx.send(embed=embedVar)
        except:
            await ctx.send("Your account does not exist! To create one, use `cc addme`")

    elif user != None:
        user_data_all = sql_search("DUSERS", user.id)
        duid, guid, doc, cbal, cdc = user_data_all
        try:
            st_doc = doc.strftime("%d-%m-%Y")
            dt_storedtime = cdc
            nextdaily = dt_storedtime + timedelta(hours=24)
            nowtime = datetime.now()
            waittime = nextdaily - nowtime
            acttime = str(waittime).split(".")[0]
            dt_acttime = datetime.strptime(acttime, "%H:%M:%S")
            str_waittime_hour = dt_acttime.strftime("%H")
            str_waittime_min = dt_acttime.strftime("%M")
            
            name = user.name
            avatar_url = user.avatar_url
            
            
            embedVar = discord.Embed(
            title="{}'s profile".format(name), description="Created on {}".format(st_doc), color = colors.green
            )
            embedVar.set_thumbnail(url=avatar_url)
            embedVar.add_field(name="Coin Balance :coin:: ", value=str(cbal), inline=False)
            embedVar.add_field(name="Next Daily in :calendar:: ", value="{}h {}m".format(str_waittime_hour, str_waittime_min), inline=False)
        
            await ctx.send(embed=embedVar)
    
        except:
            await ctx.send("There is no account with this name in this server.")


# CHECK 

@client.command()
async def bal(ctx):
    #disuserid, guildid, doc, coinbal, dt = search("USERS", int(ctx.author.id))
    data = sql_search("DUSERS", int(ctx.author.id))[0]
    embedVar = discord.Embed(
        title=str(ctx.author.name), description=str(ctx.author.id)+" "+str(ctx.guild.id), color = colors.green
        )
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    embedVar.add_field(name="UU Balance :coin:: ", value=str(data[3]), inline=False)
        #embedVar.add_field(name="Current Bets :money_with_wings::", value="`England | 2 - 1 | 300 UU`\n`Tie | 1 - 1 | 300 UU`", inline=False)
        #embedVar.add_field(name="Bets Won :thumbsup:: ", value="1", inline=False)
        #embedVar.add_field(name="Euro Cup Favorite :trophy::", value="Germany:flag_de:", inline=False)
    await ctx.send(embed=embedVar)
    await ctx.send(str(data))


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
                    
                except TypeError:
                    await ctx.send("You gave wrong input \:(")

                    
                    
                    
                    
            except TypeError:
                await ctx.send("You gave wrong input \:(")

                
                
                        
                
            
    except asyncio.TimeoutError:
            await ctx.send("You did not respond.")
    


        
        
        



client.run("ODUzNTcwMjg0OTE2NTcyMTcw.YMXTRg.yVOUfaAivE9oe9hCfOx9S4aFObc")


















    

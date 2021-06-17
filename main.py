import discord
from discord.ext import commands
import asyncio

import random
from datetime import datetime, timedelta
import emoji
try:
    from sqlfunc import *
except:
    print("Server Error")
    

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




#-------------------------------------------------------------------------------

# [x]PERSONAL ACC CREATION
# [x]GUILD ACC CREATION
# [ ]BAL CHECK
# [x]PROFILE
# [x]SERVER PRoFILE
# [x]DAILY
# [ ]LOANS
# [x]CHANGE SERVER
# [x]CHANGE SYMBOL/NAME
# [ ]TIPS
# [x]REMOVE HARDCODING

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
            



@client.command(aliases=["s"])
async def server(ctx):
    guid, cnam, csym = sql_search("DGUILDS", ctx.guild.id)
    gnam = ctx.guild.name
    icon_url = ctx.guild.icon_url
    
    
    embedVar = discord.Embed(
    title="{}'s Info".format(gnam), description="", color = colors.purple
    )
    embedVar.set_thumbnail(url=icon_url)
    embedVar.add_field(name="Coin-Name", value=cnam, inline=False)
    embedVar.add_field(name="Coin-Symbol", value=csym, inline=False)
    
    await ctx.send(embed=embedVar)







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




@client.command(aliases=["d"])
async def daily(ctx):
    #CHECK TIME
    try:
        fetchdata = sql_search("DUSERS", ctx.author.id)
        duid, guid, doc, cbal, cdc = fetchdata
        if ctx.guild.id == guid:
            guilddata = sql_search("DGUILDS", guid)

            
            guid, cnam, csym = guilddata

            
            dt_storedtime = cdc
            nextdaily = dt_storedtime + timedelta(hours=24)
            nowtime = datetime.now()
            if nowtime > nextdaily:
                amount = random.randrange(100, 600) 
                sql_addbal(ctx.author.id, amount)
                if amount in range(100, 250):
                    await ctx.send("**+{}** {} have been added to your account.".format(amount, csym))
                elif amount in range(250, 450):
                    await ctx.send("Nice! **+{}** {} have been added to your account!".format(amount, csym))
                elif amount in range(450, 600):
                    await ctx.send("AWESOME! **+{}** {} have been added to your account!!".format(amount, csym))
                
                st_now = nowtime.strftime("%Y-%m-%d %H:%M:%S")
                sql_update_date(ctx.author.id, st_now)
                
            else:
                waittime = nextdaily - nowtime
                str_waittime_hour = str(waittime.seconds//3600)
                str_waittime_min = str((waittime.seconds//60)%60)
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
                        old_coinsym = sym_inp.content
                        
                        try:
                            print(old_coinsym)
                            st_coinsym = emoji.demojize(old_coinsym, use_aliases=True)
                            print(st_coinsym)
                        except:
                            print("not work ")
                        
                            
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
                        await ctx.send("You did not respond with an emoji.")
                        
                except asyncio.TimeoutError:
                   await ctx.send("You did not respond.")                  

            else:
                await ctx.send("You don't have an account in this server!")


        except:
            await ctx.send("You don't have an account in this server!")
    else:
        await ctx.send("Sorry! You don't have the permissions!")
                    



@client.command()
async def ce(ctx):
    await ctx.send("Alright, what do you want your Server's **new** Coin-Symbol to be?")
    sym_inp = await client.wait_for(
        "message",
        timeout=30,
        check=lambda message: message.author == ctx.author and message.channel == ctx.channel
        )
    print(sym_inp.content)
    

    

#@client.command()
#async def tables(ctx, table):
#    f_all = sql_show_table(table)
#    for f_one in f_all:
#        st_f_one = []
#        for c in f_one:
#            st_f_one.append(str(c))
#        st_f = " | ".join(st_f_one)
#        await ctx.send("`"+st_f+"`")
       


@client.command(aliases=["t"])
async def tip(ctx, user: discord.User = None, amount = None):
    try:
        if sql_check_exist("DUSERS", ctx.author.id) and sql_check_exist("DUSERS", user.id): #CHECK GIVER and RECIEVER
            duid, guid, doc, cbal, cdc = sql_search("DUSERS", ctx.author.id)
            duidr, guidr, docr, cbalr, cdcr = sql_search("DUSERS", user.id)
            if guid == guidr:
                if cbal >= int(amount):
                    guid, cnam, csym = sql_search("DGUILDS", guid)
                    await ctx.send("Are you sure you want to give {} {} {}? Type `confirm`.".format(user.mention, amount, csym))
                    try:
                        conf = await client.wait_for(
                            "message",
                            timeout=30,
                            check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                            )
                        confcon = conf.content
                        if confcon.lower() in ["confirm", "confirm "]:
                            sql_addbal(user.id, amount)
                            sql_subbal(ctx.author.id, amount)
                            await ctx.send("{} {} have been transfered to {}'s account!".format(amount, csym, user.mention))
                        else:
                            await ctx.send("Procedure cancelled.")
                    except asyncio.TimeoutError:
                        await ctx.send("You did not respond.")
                else:
                    await ctx.send("You don't have enough balance in your account!")
            else:
                await ctx.send("There is no account with this name in this server.")
        else:
            await ctx.send("Both the sender and the reciever should have an account!")
    except:
        await ctx.send("You did not use the correct format => `cc tip <tag-user> <amount>`")


@client.command(aliases=["pr"])
async def profile(ctx, user: discord.User = None):
    if user == None:
        user = ctx.author
    else:
        user = user
    try:
        user_data_all = sql_search("DUSERS", user.id)
        duid, guid, doc, cbal, cdc = user_data_all
        if guid == ctx.guild.id:
            try:
                guilddata = sql_search("DGUILDS", guid) 
                guid, cnam, csym = guilddata
                st_doc = doc.strftime("%d-%m-%Y")
                
                dt_storedtime = cdc
                nextdaily = dt_storedtime + timedelta(hours=24)
                nowtime = datetime.now()
                
                try:
                    assert nextdaily > nowtime
                    waittime = nextdaily - nowtime
                    str_waittime_hour = str(waittime.seconds//3600)
                    str_waittime_min = str((waittime.seconds//60)%60)
                
                except:
                    str_waittime_hour = "**00**"
                    str_waittime_min = "**00**"  
                
                name = user.name
                avatar_url = user.avatar_url
                
                
                embedVar = discord.Embed(
                title="{}'s profile".format(name), description="Created on {}".format(st_doc), color = colors.green
                )
                embedVar.set_thumbnail(url=avatar_url)
                embedVar.add_field(name="Coin Balance {}: ".format(csym), value=str(cbal), inline=False)
                embedVar.add_field(name="Next Daily in :calendar:: ", value="{}h {}m".format(str_waittime_hour, str_waittime_min), inline=False)
                
                await ctx.send(embed=embedVar)
        
            except:
                await ctx.send("There is no account with this name in this server.")
        else:
            if user == ctx.author:
                await ctx.send("You don't have an account in this server!")
            else:
                await ctx.send("There is no account with this name in this server.")

    except:
        await ctx.send("There is no account with this name in this server.")



@client.command(aliases=["rm"])
async def removeme(ctx):
    if sql_check_exist("DUSERS", ctx.author.id):
        duid, guid, doc, cbal, cdc = sql_search("DUSERS", ctx.author.id)

        # CHECK IF ANY PENDING LOANS
        
        await ctx.send("Are you sure yoou want to delete your account? This action is permanent and you will **lose all your balance**. Type `confirm` if you want to proceed.")
        try:
            conf = await client.wait_for(
                "message",
                timeout=30,
                check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                )
            confcon = conf.content
            if confcon.lower() in ["confirm", "confirm "]:
                sql_delete("DUSERS", ctx.author.id)
                await ctx.send("Your account has been deleted.")
        except asyncio.TimeoutError:
            await ctx.send("You did not respond.")
    else:
        await ctx.send("You don't have an account yet!")
            


@client.command(aliases=["cs"])
async def changeserver(ctx):
    if sql_check_exist("DUSERS", ctx.author.id):
        duid, guid, doc, cbal, cdc = sql_search("DUSERS", ctx.author.id)
        if guid == ctx.guild.id:
            await ctx.send("You have already registered your account here! You can only use this command in a different server.")
        else:
            await ctx.send("Are you sure you want to change your server?\n**YOU WILL LOSE ALL YOUR BALANCE!!**\nType `Y` or `y` to continue.")
            try:
                conf = await client.wait_for(
                    "message",
                    timeout=30,
                    check=lambda message: message.author == ctx.author and message.channel == ctx.channel
                    )
                confcon = conf.content
                if confcon in ["Y", "y"]:
                    sql_user_cngserver(ctx.author.id, ctx.guild.id)
                    await ctx.send("Your server has been changed.")

            except asyncio.TimeoutError:
                await ctx.send("You did not respond.")
                
    else:
        await ctx.send("You do not have an account in this server. Use `cc addme` to create one!")



# CHECK 

@client.command()
async def bal(ctx, user: discord.User = None):
    try:
        if user == None:
            user = ctx.author
        else:
            user = user
        try:
            duid, guid, doc, cbal, cdc = sql_search("DUSERS", user.id)
            guid, cnam, csym = sql_search("DGUILDS", guid)
            if guid == ctx.guild.id:
                embedVar = discord.Embed(
                    title="{}'s balance".format(user.name), description=str("Use `cc daily` to get coins!"), color = colors.gold
                    )
                embedVar.set_thumbnail(url=user.avatar_url)
                embedVar.add_field(name="{} Balance: ".format(csym), value="**"+str(cbal)+"**", inline=False)
                await ctx.send(embed=embedVar)
            else:
                await ctx.send("Your account is connected to a different server, to change it user `cc changeserver` or `cc cs`.")
        except:
            if user == None:
                await ctx.send("Your account does not exist here :\ Use `cc addme` to create one.")
            else:
                await ctx.send("There is no account with this name here.")
    except:
        await ctx.send("There is no account with this name here.")

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
    


        
        
        



client.run("ODUzNTcwMjg0OTE2NTcyMTcw.YMXTRg.zqtJBlIi-oo3wqUOVYUozYho3Lk")


















    

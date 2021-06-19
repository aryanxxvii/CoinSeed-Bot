import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime, timedelta
import emoji


bot_prefix = "cc ", "<@853570284916572170> ", "<@!853570284916572170> "
intents = discord.Intents.all()
client = commands.Bot(command_prefix=bot_prefix, intents=intents)

client.remove_command("help")

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="cc help"))





try:
    from sqlfunc import *
except:
    print("Server Error or Error in MySQL Code")
    





@client.command()
async def ping(ctx):
    await ctx.send(f"pong {round(client.latency * 1000)}")

#----------------------------------------------------------------------------------
# HELPING HAND

HELP_GUIDE = {
    "addme": ["","Creates an account in the server where it is typed.", "Usage: cc addme"],
    "removeme": ["rm", "Removes your existing account.", "Usage: cc removeme"],
    "profile": ["pr", "Displays profile of user/tagged user.", "Usage: cc profile/ cc profile <tag_user>"],
    "leaderboard": ["lb", "Shows the list of richest user in your server.", "Usage: cc leaderboard"],
    "daily": ["d", "Gives your daily reward.", "Usage: cc daily"],
    "balance":  ["bal", "Shows your current balance.", "Usage: cc balance"],
    "tip": ["give/t", "Used to give someone money.", "Usage: cc tip <tag_user> <amount>"],
    "server": ["s", "Displays server info.", "Usage: cc server"],
    "cngserverinfo": ["csi", "Change server currency. *For authorised users.", "Usage: cc cngserverinfo"],
    "changeserver": ["cs", "Change the server linked to your account.", "Usage: cc changeserver"]
}

HELP_ALIAS = {
    "addme": HELP_GUIDE["addme"],
    "removeme": HELP_GUIDE["removeme"], "rm": HELP_GUIDE["removeme"],
    "profile": HELP_GUIDE["profile"], "pr": HELP_GUIDE["profile"],
    "leaderboard": HELP_GUIDE["leaderboard"], "lb": HELP_GUIDE["leaderboard"],
    "daily": HELP_GUIDE["daily"], "d": HELP_GUIDE["daily"],
    "balance": HELP_GUIDE["balance"], "bal": HELP_GUIDE["balance"],
    "tip": HELP_GUIDE["tip"], "give": HELP_GUIDE["tip"], "t": HELP_GUIDE["tip"],
    "server": HELP_GUIDE["server"], "s": HELP_GUIDE["server"],
    "cngserverinfo": HELP_GUIDE['cngserverinfo'], "csi": HELP_GUIDE["cngserverinfo"],
    "changeserver": HELP_GUIDE["changeserver"], "cs": HELP_GUIDE["changeserver"]
}

def coinseed_help(cmd): #returns 3 valued list = command/alias + desc + usage

    global HELP_ALIAS
    x = HELP_ALIAS[cmd]
    x[0] = cmd + "/" + x[0]
    return x


@client.command()
async def help(ctx, comname = None):
    if comname == None:
        embedVar = discord.Embed(
        title="CoinSeed Help", description="General Help", color = colors.gold
        )
        embedVar.set_thumbnail(url=client.user.avatar_url)
        for com in coms:
            comhelp = coms[com]
            embedVar.add_field(name="{}".format(com), value="{}".format(comhelp), inline=True)

        await ctx.send(embed=embedVar)
    else:
        for com in coms:
            if comname in coms or comname in com[0]:
                if len(com) == 2:
                    embedVar = discord.Embed(
                    title="{} Help".format(com), description="Aliases: {}\n{}".format(", ".join(com[0]), com[1]), color = colors.gold
                    )
                    embedVar.set_thumbnail(url=client.user.avatar_url)
                    await ctx.send(embed=embedVar)
                else:
                    embedVar = discord.Embed(
                    title="{} Help".format(com), description="{}".format(com[0]), color = colors.gold
                    )
                    embedVar.set_thumbnail(url=client.user.avatar_url)
                    await ctx.send(embed=embedVar)
            
    
##    else:
##        await ctx.send("No such command exists! Use `cc help` to see all commands.")
##        

#-------------------------------------------------------------------------------

# [x]PERSONAL ACC CREATION
# [x]GUILD ACC CREATION
# [x]BAL CHECK
# [x]PROFILE
# [x]SERVER PRoFILE
# [x]DAILY
# [ ]LOANS
# [x]CHANGE SERVER
# [x]CHANGE SYMBOL/NAME
# [x]TIPS
# [x]REMOVE HARDCODING
# [x]MAKE HELP
# [x]BUMP COINS
# [x]LEADERBOARD
# [ ]TOTAL COINS IN SERVER + %COINS IN USER PROFILE

# Remove 'rm' = done
# when changeserver, dont change daily = done
# test if dict key can be list, if yes, {[command, alias]:help}

#-------------------------------------------------------------------------------
# FUNCTIONS TO REDUCE REPETITION OF CODE

def check_user_guild_useringuild_exists(ctx, userid = None):
    # returns bool values for existence of user, guild and user in guild
    if userid == None:
        userid = ctx.author.id
    guild = ctx.guild

    user_exists = sql_check_exist("DUSERS", userid)
    guild_exists = sql_check_exist("DGUILDS", guild.id)
    
    if user_exists and guild_exists:
        [duid, guid] = sql_search("DUSERS", userid)[0:2]
        if guid == guild.id:
            user_exists_in_guild = True
        else:
            user_exists_in_guild = False
    else:
        user_exists_in_guild = False
    
    return user_exists, guild_exists, user_exists_in_guild

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
        sql_add("DGUILDS", guild.id, ["SeedCoin", "coin"])
            



@client.command(aliases=["s"])
async def server(ctx):
    guid, cnam, csym = sql_search("DGUILDS", ctx.guild.id)
    ecsym = emoji.emojize(csym)
    gnam = ctx.guild.name
    icon_url = ctx.guild.icon_url
    
    
    embedVar = discord.Embed(
    title="{}'s Info".format(gnam), description="", color = colors.purple
    )
    embedVar.set_thumbnail(url=icon_url)
    embedVar.add_field(name="Coin-Name", value=cnam, inline=False)
    embedVar.add_field(name="Coin-Symbol", value=ecsym, inline=False)
    
    await ctx.send(embed=embedVar)


@client.event
async def on_message(message):
    if message.author.id == 302050872383242240: #Disboard's ID
        embeds = message.embeds
        emdict = embed.to_dict()
        if "Bump done" in emdict["description"]:
            em_l = emdict["description"].split(" ")
            tag = em_l[0][:-1]
            if "!" in tag:
                userid = int(tag[3:-1])
            else:
                userid = int(tag[2:-1])
            try:
                duid, guid, doc, cbal, cdc =  sql_search("DUSERS", userid)
                guid, cnam, csym = sql_search("DGUILDS", guid)
                if guid == message.guild.id:
                    amount = random.randrange(100, 201)
                    sql_addbal(userid, amount)
                    sql_search("DGUILDS", message.guild.id)
                    await message.channel.send("<@{}>, **+{}** {} {} have been added to your balance!\n*Thanks for bumping this server!*".format(str(userid), str(amount), csym, cnam))
                    
                else:
                    await ctx.send("You have an account in a different server. You can only link one server at a time.\n Use `cc changeserver` or `cc cs` to change your account-server.")
            except:
                await ctx.send("You don't have an account yet! Create one with `cc addme`!")
    await client.process_commands(message)        

# ACC CREATION
@client.command()
async def addme(ctx, *, attr=None):
    if attr == None:
        user_exists, guild_exists, user_in_guild = check_user_guild_useringuild_exists(ctx)
        #IF MESSAGE GUILD IN DGUILDS
        if user_exists:
            if user_in_guild:
                await ctx.send('You have already registered your account in this server.')
            else:
                await ctx.send("You have already registered in another server. To change your server type `cc changeserver`.")

        elif not user_exists:
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
    user_exists, guild_exists, user_in_guild = check_user_guild_useringuild_exists(ctx)
    
    if user_exists:
        
        if user_in_guild:
            duid, guid, doc, cbal, cdc = sql_search("DUSERS", ctx.author.id)
            guid, cnam, csym = guilddata = sql_search("DGUILDS", guid)
            
            dt_storedtime = cdc
            nextdaily = dt_storedtime + timedelta(hours=24)
            nowtime = datetime.now()
            if nowtime > nextdaily:
                amount = random.randrange(100, 600) 
                sql_addbal(ctx.author.id, amount)
                if amount in range(100, 250):
                    await ctx.send("**+{}** {} {} have been added to your account.".format(amount, emoji.emojize(csym), cnam))
                elif amount in range(250, 450):
                    await ctx.send("Nice! **+{}** {} {} have been added to your account!".format(amount, emoji.emojize(csym), cnam))
                elif amount in range(450, 600):
                    await ctx.send("AWESOME! **+{}** {} have been added to your account!!".format(amount, emoji.emojize(csym), cnam))
                
                st_now = nowtime.strftime("%Y-%m-%d %H:%M:%S")
                sql_update_date(ctx.author.id, st_now)
                
            else:
                waittime = nextdaily - nowtime
                str_waittime_hour = str(waittime.seconds//3600)
                str_waittime_min = str((waittime.seconds//60)%60)
                await ctx.send("You have to wait another **{} hours {} minutes**".format(str_waittime_hour, str_waittime_min))
            
        else:
            await ctx.send("You do not have an account in this server.")
    else:
        await ctx.send("You don't have an account yet! Type `cc addme` to create one!")
    
    #IF TIME NOW GREATER THAN 24 + OL
        #ADD RANDOM BALANCE BW 100 to 500



@commands.has_permissions(ban_members=True, kick_members=True) 


@client.command(aliases=["csi"])
async def cngserverinfo(ctx):
    
    if ctx.author.guild_permissions.manage_guild:
        
        user_exists, guild_exists, user_in_guild = check_user_guild_useringuild_exists(ctx)
        
        if user_exists:

            if user_in_guild:
                duid, guid, doc, cbal, cdc = sql_search("DUSERS", ctx.author.id)
                guid, cnam, csym = sql_search("DGUILDS", ctx.guild.id)
                await ctx.send("Current Coin-Name: {}\nCurrent Coin-Symbol: {}".format(cnam, emoji.emojize(csym)))
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
                        st_coinsym = emoji.demojize(coinsym)
                            
                        sql_guild_cngcoin(guid, coinname, st_coinsym)

                        guid, cnam, csym = sql_search("DGUILDS", ctx.guild.id)
                        ecsym = emoji.emojize(csym)
                        servname = ctx.guild.name
                        icon_url = ctx.guild.icon_url
                    
                        
                        embedVar = discord.Embed(
                        title="{}'s Coin System Changed!".format(servname), description="", color = colors.green
                        )
                        embedVar.set_thumbnail(url=icon_url)
                        embedVar.add_field(name="New Coin-Name", value=str(cnam), inline=False)
                        embedVar.add_field(name="New Coin-Symbol", value=ecsym, inline=False)
                        await ctx.send(embed=embedVar)
                        
                    except asyncio.TimeoutError:
                        await ctx.send("You did not respond with an emoji.")
                        
                except asyncio.TimeoutError:
                    await ctx.send("You did not respond.")                  
            else:
                await ctx.send("You don't have an account in this server!")
        else:
            await ctx.send("You don't have an account! Create one using cc addme.")
    else:
        await ctx.send("Sorry! You don't have the permissions!")

    

##@client.command()
##async def tables(ctx, table):
##    f_all = sql_show_table(table)
##    for f_one in f_all:
##        st_f_one = []
##        for c in f_one:
##            st_f_one.append(str(c))
##        st_f = " | ".join(st_f_one)
##        await ctx.send("`"+st_f+"`")
##       


@client.command(aliases=["give", "t"])
async def tip(ctx, user: discord.User = None, amount = None):
    try:
        if sql_check_exist("DUSERS", ctx.author.id) and sql_check_exist("DUSERS", user.id): #CHECK GIVER and RECIEVER
            duid, guid, doc, cbal, cdc = sql_search("DUSERS", ctx.author.id)
            duidr, guidr, docr, cbalr, cdcr = sql_search("DUSERS", user.id)
            if guid == guidr:
                if cbal >= int(amount):
                    guid, cnam, csym = sql_search("DGUILDS", guid)
                    await ctx.send("Are you sure you want to give {} **{}** {}? Type `confirm`.".format(user.mention, amount, emoji.emojize(csym)))
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
                            await ctx.send("**{}** {} have been transfered to {}'s account!".format(amount, emoji.emojize(csym), user.mention))
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
        user = ctx.author ; cond = 'me'
    else:
        user = user; cond = 'they'
    
    user_exists, guild_exists, user_in_guild = check_user_guild_useringuild_exists(ctx, user.id)

    if user_exists:
        
        if user_in_guild:
            
            user_data_all = sql_search("DUSERS", user.id)
            duid, guid, doc, cbal, cdc = user_data_all

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
            embedVar.add_field(name="Coin Balance {}: ".format(emoji.emojize(csym)), value=str(cbal), inline=False)
            embedVar.add_field(name="Next Daily in :calendar:: ", value="{}h {}m".format(str_waittime_hour, str_waittime_min), inline=False)
            
            await ctx.send(embed=embedVar)
        
        else:
            if cond == 'me':
                await ctx.send("You don't have an account in this server!")
            elif cond == 'they':
                await ctx.send("There is no account with this name in this server.")

    else:
        if cond == 'me':
            await ctx.send("You don't have an account yet.")
        elif cond == 'they':
            await ctx.send("There is no account with this name.")




@client.command(aliases=["lb"])
async def leaderboard(ctx):
    ulist, csym, cnam = sql_server_topusers(ctx.guild.id)
    ulist = ulist[::-1]
    ecsym = emoji.emojize(csym)
    desc = ""
    for r in range(len(ulist)):
        duid, cbal = ulist[r]
        desc = desc + "**{}. {}: {} {}**\n".format(r+1, client.get_user(duid).name, cbal, emoji.emojize(csym))
    embedVar = discord.Embed(
    title="{}'s Leaderboard".format(ctx.guild.name), description=desc, color = colors.red
    )
    embedVar.set_thumbnail(url=ctx.guild.icon_url)
##    for r in range(len(ulist)):
##        duid, cbal = ulist[r]
##        embedVar.add_field(name="{}. {}: ".format(r+1, client.get_user(duid).name), value = "**{} {}**".format(cbal, emoji.emojize(csym)), inline=False)
    embedVar.set_footer(icon_url = ctx.author.avatar_url, text = "Requested by {}".format(ctx.author.name))
    await ctx.send(embed=embedVar)

           


@client.command(aliases=["cs"])
async def changeserver(ctx):
    user_exists, guild_exists, user_in_guild = check_user_guild_useringuild_exists(ctx)

    if user_exists:

        if user_in_guild:
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

@client.command(aliases=["bal"])
async def balance(ctx, user: discord.User = None):
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




        
        
        



client.run("ODUzNTcwMjg0OTE2NTcyMTcw.YMXTRg.zqtJBlIi-oo3wqUOVYUozYho3Lk")


















    

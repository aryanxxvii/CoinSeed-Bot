import mysql.connector
mydb = mysql.connector.connect(host="johnny.heliohost.org", user="aryan27_coinseedbot", passwd="Aryanxxvii27!", database="aryan27_coinseed")
mycursor = mydb.cursor()

USERS = ['DISUSERID', 'GUILDID', 'DOC', 'COINBAL', 'DT']
GUILDS =['GUILDID', 'COINNAME', 'COINSYMBOL']
TRANSACTIONS = ['RECEIVER', 'DONOR', 'PRINCIPLE', 'INTEREST', 'LD', 'DD']

def add(table, key=None, rec = list()):
    
    global mydb, mycursor
    T = table.upper()

    if T == "USERS":
        mycursor.execute("INSERT INTO USERS VALUES({},{},'{}',{},'{}')".format(key, rec[0], rec[1], rec[2], rec[3]))
    elif T == "GUILDS":
        mycursor.execute("INSERT INTO GUILDS VALUES({},'{}','{}')".format(key, rec[0], rec[1]))
    elif T == "TRANSACTIONS":
        mycursor.execute("INSERT INTO TRANSACTIONS VALUES({},{},{},{},'{}','{}')".format(key, rec[0], rec[1], rec[2], rec[3], rec[4]))
    
    mydb.commit()

def delete(table, key):

    global mydb, mycursor
    T = table.upper()
    mycursor.execute("DELETE FROM " + T + " WHERE RECEIVER = {}".format(key))
    mydb.commit()
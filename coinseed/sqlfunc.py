from re import X
import os
import mysql.connector
import time
from datetime import datetime, timedelta
passwd = os.environ['DB_PASSWD']

mydb = mysql.connector.connect(host="johnny.heliohost.org", user="aryan27_coinseedbot", passwd=passwd, database="aryan27_coinseed")
mycursor = mydb.cursor()


s_last = "00:00:00"

#Keep trying to connect to server if it goes down
def sql_connection_call():
    connected = False
    while connected == False:
        try:
            mydb = mysql.connector.connect(host="johnny.heliohost.org", user="aryan27_coinseedbot", passwd=passwd, database="aryan27_coinseed")
            mycursor = mydb.cursor()
            connected = True
            return mydb, mycursor
        except:
            time.sleep(5)
    
#Automatically reconnect to server if the last command was made 10 or more minutes ago to ensure server is up.
def check_last():
    bnow = datetime.now()
    snow = bnow.strftime("%H:%M:%S")
    now = datetime.strptime(snow, "%H:%M:%S")
    global s_last
    last = datetime.strptime(s_last, "%H:%M:%S")
    if last + timedelta(minutes = 10) < now:
        
        s_last = datetime.now().strftime("%H:%M:%S")
        
        return True
    else:
        
        return False



def sql_add(tablename, key=None, rec = list()):
    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    T = tablename.upper()
    
    if T == "DGUILDS":
        mycursor.execute("INSERT INTO DGUILDS VALUES({},'{}','{}')".format(key, rec[0], rec[1]))
    elif T == "DUSERS":
        mycursor.execute("INSERT INTO DUSERS VALUES({},{},'{}',{},'{}')".format(key, rec[0], rec[1], rec[2], rec[3]))
    elif T == "DTRANSACTIONS" and key == None:
        mycursor.execute("INSERT INTO DTRANSACTIONS(DONOR, RECEIVER, PRINCIPLE, AMOUNT, LD, DD) VALUES({},{},{},{},'{},'{}')".format(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5]))
    
    mydb.commit()

def sql_delete(tablename, key):
    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    T = tablename.upper()
    table_keys = {'DGUILDS': 'GUID', 'DUSERS': 'DUID', 'DTRANSACTIONS': 'TID'}
    mycursor.execute("DELETE FROM " + T + " WHERE " + table_keys[T] + " = {}".format(key))
    mydb.commit()

def sql_search(tablename, key):
    
    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    T = tablename.upper()
    table_keys = {'DGUILDS': 'GUID', 'DUSERS': 'DUID', 'DTRANSACTIONS': 'TID'}
    mycursor.execute("SELECT * FROM " + T + " WHERE " + table_keys[T] + " = {}".format(key))
    try:
        x = list(mycursor.fetchone())
        return x
    except:
        return None



def sql_check_exist(tablename, key):

    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    T = tablename.upper()
    table_keys = {'DGUILDS': 'GUID', 'DUSERS': 'DUID', 'DTRANSACTIONS': 'TID'}
    mycursor.execute("SELECT COUNT(*) FROM " + T + " WHERE " + table_keys[T] + " = {}".format(key))
    x = list(mycursor.fetchone())
    if x[0] == 0:
        boolx = False
    elif x[0] == 1:
        boolx = True
    return boolx

def sql_show_table(tablename): #returns a list of tuples
    
    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    mycursor.execute("SELECT * FROM " + tablename.upper() + ";")
    x = mycursor.fetchall()
    return x

#=========================================================================

# SPECIAL FUNCTIONS

def sql_server_topusers(guid): #list the players in the server, csym

    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    mycursor.execute("SELECT CSYM, CNAM FROM DGUILDS WHERE GUID = {}".format(int(guid)))
    csym, cnam = mycursor.fetchone()
    mycursor.execute("SELECT DUID, CBAL FROM DUSERS WHERE GUID = {} ORDER BY CBAL".format(int(guid)))
    user_list = mycursor.fetchall()[:10]
    user_list = user_list[::-1]
    return user_list, csym, cnam

def sql_user_cngserver(duid, newguid):

    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    mycursor.execute("UPDATE DUSERS SET GUID = {}, CBAL = 0 WHERE DUID = {}".format(newguid, duid))
    mydb.commit()

def sql_guild_cngcoin(key, newcoinname, newcoinsymbol):

    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    mycursor.execute("UPDATE DGUILDS SET CNAM = %s , CSYM = %s WHERE GUID = %s;", (newcoinname, newcoinsymbol, key))
    mydb.commit()



def sql_update_date(duid, today):

    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    mycursor.execute("UPDATE DUSERS SET CDC = '{}' WHERE DUID = '{}'".format(today, duid))
    mydb.commit()

def sql_addbal(duid, amount): #adds specified amount to balance

    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    mycursor.execute("UPDATE DUSERS SET CBAL = CBAL + {} WHERE DUID = {}".format(amount, duid))
    mydb.commit()

def sql_subbal(duid, amount): #subtracts specifies amount from balance
    
    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    mycursor.execute("UPDATE DUSERS SET CBAL = CBAL - {} WHERE DUID = {}".format(amount, duid))
    mydb.commit()

def sql_loan_transaction(tid, donor, receiver, amount): #return 1 if success else return -1 : updates the coinbalance when receiver compensates loan
    
    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass

    mycursor.execute("SELECT CBAL FROM DUSERS WHERE DUID = {}".format(receiver))
    x = mycursor.fetchone()
    mycursor.execute("SELECT AMOUNT FROM DTRANSACTIONS WHERE TID = {}".format(tid))
    y = mycursor.fetchone()
    
    if amount <= x[0] and amount <= y[0]:
        sql_subbal(receiver, amount)
        sql_addbal(donor, amount)
        mycursor.execute("UPDATE DTRANSACTIONS SET AMOUNT = AMOUNT - {} WHERE TID = {}".format(amount, tid))
        mydb.commit()
        return 1
    
    else:
        return -1

def sql_loan_initiate(donor, receiver, principle, loandate, duedate): #return 1 if success else return -1: creates a new loan record
    
    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass

    mycursor.execute("SELECT CBAL FROM DUSERS WHERE DUID = {}".format(donor))
    x = mycursor.fetchone()

    if principle <= x[0]:
        sql_subbal(donor, principle)
        sql_addbal(receiver, principle)
        mydb.commit()

        sql_add("DTRANSACTIONS", None, [donor, receiver, principle, principle, loandate, duedate])
        return 1
    
    else:
        return -1

def sql_loan_check(tid): # return 1 if success else return -1 : Deletes the record if loan completed
     
    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
     
    mycursor.execute("SELECT AMOUNT FROM DTRANSACTIONS WHERE TID = {}".format(tid))
    x = mycursor.fetchone()
    if x[0] == 0:
        sql_delete("DTRANSACTIONS", tid)
        return 1

def sql_loan_punish(today): #returns the list of users who failed to complete loan before due date
    
    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    mycursor.execute("SELECT RECEIVER FROM DTRANSACTIONS WHERE DUEDATE < '{}'".format(today))
    x = mycursor.fetchall()

    users = []
    for i in x:
        users.append(i[0])
    return users

def sql_interest_add(rate): #returns 1 if success else returns -1 : adds the interest

    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    mycursor.execute("UPDATE DTRANSACTIONS SET AMOUNT = AMOUNT + PRINCIPLE*{}".format(rate))
    mydb.commit()

# DEVELOPER FUNCTION

def sql_giveaway(amount, duid, guid):

    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    if duid in [340891107363651585, 301756088221433876]:
        mycursor.execute("UPDATE DUSERS SET CBAL = CBAL + {} WHERE GUID = {}".format(amount, guid))
        mydb.commit()
        return 1
    else:
        return 0
        

def sql_developer_call(command, duid):

    global mydb, mycursor
    if check_last():
        mydb, mycursor = sql_connection_call()
    else:
        pass
    if duid in [340891107363651585, 301756088221433876]:
        mycursor.execute(command)
        mydb.commit()

from re import X
import mysql.connector
mydb = mysql.connector.connect(host="johnny.heliohost.org", user="aryan27_coinseedbot", passwd="Aryanxxvii27!", database="aryan27_coinseed")
mycursor = mydb.cursor()

def sql_add(tablename, key=None, rec = list()):
    
    global mycursor, mydb
    T = tablename.upper()
    
    if T == "DGUILDS":
        mycursor.execute("INSERT INTO DGUILDS VALUES({},'{}','{}')".format(key, rec[0], rec[1]))
    elif T == "DUSERS":
        mycursor.execute("INSERT INTO DUSERS VALUES({},{},'{}',{},'{}')".format(key, rec[0], rec[1], rec[2], rec[3]))
    elif T == "DTRANSACTIONS" and key == None:
        mycursor.execute("INSERT INTO DTRANSACTIONS(DONOR, RECEIVER, PRINCIPLE, AMOUNT, LD, DD) VALUES({},{},{},{},'{},'{}')".format(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5]))
    
    mydb.commit()

def sql_delete(tablename, key):

    global mycursor, mydb
    T = tablename.upper()
    table_keys = {'DGUILDS': 'GUID', 'DUSERS': 'DUID', 'DTRANSACTIONS': 'TID'}
    mycursor.execute("DELETE FROM " + T + " WHERE " + table_keys[T] + " = {}".format(key))
    mydb.commit()

def sql_search(tablename, key):
    
    global mycursor, mydb
    T = tablename.upper()
    table_keys = {'DGUILDS': 'GUID', 'DUSERS': 'DUID', 'DTRANSACTIONS': 'TID'}
    mycursor.execute("SELECT * FROM " + T + " WHERE " + table_keys[T] + " = {}".format(key))
    x = list(mycursor.fetchone())
    return x

def sql_check_exist(tablename, key):
    global mycursor, mydb
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
    
    global mycursor, mydb
    mycursor.execute("SELECT * FROM " + tablename.upper() + ";")
    x = mycursor.fetchall()
    return x

#=========================================================================

# SPECIAL FUNCTIONS

def sql_update_dguild(key, coinname, coinsymbol):

    global mycursor, mydb
    mycursor.execute("UPDATE DGUILDS SET CNAM = '{}' , CSYM = '{}' WHERE GUID = {}".format(coinname, coinsymbol, key))
    mydb.commit()

def sql_update_date(duid, today):

    global mycursor, mydb
    mycursor.execute("UPDATE DUSERS SET CDC = '{}' WHERE DUID = '{}'".format(today, duid))
    mydb.commit()

def sql_addbal(duid, amount): #adds specified amount to balance

    global mycursor, mydb
    mycursor.execute("UPDATE DUSERS SET CBAL = CBAL + {} WHERE DUID = {}".format(amount, duid))
    mydb.commit()

def sql_subbal(duid, amount): #subtracts specifies amount from balance
    
    global mycursor, mydb
    mycursor.execute("UPDATE DUSERS SET CBAL = CBAL - {} WHERE DUID = {}".format(amount, duid))
    mydb.commit()

def sql_loan_transaction(tid, donor, receiver, amount): #return 1 if success else return -1 : updates the coinbalance when receiver compensates loan
    
    global mycursor, mydb

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
    
    global mycursor, mydb

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
     
    global mycursor, mydb
     
    mycursor.execute("SELECT AMOUNT FROM DTRANSACTIONS WHERE TID = {}".format(tid))
    x = mycursor.fetchone()
    if x[0] == 0:
        sql_delete("DTRANSACTIONS", tid)
        return 1

def sql_loan_punish(today): #returns the list of users who failed to complete loan before due date
    
    global mycursor, mydb
    mycursor.execute("SELECT RECEIVER FROM DTRANSACTIONS WHERE DUEDATE < '{}'".format(today))
    x = mycursor.fetchall()

    users = []
    for i in x:
        users.append(i[0])
    return users

def sql_interest_add(rate): #returns 1 if success else returns -1 : adds the interest

    global mycursor, mydb
    mycursor.execute("UPDATE DTRANSACTIONS SET AMOUNT = AMOUNT + PRINCIPLE*{}".format(rate))
    mydb.commit()


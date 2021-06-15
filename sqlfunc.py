from re import X
import mysql.connector
mydb = mysql.connector.connect(host="johnny.heliohost.org", user="aryan27_coinseedbot", passwd="Aryanxxvii27!", database="aryan27_coinseed")
mycursor = mydb.cursor()

def add(tablename, key=None, rec = list()):
    
    global mycursor, mydb
    T = tablename.upper()
    
    if T == "DGUILDS":
        mycursor.execute("INSERT INTO DGUILDS VALUES({},'{}','{}')".format(key, rec[0], rec[1]))
    elif T == "DUSERS":
        mycursor.execute("INSERT INTO DUSERS VALUES({},{},'{}',{},'{}')".format(key, rec[0], rec[1], rec[2], rec[3]))
    elif T == "DTRANSACTIONS" and key == None:
        mycursor.execute("INSERT INTO DTRANSACTIONS(DONOR, RECEIVER, PRINCIPLE, AMOUNT, LD, DD) VALUES({},{},{},{},'{},'{}')".format(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5]))
    
    mydb.commit()

def delete(tablename, key):

    global mycursor, mydb
    T = tablename.upper()
    table_keys = {'DGUILDS': 'GUID', 'DUSERS': 'DUID', 'DTRANSACTIONS': 'TID'}
    mycursor.execute("DELETE FROM " + T + " WHERE " + table_keys[T] + " = {}".format(key))
    mydb.commit()

def search(tablename, key):
    
    global mycursor, mydb
    T = tablename.upper()
    table_keys = {'DGUILDS': 'GUID', 'DUSERS': 'DUID', 'DTRANSACTIONS': 'TID'}
    mycursor.execute("SELECT * FROM " + T + " WHERE " + table_keys[T] + " = {}".format(key))
    x = list(mycursor.fetchone())
    return x

#=========================================================================

# SPECIAL FUNCTIONS

def loan_transaction(tid, donor, receiver, amount): #return 1 if success else return -1 : updates the coinbalance
    
    global mycursor, mydb

    mycursor.execute("SELECT CBAL FROM DUSERS WHERE DUID = {}".format(receiver))
    x = mycursor.fetchone()
    mycursor.execute("SELECT AMOUNT FROM DTRANSACTIONS WHERE TID = {}".format(tid))
    y = mycursor.fetchone()
    
    if amount <= x[0] and amount <= y[0]:
        mycursor.execute("UPDATE DUSERS SET CBAL = CBAL - {} WHERE DUID = {}".format(amount, receiver))
        mycursor.execute("UPDATE DUSERS SET CBAL = CBAL + {} WHERE DUID = {}".format(amount, donor))
        mycursor.execute("UPDATE DTRANSACTIONS SET AMOUNT = AMOUNT - {} WHERE TID = {}".format(amount, tid))
        mydb.commit()
        return 1
    
    else:
        return -1

def loan_initiate(donor, receiver, principle, loandate, duedate): #return 1 if success else return -1: adds record on success
    
    global mycursor, mydb

    mycursor.execute("SELECT CBAL FROM DUSERS WHERE DUID = {}".format(donor))
    x = mycursor.fetchone()

    if principle <= x[0]:
        mycursor.execute("UPDATE DUSERS SET CBAL = CBAL - {} WHERE DUID = {}".format(principle, donor))
        mycursor.execute("UPDATE DUSERS SET CBAL = CBAL + {} WHERE DUID = {}".format(principle, receiver))
        mydb.commit()

        add("DTRANSACTIONS", None, [donor, receiver, principle, principle, loandate, duedate])
        return 1
    
    else:
        return -1

def loan_check(tid): # return 1 if success else return -1 : Deletes the record if loan completed
     
    global mycursor, mydb
     
    mycursor.execute("SELECT AMOUNT FROM DTRANSACTIONS WHERE TID = {}".format(tid))
    x = mycursor.fetchone()
    if x[0] == 0:
        delete("DTRANSACTIONS", tid)
        return 1

def loan_punish(today): #returns the list of users who failed to complete loan before due date
    
    global mycursor, mydb
    mycursor.execute("SELECT RECEIVER FROM DTRANSACTIONS WHERE DUEDATE < TODAY")
    x = mycursor.fetchall()

    users = []
    for i in x:
        users.append(i[0])
    return users

def interest_add(rate): #returns 1 if success else returns -1 : adds the interest

    global mycursor, mydb
    mycursor.execute("UPDATE DTRANSACTIONS SET AMOUNT = AMOUNT + PRINCIPLE*{}".format(rate))
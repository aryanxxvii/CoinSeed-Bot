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
'''
def update(tablename, rec = {"set": "", "where": ""}):
    
    global mycursor, mydb
    T = tablename.upper()
    table_keys = {'DGUILDS': 'GUID', 'DUSERS': 'DUID', 'DTRANSACTIONS': 'TID'}

    set_query = " SET " + rec['set']
    where_query = " WHERE " + rec['where']

   ''' 
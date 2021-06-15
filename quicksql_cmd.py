import mysql.connector
mydb = mysql.connector.connect(host="johnny.heliohost.org", user="aryan27_coinseedbot", passwd="Aryanxxvii27!", database="aryan27_coinseed")
mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE DGUILDS(GUID BIGINT PRIMARY KEY, CNAM VARCHAR(20), CSYM VARCHAR(20))")
mycursor.execute("CREATE TABLE DUSERS(DUID BIGINT PRIMARY KEY, GUID BIGINT REFERENCES DGUILDS(GUID), DOC DATETIME, CBAL BIGINT, CDC DATETIME)")
mycursor.execute("CREATE TABLE DTRANSACTIONS(TID BIGINT PRIMARY KEY AUTO_INCREMENT, DONOR BIGINT REFERENCES DUSERS(DUID), RECEIVER BIGINT REFERENCES(DUID), PRINCIPLE BIGINT(20), AMOUNT BIGINT(20), LD DATETIME, DD DATETIME)")

mydb.commit()

mycursor.execute("DESC DGUILDS")
x = mycursor.fetchall()
print(x)
mycursor.execute("DESC DUSERS")
x = mycursor.fetchall()
print(x)
mycursor.execute("DESC DTRANSACTIONS")
x = mycursor.fetchall()
print(x)

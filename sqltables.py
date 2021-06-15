import mysql.connector
mydb = mysql.connector.connect(host="johnny.heliohost.org", user="aryan27_coinseedbot", passwd="Aryanxxvii27!", database="aryan27_coinseed")
mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE DGUILDS(GUID BIGINT(20) PRIMARY KEY, CNAM VARCHAR(20), CSYM VARCHAR(20))")
mycursor.execute("CREATE TABLE DUSERS(DUID BIGINT(20) PRIMARY KEY, GUID BIGINT(20) REFERENCES DGUILDS(GUID), DOC DATETIME, CBAL BIGINT(20), CDC DATETIME)")
mycursor.execute("CREATE TABLE DTRANSACTIONS(TID BIGINT(20) PRIMARY KEY AUTO_INCREMENT, DONOR BIGINT(20) REFERENCES DUSERS(DUID), RECEIVER BIGINT(20) REFERENCES DUSERS(DUID), PRINCIPLE BIGINT(20), AMOUNT BIGINT(20), LD DATETIME, DD DATETIME)")

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
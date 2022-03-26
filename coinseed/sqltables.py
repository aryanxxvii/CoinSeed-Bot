import os
import mysql.connector
passwd = os.environ['DB_PASSWD']
mydb = mysql.connector.connect(host="johnny.heliohost.org", user="aryan27_coinseedbot", passwd=passwd, database="aryan27_coinseed")
mycursor = mydb.cursor()

#mycursor.execute("DROP TABLE DGUILDS")
#mycursor.execute("DROP TABLE DUSERS")
#mycursor.execute("DROP TABLE DTRANSACTIONS")

#mycursor.execute("CREATE TABLE DGUILDS(GUID BIGINT(20) PRIMARY KEY, CNAM VARCHAR(20), CSYM VARCHAR(60))")
#mycursor.execute("CREATE TABLE DUSERS(DUID BIGINT(20) PRIMARY KEY, GUID BIGINT(20) REFERENCES DGUILDS(GUID), DOC DATETIME, CBAL BIGINT(20), CDC DATETIME)")
#mycursor.execute("CREATE TABLE DTRANSACTIONS(TID BIGINT(20) PRIMARY KEY AUTO_INCREMENT, DONOR BIGINT(20) REFERENCES DUSERS(DUID), RECEIVER BIGINT(20) REFERENCES DUSERS(DUID), PRINCIPLE BIGINT(20), AMOUNT BIGINT(20), LD DATETIME, DD DATETIME)")

#mydb.commit()

#DGUILDS
[('GUID', 'bigint(20)', 'NO', 'PRI', None, ''), 
('CNAM', 'varchar(20)', 'YES', '', None, ''), 
('CSYM', 'varchar(20)', 'YES', '', None, '')]

#DUSERS
[('DUID', 'bigint(20)', 'NO', 'PRI', None, ''), 
('GUID', 'bigint(20)', 'YES', '', None, ''), 
('DOC', 'datetime', 'YES', '', None, ''), 
('CBAL', 'bigint(20)', 'YES', '', None, ''), 
('CDC', 'datetime', 'YES', '', None, '')]

#DTRANSACTIONS
[('TID', 'bigint(20)', 'NO', 'PRI', None, 'auto_increment'), 
('DONOR', 'bigint(20)', 'YES', '', None, ''), 
('RECEIVER', 'bigint(20)', 'YES', '', None, ''), 
('PRINCIPLE', 'bigint(20)', 'YES', '', None, ''), 
('AMOUNT', 'bigint(20)', 'YES', '', None, ''), 
('LD', 'datetime', 'YES', '', None, ''), 
('DD', 'datetime', 'YES', '', None, '')]

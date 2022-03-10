import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="gitpod_db")

mycursor = mydb.cursor()

mycursor.execute("select * from Contact")

result = mycursor.fetchall()

for i in result:
    print(i)
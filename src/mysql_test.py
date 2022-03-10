import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="admin12345", database="gitpod_db")

mycursor = mydb.cursor()

mycursor.execute("select * from contact")

result = mycursor.fetchall()

for i in result:
    print(i)
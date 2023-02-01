import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="MYSQL PASSWORD",
  # database="weather_db",
)
mycursor=mydb.cursor()
mycursor.execute("Create DATABASE weather_db")
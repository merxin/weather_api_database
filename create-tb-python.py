import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="MYSQL PASSWORD",
  database="weather_db",
)

print(mydb)

mycursor=mydb.cursor()

mycursor.execute("Create table forecast(fcst_from DATE, fcst_for_day DATE, city varchar(50), temperature float(5), precipitation varchar(50))")
mydb.commit()
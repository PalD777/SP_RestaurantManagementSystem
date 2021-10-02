import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="server",
  password="SP12345",
  database = "restaurant"
)

print(mydb)
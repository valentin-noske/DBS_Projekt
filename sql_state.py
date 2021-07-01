 
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)

mycursor = mydb.cursor()
indicator = "energieverbrauch"
indicator_tabelle = "energie"
land = "Germany"
mycursor.execute("Select CO2_Emissionen, U.Jahr, "+indicator+" From Land L Join Umweltverschmutzung U ON L.Laenderkuerzel = U.Laenderkuerzel Join "+indicator_tabelle+" X ON L.Laenderkuerzel = X.Laenderkuerzel Where L.Name = "+land+" And U.Jahr BETWEEN 1980 And 2015")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

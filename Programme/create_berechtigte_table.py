from mysql.connector import connect, Error
from getpass import getpass

try: 
    connection= connect(
        host = "localhost",
        user = input ("Enter Username"),
        password = getpass ("Enter password")
    )
    #Tabelle einfügen
    cursor=connection.cursor()
    cursor.execute("use Drucker_Berechtigte")
    sql_query=""" Create Table if not exists berechtigte(
                    id int primary key auto_increment,
                    name varchar(100));               
              """
    cursor.execute(sql_query)
    print("Table created: Berechtigte")




except Error as e:
    print(f"Fehler: {e}")

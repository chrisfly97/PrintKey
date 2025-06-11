from mysql.connector import connect, Error
from getpass import getpass

try: 
    connection= connect(
        host = "localhost",
        user = input ("Enter Username"),
        password = getpass ("Enter password")
    )
    print(connection)
except Error as e:
    print(f"Fehler: {e}")

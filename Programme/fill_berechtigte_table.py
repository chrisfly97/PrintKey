from mysql.connector import connect, Error
from getpass import getpass

try: 
    connection= connect(
        host = "localhost",
        user = input ("Enter Username"),
        password = getpass ("Enter password")
    )
    cursor=connection.cursor()
    cursor.execute("use Drucker_Berechtigte")
    
    

    sql_query="""INSERT INTO  berechtigte  (name) VALUES
    ('Christoph'),
    ('Lenny'),
    ('Johannes');"""

    cursor.execute(sql_query)
    connection.commit()
    print("Database Berechtigte filled with people")
    
    
except Error as e:
    print(f"Fehler: {e}")



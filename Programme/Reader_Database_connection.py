from mfrc522 import SimpleMFRC522
from mysql.connector import connect, Error
import RPi.GPIO as GPIO

def name_suchen(suchname):
    try: 
        connection= connect(
            host = "localhost",
            user = "admin",
            password = "admin"
        )
        #print("Database connected")
        cursor=connection.cursor()
        cursor.execute("use Drucker_Berechtigte")
        
        

        # Suche nach exakter Übereinstimmung
        query = f"SELECT * FROM berechtigte WHERE name = %s"
        cursor.execute(query, (suchname,))  
        
        existiert = cursor.fetchall()
        print(existiert)
        cursor.close()
        connection.close()

        return existiert
        
        
    except Error as e:
        print(f"Fehler: {e}")

def get_name():
    reader = SimpleMFRC522()

    try:
        print("Bitte Tag auflegen...")
        id, text = reader.read()
        return text

    finally:
        GPIO.cleanup()

 
if name_suchen(get_name()) != []:
    print("Du darfst drucken")
else:
    print("Du darfst nicht druckem!")



from mysql.connector import connect, Error
from getpass import getpass
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


def get_name():
    reader = SimpleMFRC522()

    try:
        print("Bitte Tag auflegen...")
        id, text = reader.read()
        return text.strip()  #text ist ein string

    except Error as e:
        print(f"Fehler: {e}")


def tag_beschreiben(name):
    reader = SimpleMFRC522()
    try:
        print("Halten sie den neuen Tag an den Reader")
        reader.write(name)
        print(f"User {name} erfolgreich hinzugefügt")
            
    finally:
        GPIO.cleanup()

def tag_reset():
    reader = SimpleMFRC522()
    try:
        print("Halten sie den alten Tag an den Reader")
        reader.write("")    
        print("Tag wurde zurückgesetzt") 
    finally:
        GPIO.cleanup()

def user_hinzufuegen(name):
    try:
        # Prüfen, ob der Name bereits existiert
        cursor.execute("SELECT * FROM berechtigte WHERE name = %s", (name,)) #Berechtigte nach namen durchsuchen
        if cursor.fetchone(): #fetchone nimmt die erste zeile wo es vorhanden ist und gibt diese als Tupel zurück wann nicht vorhanden None
            print(f"Der Name {name} existiert bereits!")
            tag_beschreiben(name)
        else:
            # Name hinzufügen
            cursor.execute("INSERT INTO berechtigte (name) VALUES (%s)", (name,)) 
            connection.commit()
            print(f"Name {name} erfolgreich hinzugefügt!")
            tag_beschreiben(name)
    except Error as e:
        print(f"Fehler: {e}")

def user_entfernen(name):
    try:
        # Prüfen, ob der Name existiert
        cursor.execute("SELECT * FROM berechtigte WHERE name = %s", (name,)) #Berechtigte nach namen durchsuchen
        if cursor.fetchone(): #fetchone nimmt die erste zeile wo es vorhanden ist und gibt diese als Tupel zurück wann nicht vorhanden None
            cursor.execute("DELETE FROM berechtigte WHERE name = %s", (name,))
            connection.commit()
            tag_reset()
            print(f"user {name} erfolgreich entfernt!")    
        else:
            print(f"Der user existiert nicht! / Tag ist leer")
    except Error as e:
        print(f"Fehler: {e}")


try:
    print("Mit Datenbank verbinden:")
    connection= connect(
        host = "localhost",
        user = input ("Enter Username"),
        password = getpass ("Enter password")
    )
    cursor=connection.cursor()
    cursor.execute("use Drucker_Berechtigte")

except Error as e:
    print(f"Verbindungsfehler: {e}")

while True:
    print("\nMöglichkeiten: add / remove / cancel")
    admin_input = input("Was möchten Sie machen: ")
    if admin_input == "add":
        name = input("Name des neuen users: ")
        user_hinzufuegen(name)
    elif admin_input == "remove":
        name = get_name()
        user_entfernen(name)
    elif admin_input == "cancel":
        print("Programm wird beendet")
        break
    else: 
        print("Falscher input")
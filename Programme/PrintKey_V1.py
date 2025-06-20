from mfrc522 import SimpleMFRC522
from mysql.connector import connect, Error
import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from luma.core.error import DeviceNotFoundError
import time

# Diplay einrichten
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# GPIO-Pins definieren
GREEN_LED_PIN = 27   # Scan möglich
YELLOW_LED_PIN = 22  # 3D-Druck läuft
RED_LED_PIN = 17     # Kein Scan möglich
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def Ausgangsstellung():
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)

    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)  

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((5, 5), "Bitte, Tag auflegen...", fill="white")

def name_suchen(suchname):
    try: 
        connection= connect(
            host = "localhost",
            user = "admin",
            password = "admin"
        )
        cursor=connection.cursor()
        cursor.execute("use Drucker_Berechtigte")
        
        # Suche nach  Übereinstimmung
        query = f"SELECT * FROM berechtigte WHERE name = %s" #%s Platzhalter für Suchname
        cursor.execute(query, (suchname,))  
        
        ergebnis = cursor.fetchall()   # ergebnis ist ein Tupel in einer Liste, [(ID,"Name")]
        cursor.close()
        connection.close()
        return ergebnis
        
    except Error as e:
        print(f"Fehler: {e}")


def get_name():
    reader = SimpleMFRC522()

    try:
        print("Bitte Tag auflegen...")
        id, text = reader.read()
        return text  #text ist ein string

    except Error as e:
        print(f"Fehler: {e}")
        

def get_drucker_state():
    GPIO.setup(YELLOW_LED_PIN, GPIO.IN)
    if GPIO.input(YELLOW_LED_PIN) == True:
        return True
    else:
        return False

try:
    while True:   
        Ausgangsstellung()
        if get_drucker_state() == False:
            GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
            ergebnis = name_suchen(get_name())

            if ergebnis != []:
                name = ergebnis[0][1]
                print(f"Hallo {name}, du darfst drucken")

                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((5, 5), f"Hallo, ", fill="white")
                    draw.text((5, 15), f"{name}", fill="white")
                    draw.text((5, 25), f"du darfst drucken", fill="white")
                time.sleep(3)

                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((5, 5), f"Drucken...", fill="white")
                
                GPIO.output(GREEN_LED_PIN, GPIO.LOW)
                GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
                GPIO.output(RED_LED_PIN, GPIO.HIGH) 
                time.sleep(10)

            else:
                print("Du darfst nicht drucken!du bist nicht berechtigt!")

                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((5, 5), "Du darfst nicht drucken!", fill="white")
                    draw.text((5, 25), "Du bist nicht berechtigt!", fill="white")
        
                GPIO.output(RED_LED_PIN, GPIO.HIGH) 
                GPIO.output(GREEN_LED_PIN, GPIO.LOW)
                time.sleep(5)

except KeyboardInterrupt:
    print("Programm wurde beendet")
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.cleanup()  # Gibt die GPIOs frei

except DeviceNotFoundError as e: 
    print(f"Error: {e} Display nicht verbunden")
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    time.sleep(3)
    print("Programm wurde beendet")
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)

except OSError as e:  
    print(f"I²C-Fehler: {e}. Überprüfe die Verbindung des Displays!")
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    time.sleep(3)
    print("Programm wurde beendet")
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
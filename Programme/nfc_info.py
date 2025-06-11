from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

try:
    print("Bitte Tag auflegen...")
    id, text = reader.read()
    print("Tag-ID:", id)
    print("Inhalt:", text)
except Exception as e:
    print("Fehler:", e)
finally:
    GPIO.cleanup()

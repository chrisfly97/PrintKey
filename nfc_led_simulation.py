
### Programm simuliert 3d-Drucker mittels LED. (Siehe Dokumentation vom 11.06.25 auf GitHub) ###


import RPi.GPIO as GPIO
import time

# GPIO-Pins definieren
GREEN_LED_PIN = 27   # Grün: Zugriff/NFC erkannt
YELLOW_LED_PIN = 22  # Gelb: 3D-Druck läuft
RED_LED_PIN = 17     # Rot: Bereitschaft / Kein NFC

# GPIO einrichten
GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)

def reset_leds():
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.HIGH)  # Bereitschaft

def simulate_nfc_interaction():
    input("NFC-Chip an den Leser halten (ENTER drücken zur Simulation)...")

    # Tag erkannt
    print("NFC erkannt – Zugriff erlaubt. Starte 3D-Druck...")
    
    # LEDs setzen
    GPIO.output(RED_LED_PIN, GPIO.LOW)     # Rot aus
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)  # Grün an
    GPIO.output(YELLOW_LED_PIN, GPIO.HIGH) # Gelb an (Druck läuft)

    # Grüne LED 3 Sekunden, gelbe LED 30 Sekunden
    time.sleep(3)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)   # Grün aus
    GPIO.output(RED_LED_PIN, GPIO.HIGH)    # Rot wieder an

    time.sleep(27)  # Restliche Zeit für Gelb
    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)  # Gelb aus (Druck beendet)
    print("3D-Druck abgeschlossen.")

try:
    print("Starte NFC + 3D-Druck-Simulation. STRG+C zum Beenden.")
    GPIO.output(RED_LED_PIN, GPIO.HIGH)  # Initial: Rot an

    while True:
        simulate_nfc_interaction()

except KeyboardInterrupt:
    print("\nProgramm beendet.")

finally:
    reset_leds()
    GPIO.cleanup()

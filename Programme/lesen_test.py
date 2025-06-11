from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

try:
    print("Bitte Tag auflegen...")
    id, text = reader.read()
    print(f"ID: {id}")
    print(f"Text: {text}")
finally:
    import RPi.GPIO as GPIO
    GPIO.cleanup()

#!/usr/bin/env python3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

text = input('Enter tag data:')
print("Hold tag to module")

# Display logik 
try:
        error = reader.write(text)
        if 584191826653 in error:
                print("FEHLER")
        elif 285658986851 in error:
                print("Done...")

finally:
        GPIO.cleanup()

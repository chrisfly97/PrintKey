#!/usr/bin/env python3
import RPi.GPIO as GPIO
from mfrc522 import MFRC522

def erkenne_tag_typ(sak):
    if sak == 0x08:
        return "MIFARE Classic 1K"
    elif sak == 0x18:
        return "MIFARE Classic 4K"
    elif sak == 0x00:
        return "NTAG (z. B. NTAG213/215/216)"
    else:
        return f"Unbekannt (SAK: 0x{sak:02X})"

try:
    reader = MFRC522()
    print("Bitte Tag auflegen...")

    while True:
        (status, tag_type) = reader.MFRC522_Request(reader.PICC_REQIDL)
        if status != reader.MI_OK:
            continue

        (status, uid) = reader.MFRC522_Anticoll()
        if status != reader.MI_OK:
            continue

        print("\nTag erkannt!")
        print("UID:", ".".join([f"{x:02X}" for x in uid]))

        sak = reader.MFRC522_SelectTag(uid)
        if sak == 0:
            print("Fehler beim Lesen des SAK.")
        else:
            typ = erkenne_tag_typ(sak)
            print("Tag-Typ laut SAK:", typ)

        break

finally:
    GPIO.cleanup()

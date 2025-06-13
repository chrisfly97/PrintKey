while True:
    if name_suchen(get_name()) != []:
        print("Du darfst drucken")
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((5, 20), "Hallo, du darfst drucken", fill="white")
        
    else:
        print("Du darfst nicht druckem!")
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((5, 20), "Du bist nicht berechtigt zu drucken", fill="white")

            
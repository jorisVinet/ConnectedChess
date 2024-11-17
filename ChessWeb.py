import serial
import firebase_admin
from firebase_admin import db, credentials, firestore

# authenticate to firebase
cred = credentials.Certificate("credentials.json")
#firebase_admin.initialize_app(cred, {"databaseURL": "https://chessproject-3b7d3-default-rtdb.europe-west1.firebasedatabase.app/"})
firebase_admin.initialize_app(cred)
db = firestore.client()


def send_data_firestore(document_id, turnNumber, data):
    try:
        # Ajouter des données à la collection
        doc_ref = db.collection("games").document(document_id)
        doc_ref.update({
            "moves": firestore.ArrayUnion([data])
        })
        print(f"Data send")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


# db.reference("/videos").set(3)
# ref.get()

def send_data_firebase(data, turnNumber) : 
    ref = db.reference("/Turn" + str(turnNumber))
    ref.set(data)

def convert_Position_Chess(position) :
    
    x = int(list(position)[3])
    y = int(list(position)[5])
    letters = "abcdefgh"
    chiffres="87654321"
    return f"{letters[x]}{chiffres[y]}"


# Ouvre la connexion série
ser = serial.Serial(port='COM6', baudrate=9600, timeout=.1) 
compteur = 0
positionBefore=""
positionAfter=""
turnNumber = 1
cptDB = 0
try:
    # Boucle infinie pour lire continuellement les données
    while True:
        # Lis une ligne de données du port série
        line = ser.readline().decode().strip()
        res = line.split()
        #DB = Detected Before
        if line.startswith("DB"):
            print("Detected Before trouve")
            cptDB+=1
            if(cptDB==2):
                print("prise du pion : ")
                print(convert_Position_Chess(line))
            else :
                positionBefore = line
                compteur+=1

        elif line.startswith("DA"):
            print("Detected After trouve")
            compteur+=1
            postionAfter = line
        elif line.startswith("ERROR"):
            print("ERROR DETECTION")

        # Affiche la ligne de données
        print(line)
        

        #envoie les information à firebase
        if(compteur==2) : 
            from_position = convert_Position_Chess(positionBefore)
            to_position = convert_Position_Chess(postionAfter)
            print(from_position)
            print(to_position)
            data = {
                'from': from_position,
                'to': to_position
            }
            send_data_firestore("game2", turnNumber, data)
            compteur = 0
            turnNumber+=1
            cptDB = 0

except KeyboardInterrupt:
    # Intercepte une interruption clavier (Ctrl+C) pour arrêter le programme proprement
    print("Arret du programme")
    ser.close()

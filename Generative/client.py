import requests, subprocess
from myjson import *

base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key="
google_api_key= ""
api_url = base_url + google_api_key

print("Benvenuto nella mia generative AI")

def print_dictionary(dData: dict) -> None:
    for keys, values in dData.items():
        print(keys + " - " + values)

def ComponiJsonPerImmagine(sImagePath):
  subprocess.run(["rm", "./image.jpg"])
  subprocess.run(["rm", "./request.json"])
  subprocess.run(["cp", sImagePath,"./image.jpg"])
  subprocess.run(["bash", "./creajsonpersf.sh"])


def CreaInterfaccia():
    print("Operazioni disponibili:")
    print("1. Creare una favola")
    print("2. Rispondere ad una domanda")
    print("3. Rsipondere ad una domanda da un file img")
    print("4. Esci")


sOper: str = '0'
while sOper != "4":

    CreaInterfaccia()
    sOper = input("Seleziona operazione: ")

    if sOper == "1":
        sArgomento = input("Inserisci l'argomento della favola:\n")
        jsonDataRequest = {"contents": [{"parts": [{"text": "Raccontami una favola che parla di " + sArgomento}]}]}
        response = requests.post(api_url, json=jsonDataRequest)
        if response.status_code == 200:
            jsonfile = response.json()
            testo = jsonfile["candidates"][0]["content"]["parts"][0]["text"]
            safety = jsonfile["candidates"][0]["safetyRatings"]
            print()
            print(testo)
            print(safety)

    if sOper == '2':
        response = requests.get(api_url)
        cittadino = response.json()
        if type(cittadino) is dict:
            print_dictionary(cittadino)
        print(f"Status-Code  : {response.status_code}")


    if sOper == '3':
        sFile= input("Inserisci il percorso dell'immagine: ")
        ComponiJsonPerImmagine(sFile)
        dJsonRequest = JsonDeserialize("request.json")
        sDomanda = input("Fai una domanda sull'immagine: ")
        dJsonRequest["content"][0]["parts"][0]["text"] = sDomanda
        response = requests.post(api_url, json=dJsonRequest)
        print(response.status_code)
        if response.status_code == 200:
            jsonfile = response.json()
            testo = jsonfile["candidates"][0]["content"]["parts"][0]["text"]
            safety = jsonfile["candidates"][0]["safetyRatings"]
            print()
            print(testo)
            print(safety)
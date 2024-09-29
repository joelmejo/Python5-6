import requests
from requests.auth import HTTPBasicAuth
import urllib3
import time
import sys

# Disabilita l'avviso di sicurezza
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app_url = "https://127.0.0.1:8080/"
username = ""
password = ""

def acquisisciCredenziali():
    global username, password
    username = input("Inserisci l'username: ")
    password = input("Inserisci la password: ")

print("Client Anagrafe")
acquisisciCredenziali()

def print_dictionary(dData):
    for keys, values in dData.items():
        print(keys + " - " + values)

def menuOperazioni():
    print("1. Inserisci cittadino")
    print("2. Visualizza cittadini")
    print("3. Modifica cittadino")
    print("4. Elimina cittadino")
    print("5. Cambia credenziali")
    print("6. Exit")
    comando = input()
    return comando

def getDatiCittadino():
    nome = input("Inserisci il nome: ")
    cognome = input("Inserisci il cognome: ")
    data_nascita = input("Inserisci la data di nascita: ")
    codice_fiscale = input("Inserisci il codice fiscale: ")
    return [nome, cognome, data_nascita, codice_fiscale]

while True:
    time.sleep(2)
    print()
    print("Digita cosa vuoi fare:")
    azione = menuOperazioni()

    if azione == "1":
        if username != "" and password != "":
            data = getDatiCittadino()
            try:
                response = requests.post(app_url + "inserisci_cittadino",json=data, verify=False, auth=HTTPBasicAuth(username, password))
                #print(response.json())
                print(response.status_code)
                print(response.headers["Content-Type"])

                if type(response.json()) is dict:
                    print_dictionary(response.json())
            except:
                time.sleep(2)
        else:
            print("Devi inserire le credenziali per eseguire questo comando!")
    
    if azione == "2":
        cittadini = requests.get(app_url + "get_cittadini", verify=False, auth=HTTPBasicAuth(username, password))
        print(cittadini.text)
    
    if azione == "3":
        if username != "" and password != "":
            cf = input("Inserisci il codice fiscale del cittadino che vuoi modificare: ")
            data = getDatiCittadino()
            try:
                response = requests.put(app_url + "modifica_cittadino/" + cf, json=data, verify=False, auth=HTTPBasicAuth(username, password))
                print(response.status_code)
                print(response.headers["Content-Type"])
                if type(response.json()) is dict:
                    print_dictionary(response.json())
            except:
                time.sleep(2)
        else:
            print("Devi inserire le credenziali per eseguire questo comando!")

    if azione == "4":
        if username != "" and password != "":
            cf = input("Inserisci il codice fiscale del cittadino che vuoi eliminare: ")
            try:
                response = requests.delete(app_url + "elimina_cittadino/" + cf, verify=False, auth=HTTPBasicAuth(username, password))
                print(response.status_code)
                print(response.headers["Content-Type"])
                if type(response.json()) is dict:
                    print_dictionary(response.json())
            except:
                time.sleep(2)
        else:
            print("Devi inserire le credenziali per eseguire questo comando!")

    if azione == "5":
        acquisisciCredenziali()
    
    if azione == '6':
        sys.exit()
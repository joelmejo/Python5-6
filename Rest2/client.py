import json, requests
from requests.auth import HTTPBasicAuth

base_url = "http://127.0.0.1:8080"

def print_dictionary(dData: dict) -> None:
    for keys, values in dData.items():
        print(keys + " - " + values)


def RichiediDatiCittadino() -> dict:
    nome = input("inserisci nome cittadino: ")
    cognome = input("inserisci cognome cittadino: ")
    dataNascita = input("inserisci data nascita: ")
    codFiscale = input("Inserisci codice fiscale: ")
    jRequest = {"nome":nome, "cognome":cognome, "data nascita":dataNascita,"codice fiscale":codFiscale }
    return jRequest

def CreaInterfaccia():
    print("Operazioni disponibili:")
    print("1. Inserisci cittadino (es. atto di nascita)")
    print("2. Richiedi dati cittadino (es. cert. residenza)")
    print("3. Modifica dati cittadino")
    print("4. Elimina cittadino")
    print("5. Exit")

def datiLogin():
    global username, password, privilegi, login_eseguito
    username = input("Inserisci l'username: ")
    password = input("Inserisci la password: ")

def ControlLogin():
    global login_eseguito
    api_url = base_url + "/login"
    jRequest: dict= {"username": username, "password": password}
    try:
        response = requests.post(api_url,json=jRequest)
        print(response.headers["Content-Type"])
        data1 = response.json()
        privilegi = data1["Privilegi"]
        print(data1)
        login_eseguito = 1
    except:
        login_eseguito = 0
        print("Errore")
    print(f"Status-Code  : {response.status_code}")


login_eseguito: int= 0
username: str= ""
password: str= ""
privilegi: str= ""

while login_eseguito == 0:
    ControlLogin()

sOper = None
while (sOper != "5"):

    CreaInterfaccia()
    sOper = input("Seleziona operazione")

    if sOper == "1":
        api_url = base_url + "/add_cittadino"
        jsonDataRequest = RichiediDatiCittadino()
        try:
            response = requests.post(api_url,json=jsonDataRequest, auth=HTTPBasicAuth(username, password))
            print(response.status_code)
            print(response.headers["Content-Type"])
            data1 = response.json()
            print(data1)
        except:
            print("Errore")
    print(f"Status-Code  : {response.status_code}")

    if sOper == '2':
        response = requests.get(api_url + "get_cittadini", verify=False, auth=HTTPBasicAuth(username, password))
        cittadino = response.json()
        if type(cittadino) is dict:
            print_dictionary(cittadino)
        print(f"Status-Code  : {response.status_code}")

    if sOper == '3':
        cf: str = input("Inserisci il codice fiscale del cittadino che vuoi modificare: ")
        print("Inserisci i nuovi dati del cittadino")
        data = RichiediDatiCittadino()

        response = requests.put(api_url + "modifica_cittadino/" + cf, json=data, verify=False, auth=HTTPBasicAuth(username, password))
        print(response.status_code)
        print(response.headers["Content-Type"])
        if type(response.json()) is dict:
            print_dictionary(response.json())
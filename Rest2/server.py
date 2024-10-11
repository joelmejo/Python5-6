from flask import Flask, json, request
from myjson import JsonSerialize,JsonDeserialize
import base64

sFileAnagrafe: str= "./anagrafe.json"
dAnagrafe = JsonDeserialize(sFileAnagrafe)
sFileUtenti: str= "./utenti.json"
dUtenti = JsonDeserialize(sFileUtenti)
api = Flask(__name__)

def authentication(auth) -> int:
    #lettura dati basic authentication per VERIFICA
    auth = auth[6:]

    security_data = base64.b64decode(auth).decode("utf-8")
    # print(security_data)
    username, password = security_data.split(":")
    if username in dUtenti:
        if dUtenti[username]["password"] == password:
            if dUtenti[username]["privilegi"] == "rw":
                return 2
            return 1
    # print("Utente e/o password errati")
    return 0

@api.route('/login', methods=['POST'])
def GestisciLogin():
    #prendi i dati della richiesta
    content_type = request.headers.get('Content-Type')
    print("Ricevuta chiamata " + content_type)
    if content_type=="application/json":
        jRequest = request.json
        cUsername = jRequest["username"]
        cPassword = jRequest["password"]
        if cUsername in dUtenti:
            if dUtenti[cUsername]["password"] == cPassword:
                sPriv = dUtenti[cUsername]["privilegi"]
                jResponse = {"Esito": "000", "Msg": "Utente registrato", "Privilegi": sPriv}
                return json.dumps(jResponse), 200
            else:
                jResponse = {"Esito": "001", "Msg": "Utente o password errati"}
                return json.dumps(jResponse)
        else:
            jResponse = {"Esito": "001", "Msg": "Utente o password errati"}
            return json.dumps(jResponse)
    else:
        return "Errore, formato non riconosciuto", 401

@api.route('/add_cittadino', methods=['POST'])
def GestisciAddCittadino():

    auth_response = authentication(request.headers.get('Authorization'))
    if auth_response == 0:
        response = {"Esito":"KO","Msg":"Username e/o password errati"}	
        return json.dumps(response), 401
    elif auth_response == 1:
        print("Utente non autorizzato ad eseguire questa operazione")
        response = {"Esito":"KO","Msg":"Non sei autorizzato ad eseguire questa operazione"}	
        return json.dumps(response), 403
    else:
        print("Autenticazione riuscita!")

    #prendi i dati della richiesta
    content_type = request.headers.get('Content-Type')
    print("Ricevuta chiamata " + content_type)
    if content_type=="application/json":
        jRequest = request.json
        sCodiceFiscale = jRequest["codice fiscale"]
        print("Ricevuto " + sCodiceFiscale)
        if sCodiceFiscale not in dAnagrafe:
            dAnagrafe[sCodiceFiscale] = jRequest
            JsonSerialize(dAnagrafe,sFileAnagrafe)
            jResponse = {"Error":"000", "Msg": "ok"}
            return json.dumps(jResponse), 200
        else:
            jResponse = {"Error":"001", "Msg": "codice fiscale gia presente in anagrafe"}
            return json.dumps(jResponse), 200
    else:
        return "Errore, formato non riconosciuto", 401
    #controlla che il cittadino non è gia presente in anagrafe
    #rispondi

@api.route('/get_dati_cittadino', methods=['GET'])
def gestisciGetCittadino():

    auth_response = authentication(request.headers.get('Authorization'))
    if auth_response == 0:
        response = {"Esito":"KO","Msg":"Username e/o password errati"}	
        return json.dumps(response), 401
    elif auth_response == 1:
        print("Utente non autorizzato ad eseguire questa operazione")
        response = {"Esito":"KO","Msg":"Non sei autorizzato ad eseguire questa operazione"}	
        return json.dumps(response), 403
    else:
        print("Autenticazione riuscita!")


    content_type = request.headers.get('Content-Type')

    print("Ricevuta chiamata " + content_type)
    if content_type=="application/json":
        jRequest = request.json
        sCodiceFiscale = jRequest["codice fiscale"]
        print("Ricevuto " + sCodiceFiscale)

        if sCodiceFiscale in dAnagrafe:
            return json.dumps(dAnagrafe[sCodiceFiscale]), 200
        else:
            response: dict= {"Esito": "KO", "Msg": "Cittadino non trovato"}
            return json.dumps(response), 404

api.run(host="127.0.0.1", port=8080)
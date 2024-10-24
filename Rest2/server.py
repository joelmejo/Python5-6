from flask import Flask, json, request
from myjson import JsonSerialize, JsonDeserialize
import base64, cryptography

sFileAnagrafe: str= "./anagrafe.json"
dAnagrafe = JsonDeserialize(sFileAnagrafe)
sFileUtenti: str= "./utenti.json"
dUtenti = JsonDeserialize(sFileUtenti)
api = Flask(__name__)

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

api.run(host="127.0.0.1", port=8080, ssl_context="adhoc")
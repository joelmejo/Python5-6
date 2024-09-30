from flask import Flask, json, request
from myjson import JsonSerialize,JsonDeserialize
# import sys

# lListaCampil = ["nome", "cognome", "data nascita", "codice fiscale"]
# if campoRicevutoDalClient in lListaCampi:

# sfile = "./prova.json"
# mydict = {'nome': 'mario', 'cognome': 'rossi'}
# falso = 1
# iRet = JsonSerialize(mydict, sfile)
# if iRet == 0:
#     print("Operazione terminata correttamente")
# elif iRet == 1:
#     print("Errore, atteso dizionario")
# elif iRet == 2:
#     print("Errore salvataggio su file")
# sys.exit()
    

sFileAnagrafe = "./anagrafe.json"
api = Flask(__name__)

@api.route('/add_cittadino', methods=['POST'])
def GestisciAddCittadino():
    #prendi i dati della richiesta
    content_type = request.headers.get('Content-Type')
    print("Ricevuta chiamata " + content_type)
    if content_type=="application/json":
        jRequest = request.json
        sCodiceFiscale = jRequest["codice fiscale"]
        print("Ricevuto " + sCodiceFiscale)
        #carichiamo l'anagrafe
        dAnagrafe = JsonDeserialize(sFileAnagrafe)
        if sCodiceFiscale not in dAnagrafe:
            dAnagrafe[sCodiceFiscale] = jRequest
            JsonSerialize(dAnagrafe,sFileAnagrafe)
            jResponse = {"Error":"000", "Msg": "ok"}
            return json.dumps(jResponse),200
        else:
            jResponse = {"Error":"001", "Msg": "codice fiscale gia presente in anagrafe"}
            return json.dumps(jResponse),200
    else:
        return "Errore, formato non riconosciuto",401
    #controlla che il cittadino non è gia presente in anagrafe
    #rispondi

@api.route('/get_dati_cittadino', method = ['GET'])
def gestisciGetCittadino():
    content_type = request.headers.get('Content-Type')

    print("Ricevuta chiamata " + content_type)
    if content_type=="application/json":
        jRequest = request.json
        sCodiceFiscale = jRequest["codice fiscale"]
        print("Ricevuto " + sCodiceFiscale)
        #carichiamo l'anagrafe
        dAnagrafe = JsonDeserialize(sFileAnagrafe)
        if sCodiceFiscale in dAnagrafe:
            return json.dumps(dAnagrafe[sCodiceFiscale]), 200
        else:
            response: dict= {"Esito": "KO", "Msg": "Cittadino non trovato"}
            return json.dumps(response), 404

api.run(host="127.0.0.1", port=8080)
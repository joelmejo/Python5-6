from flask import Flask, json, request
import base64
import cryptography


utenti = [["mario", "12345", "rw"], ["franco", "6789", "r"]]

cittadini = [{"nome": "Mario", "cognome": "Rossi", "dataNascita": "20/02/1990","codFiscale":"dfcged90b28h501u"},
             {"nome": "Mario", "cognome": "Bianchi", "dataNascita": "20/02/1990","codFiscale":"dfcged90b28h501u"},
             {"nome": "Giuseppe", "cognome": "Verdi", "dataNascita": "20/12/1956","codFiscale":"dfcvds90b28h501u"}]

app = Flask(__name__)

def authentication(auth):
    #lettura dati basic authentication per VERIFICA
    auth = auth[6:]

    security_data = base64.b64decode(auth).decode("utf-8")
    print(security_data)
    username, password = security_data.split(":")
    for u in utenti:
        if u[0] == username:
            if u[1] == password:
                if u[2] == 'rw':
                    return 2
                else:
                    return 1
    print("Utente e/o password errati")
    return 0

def find_citizen(cf: str) -> list:
    cittadino_trovato = None
    for c in cittadini:
        if c['codFiscale'] == cf:
            cittadino_trovato = c
            break
    return cittadino_trovato

@app.route('/inserisci_cittadino', methods=['POST'])
def process_json():
    print("Ricevuta chiamata")

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
    if (content_type == 'application/json'):
        json1 = request.json
        print(json1)
        cittadini.append(json1)
        response = {"Esito":"ok","Msg":"Dato inserito"}	
        return json.dumps(response), 200
    else:
        return 'Content-Type not supported!'

@app.route('/get_cittadini', methods=['GET'])
def get_cittadini():
    print("Ricevuta chiamata")

    auth_response = authentication(request.headers.get('Authorization'))
    if auth_response == 0:
        response = {"Esito":"KO","Msg":"Username e/o password errati"}	
        return json.dumps(response), 401
    else:
        print("Autenticazione riuscita!")
    return json.dumps(cittadini), 200

@app.route('/modifica_cittadino/<string:cf>', methods=['PUT'])
def update_cittadini(cf):
    print("Ricevuta chiamata")

    auth_response = authentication(request.headers.get('Authorization'))
    if auth_response == 0:
        response = {"Esito":"KO","Msg":"Username e/o password errati"}	
        return json.dumps(response), 401
    elif auth_response == 1:
        print("Utente non autorizzato")
        response = {"Esito":"KO","Msg":"Non sei autorizzato ad eseguire questa operazione"}	
        return json.dumps(response), 403
    else:
        print("Autenticazione riuscita!")
    
    cittadino_trovato = find_citizen(cf)

    if cittadino_trovato == None:
        print("Cittadino non trovato")
        response = {"Esito":"KO","Msg":"Cittadino non trovato"}	
        return json.dumps(response), 404
    
    
    content_type = request.headers.get('Content-Type')
    print("Ricevuta chiamata " + content_type)
    if (content_type == 'application/json'):
        nuovi_dati = request.json
        print(nuovi_dati)
        cittadino_trovato = nuovi_dati
        response = {"Esito":"ok","Msg":"Dato modificato"}	
        return json.dumps(response), 200
    else:
        return 'Content-Type not supported!'
    
@app.route('/elimina_cittadino/<string:cf>', methods=['DELETE'])
def delete_cittadini(cf):
    print("Ricevuta chiamata")

    auth_response = authentication(request.headers.get('Authorization'))
    if auth_response == 0:
        response = {"Esito":"KO","Msg":"Username e/o password errati"}	
        return json.dumps(response), 401
    elif auth_response == 1:
        print("Utente non autorizzato")
        response = {"Esito":"KO","Msg":"Non sei autorizzato ad eseguire questa operazione"}	
        return json.dumps(response), 403
    else:
        print("Autenticazione riuscita!")
    
    cittadino_trovato = find_citizen(cf)

    if cittadino_trovato == None:
        print("Cittadino non trovato")
        response = {"Esito":"KO","Msg":"Cittadino non trovato"}	
        return json.dumps(response), 404
    
    cittadini.remove(cittadino_trovato)
    response = {"Esito":"ok","Msg":"Dato eliminato"}	
    return json.dumps(response), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, ssl_context = "adhoc")
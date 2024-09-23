from flask import Flask, json, request
import base64
import cryptography


utenti = [["mario", "12345", "rw"], ["franco", "6789", "r"]]

cittadini: list = [["Mario", "Rossi", "01/01/2000", "KRT897AHSJ"]]

api = Flask(__name__)

def authentication(username, password):
    for u in utenti:
        if u[0] == username:
            if u[1] == password:
                return True
            else:
                print("Password errata")
                return False
        else:
            print("Utente errato")
            return False

@api.route('/inserisci_cittadino', methods=['POST'])
def process_json():
    print("Ricevuta chiamata")

    #lettura dati basic authentication per VERIFICA
    auth = request.headers.get('Authorization')
    auth = auth[6:]

    security_data = base64.b64decode(auth).decode("utf-8")
    print(security_data)
    username, password = security_data.split(":")
    if authentication(username, password) is False:
        print("Autenticazione non riuscita")
        return

    content_type = request.headers.get('Content-Type')
    print("Ricevuta chiamata " + content_type)
    if (content_type == 'application/json'):
        json1 = request.json
        print(json1)
        cittadini.append(json1)
        response = {"Esito":"ok","Msg":"Dato inserito"}	
        return json.dumps(response)
    else:
        return 'Content-Type not supported!'

@api.route('/get_cittadini', methods=['GET'])
def get_cittadini():
    return json.dumps(cittadini)

# @api.route('/modifica_cittadino', methods=['POST'])

if __name__ == '__main__':
    api.run(host="0.0.0.0", port=8080, ssl_context = "adhoc")
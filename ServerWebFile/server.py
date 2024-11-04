from flask import Flask, render_template, request
import requests, base64

api = Flask(__name__)

with open('pgkey.txt', 'r') as file:
    google_api_key = file.read()

base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-exp-0827:generateContent?key="
api_url = base_url + google_api_key

@api.route('/', methods=['GET'])
def index():
    return render_template('sendfile.html')

@api.route('/mansendfile', methods=['POST'])
def mansendfile():
    richiesta = request.form['richiesta']
    if 'image' in request.files:
        file = request.files['image']
        jsonDataRequest = {         
        "contents":[
            {
            "parts":[
                {"text": richiesta},
                {
                "inline_data": {
                    "mime_type":"image/jpeg",
                    "data": base64.b64encode(file.read()).decode('utf-8')
                }
                }
            ]
            }
        ]
        }
    else:
        jsonDataRequest = {"contents": [{"parts": [{"text": richiesta}]}]}
    response = requests.post(api_url, json=jsonDataRequest)
    if response.status_code == 200:
        jsonfile = response.json()
        testo = jsonfile["candidates"][0]["content"]["parts"][0]["text"]
        return "<HTML><BODY>" + testo + "<BODY><HTML>"
    return "<HTML><BODY>" + str(response.status_code) + "<BODY><HTML>"

api.run(host="www.cyberits.com",port=8085,ssl_context=("./Certs/01.pem","./Certs/localhost.key"))
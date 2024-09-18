from flask import Flask, render_template, request


utenti= [["mariorossi@gmail.com", "dsrfde43rfd", "pippo", False]]


api = Flask("__name__")

@api.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# @api.route('/regok', methods=['GET'])
# def regOK():
#     return render_template('regOK.html')

# api.route('/regko', methods=['GET'])
# def regKO():
#     return render_template('regKO.html')

@api.route('/registrati', methods=['GET'])
def registra():
    cF = request.args.get("codfisc")
    print("Nome inserito: " + cF)
    mail = request.args.get("email")
    print("Email inserita: " + mail)
    password = request.args.get("pwd")
    print("Password inserita: " + password)

    utente = [mail, cF, password, False]

    if utente in utenti:
        index = utenti.index(utente)
        utenti[index][3] = True
        return render_template('regOK.html')
    else:
        return render_template('regKO.html')

api.run(host="0.0.0.0", port=8085)


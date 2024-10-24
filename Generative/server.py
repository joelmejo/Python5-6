from flask import Flask, render_template, request


utenti= [["mariorossi@gmail.com", "dsrfde43rfd", "pippo", False]]


api = Flask("__name__")

@api.route('/', methods=['GET'])
def index():
    return render_template('sendfile.html')

# @api.route('/mansendfile', methods=['GET'])
# def index():
#     sMailRicevuta = request.form("email")
#     sResponsePage = "<html><body><h1>Buongiorno" + sMailRicevuta + " a tutti, il 17 settembre 2024</h1></body></html>"
#     return sResponsePage


api.run(host="0.0.0.0", port=8085, ssl_context="adhoc")


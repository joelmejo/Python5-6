import os
import dbclient as db
import sys
import json

mydb = db.connect()
if mydb is None:
    print("Errore connessione al db")
    sys.exit
else:
    print("Connessione avvenuta correttamente")

cittadini: dict = {}
with open("anagrafe.json", "r") as json_file:
    cittadini = json.load(json_file)

for key, item in cittadini.items():
    cod_fiscale = key
    nome = item["nome"]
    cognome = item["cognome"]
    dataNascita = item["dataNascita"]
    sQuery = f"insert into cittadini(codice_fiscale,nome,cognome,data_nascita)" + " values('{cod_fiscale}','{nome}','{cognome}','{dataNascita}')"
    print(sQuery)
    db.write_in_db(mydb,sQuery)

db.close(mydb)
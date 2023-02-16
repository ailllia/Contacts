import ast, os, datetime
import json
from flask import Flask, jsonify, request
app = Flask(__name__)

def get_contacts(): #funktion, die auf die Kontakt-Datei zugreift und ihren Inhalt zurückgibt
    f = open('Telefonbuch/contacts.json', 'a+', encoding="utf-8")
    if os.stat('Telefonbuch/contacts.json').st_size == 0:
        file_contents = {}
    else:
        f.seek(0)
        file_contents = ast.literal_eval(f.read())
    f.close()
    return(file_contents)

@app.route('/contacts/<string:name>', methods=['GET']) #gibt einzelnen Kontakt aus bei Aufruf http://127.0.0.1:5000/contacts/Anna
def find_name(name):
    contacts = ast.literal_eval(str(get_contacts()))
    name #= request.args.get('name')
    for x in contacts:
        if x == name:
            return {name:contacts.get(x)}
    return "Does not exist."

@app.route('/contacts', methods=['GET']) #gibt alle Kontakte aus bei Aufruf http://127.0.0.1:5000/contacts
def output():
    return get_contacts()

app.run()
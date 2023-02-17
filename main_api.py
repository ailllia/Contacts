#REST-API
#folgende Befehle sind möglich:
# GET -> done
# POST -> done
# PUT
# PATCH
# DELETE
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

def update_contacts(contacts): #Funktion, die die contacts.json updated, wenn etwas geändert wurde
    f = open('Telefonbuch/contacts.json', 'w', encoding="utf-8") #w = edit
    f.write(str(contacts))
    f.close()
    return

def find_name_bool(searched_name): # gibt True zurück, wenn Name schon existiert
    names = ast.literal_eval(str(get_contacts()))
    for x in names:
        if x == searched_name:
            return True
    return False

@app.route('/contacts/<string:name>', methods=['GET']) #gibt einzelnen Kontakt aus bei Aufruf http://127.0.0.1:5000/contacts/Anna
def find_name(name):
    contacts = ast.literal_eval(str(get_contacts()))
    name #= request.args.get('name')
    for x in contacts:
        if x == name:
            return {name:contacts.get(x)}
    return "Does not exist."

@app.route('/contacts', methods=['GET', 'POST']) 
def home():
    if request.method == 'GET': #gibt alle Kontakte aus bei GET-Aufruf http://127.0.0.1:5000/contacts
        return get_contacts()
    else:                       #fügt Kontakt hinzu bei POST-Aufruf http://127.0.0.1:5000/contacts?name=Erik&number=123456
        return add_contact()

#@app.route('/contacts/new', methods=['POST']) 
def add_contact(): #Funktion, die einen neuen Kontakt hinzufügt, falls der Name noch nicht existiert
    name = request.args.get('name')
    number = request.args.get('number')
    if find_name_bool(name):
        return f'Contact {name}: {number} already exists.'
    contacts = get_contacts()
    contacts.update({name: number})
    update_contacts(contacts)
    return f'Added {name}: {number} to contacts.'

app.run()
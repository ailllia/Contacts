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
    file_contents = {} #BP: Vor Verwendung initialisieren
    f = open('contacts.json', 'a+', encoding="utf-8")
    if os.stat('contacts.json').st_size != 0:
        f.seek(0)
        file_contents = ast.literal_eval(f.read())
    f.close()
    return(file_contents)

def update_contacts(contacts): #Funktion, die die contacts.json updated, wenn etwas geändert wurde
    f = open('contacts.json', 'w', encoding="utf-8") #w = edit
    f.write(str(contacts))
    f.close()
    return

def name_exists(searched_name): # gibt True zurück, wenn Name schon existiert
    names = ast.literal_eval(str(get_contacts()))
    return searched_name in names


@app.errorhandler(404)
def page_not_found(e):
    return "Content does not exist."

@app.route('/contacts/<string:name>', methods=['GET']) #gibt einzelnen Kontakt aus bei Aufruf http://127.0.0.1:5000/contacts/Anna
def find_contact(name):
    contacts = ast.literal_eval(str(get_contacts()))
    #name = request.args.get('name')
    if name in contacts:
        return {name:contacts.get(name)}
    return flask.redirect('/404') # BP: return http 404 code

@app.route('/contacts', methods=['GET', 'POST']) 
def home():
    if request.method == 'GET': #gibt alle Kontakte aus bei GET-Aufruf http://127.0.0.1:5000/contacts
        return get_contacts()
    elif request.method == 'POST': #fügt Kontakt hinzu bei POST-Aufruf http://127.0.0.1:5000/contacts?name=Erik&number=123456
        return add_contact()

#@app.route('/contacts/new', methods=['POST']) 
def add_contact(): #Funktion, die einen neuen Kontakt hinzufügt, falls der Name noch nicht existiert
    name = request.args.get('name')
    number = request.args.get('number')
    if name_exists(name):
        return f'Contact {name}: {number} already exists.'
    contacts = get_contacts()
    contacts.update({name: number})
    update_contacts(contacts)
    return f'Added {name}: {number} to contacts.'

app.run()
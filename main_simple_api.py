#REST-API
#folgende Funktionen in main_simple: 
#create new contact -> done
#read your contacts -> done
#edit a contact
#delete a contact
#folgende Befehle sind möglich:
# GET to get-> done
# POST for create operations -> done
# PUT for updating or creating - full replacement of a document (info in body), updates the entire resource at once
# PATCH for change or adding data - only updates the fields that we pass
# DELETE
import ast, os, datetime
import json
from flask import Flask, jsonify, request
import flask
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

@app.errorhandler(409)
def page_not_found(e):
    return "Content does already exist."

def add_contact(): #Funktion, die einen neuen Kontakt hinzufügt, falls der Name noch nicht existiert
    name = request.args.get('name')
    number = request.args.get('number')
    if name_exists(name):
        return flask.redirect('/409')
    contacts = get_contacts()
    contacts.update({name: number})
    update_contacts(contacts)
    return f'Added {name}: {number} to contacts.',200

def delete_contact():
    name = request.args.get('name')
    if not name_exists(name):
        return flask.redirect('/404')
    contacts = get_contacts()
    number = contacts.get(name)
    contacts.pop(name)
    update_contacts(contacts)
    return f'Deleted {name}: {number} from contacts.',200

@app.route('/contacts/<string:name>', methods=['GET']) #gibt einzelnen Kontakt aus bei Aufruf http://127.0.0.1:5000/contacts/Anna
def find_contact(name):
    contacts = ast.literal_eval(str(get_contacts()))
    #name = request.args.get('name')
    if name in contacts:
        return {name:contacts.get(name)}
    return flask.redirect('/404') # BP: return http 404 code

@app.route('/contacts', methods=['GET', 'POST', 'DELETE']) 
def home():
    if request.method == 'GET': #gibt alle Kontakte aus bei GET-Aufruf http://127.0.0.1:5000/contacts
        return get_contacts()
    elif request.method == 'POST': #fügt Kontakt hinzu bei POST-Aufruf http://127.0.0.1:5000/contacts?name=Erik&number=123456
        return add_contact()
    elif request.method == 'DELETE':
        return delete_contact()

app.run()
import ast, os, datetime

def get_contacts():
    f = open('Telefonbuch/contacts.json', 'a+', encoding="utf-8")
    if os.stat('Telefonbuch/contacts.json').st_size == 0:
        file_contents = {}
    else:
        f.seek(0)
        file_contents = ast.literal_eval(f.read())
    f.close()
    return(file_contents)

def update_contacts(contacts):
    f = open('Telefonbuch/contacts.json', 'w', encoding="utf-8") #w = edit
    f.write(str(contacts))
    f.close()
    return

def find_name(searched_name):
    names = ast.literal_eval(str(get_contacts()))
    for x in names:
        if x == searched_name:
            return True
    return False

def create():
    # immer 'b' zum zurückgehen
    name = input('b - back to menu\nEnter the Name of the new Contact: ')
    if name == 'b':
        return
    #Abfragen, ob name/ kontakt schon vorhanden und entsprechende Nachricht anzeigen
    if find_name(name):
        user_confirmation = input(f'There already exists a contact with the name {name}, do you want to continue? (y/n)')
        if user_confirmation != 'y':
            return
    number = input('b - back to menu\nEnter the Number of the new contact: ')
    if number == 'b':
        return    
    #neue Kontaktinfos bestätigen lassen
    user_confirmation = input(f'b - back to menu\nAdd "{name}: {number}" to contacts? (y/n)')
    if user_confirmation != 'y':
        return
    contacts = get_contacts()
    contacts.update({name: number})
    update_contacts(contacts)
    print('Contact successfully added.')
    #fragen, ob noch ein Kontakt angelegt werden soll oder zurück
    user_confirmation = input('Do you want to add another contact? (y/n)')
    if user_confirmation == 'y':
        return create()
    return

def output():
    #kontaktliste printen, dann zurück
    contacts = str(get_contacts())
    for character in "{'}":
        contacts = contacts.replace(character, '')
    print(contacts)
    return

def delete():
    #immer 'b' zum zurückgehen
    name = input('b - back to menu\nEnter the Name of the contact you want to delete: ')
    if name == 'b':
        return
    if not find_name(name):
        print('No such name in contacts.')
        return
    else: 
        contacts = get_contacts()
        number = contacts.get(name)
    #löschen von Nutzer bestätigen lassen, dann zurück
    user_confirmation = input(f'b - back to menu\nDelete "{name}: {number}" from contacts? (y/n)')
    if user_confirmation != 'y':
        return
    else:
    #einen Kontakt zum löschen heraussuchen
        contacts.pop(name)
        update_contacts(contacts)
        print('Contact successfully deleted.')
    return

def get_choice(letter):
    match letter:
        case 'c':
            return create()
        case 'r':
            return output()
        case 'd':
            return delete()
        case 'x':
            print('Good Bye!')
            return
        case _:
            print('Invalid Input.')
            return

def get_greeting():
    my_date = datetime.datetime.now()    # Get current datetime
    #current_hour = my_date.hour          # Applying hour attribute of datetime module
    current_hour = 23
    if current_hour >= 5 and current_hour < 11:
        return ('Good Morning!')
    if current_hour >= 11 and current_hour < 14:
        return ('Hello!')
    if current_hour >= 14 and current_hour < 18:
        return ('Good Afternoon!')
    if current_hour >= 18:
        return ('Good Evening!')
    return ('Good Night!')

def start ():
    user_command = ''
    print(get_greeting())
    while user_command != 'x':
        #Main menu:
        print(' c - create new contact\n r - read your contacts\n d - delete a contact\n x - close program')
        user_command = input('Enter here: ')
        get_choice(user_command)
    return

start()
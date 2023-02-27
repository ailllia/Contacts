import ast, os, datetime

def get_contacts():
    file_contents = {} #BP: Vor Verwendung initialisieren
    f = open('contacts.json', 'a+', encoding="utf-8")
    if os.stat('contacts.json').st_size != 0:
        f.seek(0)
        file_contents = ast.literal_eval(f.read())
    f.close()
    return(file_contents)

def update_contacts(contacts):
    f = open('contacts.json', 'w', encoding="utf-8") #w = edit
    f.write(str(contacts))
    f.close()
    return

def name_exists(searched_name):
    names = ast.literal_eval(str(get_contacts()))
    return searched_name in names
# alte Version:
# def name_exists(searched_name):
#     names = ast.literal_eval(str(get_contacts()))
#     for x in names:
#         if x == searched_name:
#             return True
#     return False

def find_contact(name):
    contacts = ast.literal_eval(str(get_contacts()))
    #name = request.args.get('name')
    if name in contacts:
        return {name:contacts.get(name)}
    return None

def create():
    # immer 'b' zum zurückgehen
    name = input('b - back to menu\nEnter the Name of the new Contact: ')
    if name == 'b':
        return
    #Abfragen, ob name/ kontakt schon vorhanden und entsprechende Nachricht anzeigen
    if name_exists(name):
        user_confirmation = input(f'There already exists a contact with the name {name} that will be overridden, do you want to continue? (y/n)')
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

def update_contact(name=None):
    if name == None:
        name = input('b - back to menu\nEnter the Name of the contact you want to edit: ')
    #ist name ein kontakt?
    contact = find_contact(name)
    if contact == None:
        print(f'{name} does not exist.')
        return
    #wenn ja - name: nummer ausgeben und fragen, ob name oder nummer geändert werden soll
    command = input('What do you want to edit?\nn - name\nt - telephone number\nEnter here: ')
    #name ändern
    old_name, new_name = name, name
    old_number, new_number = contact[name], contact[name]
    if command == 'n':
        new_name = input('Enter the new name: ')
        while name_exists(new_name):
            new_name = input('The name you entered already exists. Enter another new name: ')
    #nummer ändern
    elif command == 't':
        new_number = input('Enter the new number: ')
        #neuen kontakt anzeigen und bestätigen lassen
    command = input(f'Change {old_name}: {old_number} into {new_name}: {new_number}? (y/n)')
    if command == 'y':
        contacts = get_contacts()
        contacts.update({new_name: new_number})
        if new_name is not old_name:
            contacts.pop(old_name)
        update_contacts(contacts)
        print('Contact successfully changed.')
        return
    elif command =='n':
        command = input('Edit the contact again? (y/n)')
        if command == 'y':
            return (update_contact(name))
    else: 
        print('Change canceled.')
        return
    #wenn nicht bestätigt, erneut fragen was geändert werden soll

def print_all_contacts():
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
    if not name_exists(name):
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
            return print_all_contacts()
        case 'e':
            return update_contact()
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
        print(' c - create new contact\n r - read your contacts\n e - edit a contact\n d - delete a contact\n x - close program')
        user_command = input('Enter here: ')
        get_choice(user_command)
    return

start()
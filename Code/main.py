from classes import *
import sort

address_book = AddressBook()
notebook = Notebook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError as ve:
            return f"ValueError: {str(ve)}"
        except IndexError:
            return "Invalid command format"
        except Exception as e:
            return f"Error: {str(e)}"
    return wrapper


def hello():
    return "Welcome to Your Address Book!\nType 'help' to see available commands and instructions."


def help():
    return """Please enter the command in accordance with the described capabilities (left column), for the specified type (right column).\n
    Here are some things you can do:\n
        'add                                                    - Add a new contact with an optional birthday.
        'add <name_contact> <another_phone>'                    - Add an additional phone number to an existing contact.
        'birthday add <name_contact> <new_birthday_date>'       - Add or update the birthday of an existing contact.
        'change phone <name_contact> <old_phone> <new_phone>'   - Change an existing phone number of a contact.
        'search'                                                - Search for contacts by name or phone number that match the entered string.
        'when <name_contact>'                                   - Show the number of days until the birthday for a contact.
        'finde phone <name_contact>'                            - Show all phone numbers for a contact.
        'show all'                                              - Display all contacts.
        'remove <name_contact> <phone_number>'                  - Remove a phone number from an existing contact.
        'delete <name_contact>'                                 - Delete an entire contact.
        'save'                                                  - Save the address book to a file.
        'load'                                                  - Load the address book from a file.
        'clear all'                                             - Clear all contacts.
        'create note'                                           - Create a new note in the Notebook.
        'change title <old_title> <new_title>'                  - Change the title of an existing note.
        'edit note <note_title>'                                - Edit the content of an existing note.
        'delete note <note_title>'                              - Delete an existing note.
        'find notes <query>'                                    - Find notes containing the specified query in the title or body or by author.
        'show all notes'                                        - Display all notes.
        'add tags'                                              - Adds tags to an existing note.
        'exit' or 'close' or 'good bye'                         - Exit the program."""


@input_error
def add_contact_interactive():
    name = input("Enter the contact's name: ").strip()
    record = Record(name)
    added_info = []

    while True:
        phone = input("Enter a phone number (or nothing to finish): ").strip()
        if phone.lower() == '':
            break
        try:
            record.add_phone(phone)
            added_info.append(f"Phone number: {phone}")
        except ValueError as e:
            print(f"Error: {str(e)} Please try again.")

    while True:
        email = input("Enter an email address (or nothing to finish): ").strip()
        if email.lower() == '':
            break
        try:
            record.add_email(email)
            added_info.append(f"Email: {email}")
        except ValueError as e:
            print(f"Error: {str(e)} Please try again.")

    while True:
        address = input("Enter an address (or nothing to finish): ").strip()
        if address.lower() == '':
            break
        try:
            record.add_address(address)
            added_info.append(f"Address: {address}")
        except ValueError as e:
            print(f"Error: {str(e)} Please try again.")

    while True:
        birthday = input("Enter the contact's birthday (or nothing if not available): ").strip()
        if birthday.lower() == '':
            break
        try:
            record.update_birthday(birthday)
            added_info.append(f"Birthday: {birthday}")
            break
        except ValueError as e:
            print(f"Error: {str(e)} Please try again.")

    address_book.add_record(record)

    return f"Contact {name} has been added : \n" + "\n".join(added_info)

@input_error
def change_phone(command):
    parts = command.split(" ")
    if len(parts) == 3:
        name, old_phone, new_phone = parts[0], parts[1], parts[2]
        record = address_book.find(name)
        if record:
            new_phone_field = Phone(new_phone)
            result = record.edit_phone(old_phone, new_phone_field.value)
            return result
        else:
            raise KeyError(f"Contact {name} not found")
    else:
        raise ValueError("Invalid command format. Please enter name old phone and new phone.")

@input_error
def get_phone(command):
    parts = command.split(" ")
    if len(parts) == 1:
        name = parts[0]
        record = address_book.find(name)
        if record:
            phones_info = ', '.join(phone.value for phone in record.phones)
            return f"Phone numbers for {name}: {phones_info}"
        else:
            raise KeyError
    else:
        raise ValueError

@input_error
def show_all_contacts():
    records = address_book.data.values()
    if records:
        result = "All contacts:\n"
        for record in records:
            result += f"{record.name.value}:\n"
            phones_info = ', '.join(phone.value for phone in record.phones)
            if phones_info:
                result += f"  Phone numbers: {phones_info}\n"
            if record.birthday:
                result += f"  Birthday: {record.birthday}\n"
            email_info = ', '.join(email.value for email in record.emails)
            if email_info:
                result += f"  Email: {email_info}\n"
            address_info = ', '.join(address.value for address in record.addresses)
            if address_info:
                result += f"  Address: {address_info}\n"
        return result
    else:
        return "Contact list is empty"


def exit_bot():
    save_to_disk()
    return "Good bye!"

@input_error
def unknown_command():
    return f"Unknown command: Type 'help' for available commands."

@input_error
def save_to_disk():
    filename = input("Enter the filename to save the address book: ").strip()
    address_book.save_to_disk(filename)
    return f"Address book saved to {filename}"

@input_error
def load_from_disk():
    filename = input("Enter the filename to load/create the address book: : ").strip()
    address_book.load_from_disk(filename)
    return f"Address book loaded from {filename}"

@input_error
def search_contacts():
    query = input("Enter part of the name or phone number: ").strip()
    results = address_book.search_contacts(query)

    if results:
        result = f"Search results for '{query}':\n"
        for record in results:
            result += f"{record.name.value}:\n"
            phones_info = ', '.join(phone.value for phone in record.phones)
            if phones_info:
                result += f"  Phone numbers: {phones_info}\n"
            if record.birthday:
                result += f"  Birthday: {record.birthday}\n"
            email_info = ', '.join(email.value for email in record.emails)
            if email_info:
                result += f"  Email: {email_info}\n"
            address_info = ', '.join(address.value for address in record.addresses)
            if address_info:
                result += f"  Address: {address_info}\n"
        return result
    else:
        return(f"No results found for '{query}'.")


@input_error
def when_birthday(command):
    parts = command.split(" ")
    if len(parts) == 1:
        name = parts[0]
        record = address_book.find(name)
        if record:
            return f"Days until birthday for {name}: {record.days_to_birthday()} days."
        else:
            raise KeyError
    else:
        raise ValueError

@input_error
def update_birthday(command):
    parts = command.split(" ")
    if len(parts) == 2:
        name, new_birthday = parts[0], parts[1]
        record = address_book.find(name)
        if record:
            record.update_birthday(new_birthday)
            return f"Birthday for {name} updated to {new_birthday}."
        else:
            raise KeyError(f"Contact {name} not found")
    else:
        raise ValueError("Invalid command format. Please enter old_birthday name new_birthday.")

@input_error
def remove_phone_from_contact(command):
    parts = command.split(" ")
    if len(parts) == 2:
        name, phone = parts[0], parts[1]
        record = address_book.find(name)
        if record:
            result = record.remove_phone(phone)
            return result
        else:
            raise KeyError
    else:
        raise ValueError

def sort_folder(args=None):
    try:
        if args is None:
            raise ValueError("Please specify the source folder.")
        else:
            sort.main(args)
            return("The folder is sorted \N{winking face}")
    except Exception as e:
        print(f"Error: {e}")
        return("\nPlease usage: sort <source_folder>")

@input_error
def delete_contact(command):
    parts = command.split(" ")
    if len(parts) == 1:
        name = parts[0]
        try:
            address_book.delete(name)
            return f"Contact {name} deleted."
        except KeyError:
            return f"Contact {name} not found."
    else:
        raise ValueError("Invalid command format for deleting a contact.")
    
@input_error
def add_email(command):
    parts = command.split(" ")
    if len(parts) == 2:
        name, email = parts[0], parts[1]
        record = address_book.find(name)
        if record:
            email_field = Email(email)
            record.add_email(email_field.value)
            return f"Email {email} added to contact {name}."
        else:
            raise KeyError(f"Contact {name} not found")
    else:
        raise ValueError("Invalid command format. Please enter name and email.")

@input_error
def search_contact_by_birthday(request):
    address = address_book.search_by_birthday(request)
    if len(address) == 0:
        return '\nContacts not find in this range!'
    result = ''
    for i in address:
        phones_info = ', '.join(phone.value for phone in i.phones)
        result += f"{i.name.value}:\n  Phone numbers: {phones_info}\n  Birthday: {i.birthday}\n"
    return result

@input_error
def add_address(command):
    parts = command.split(" ", 1)
    if len(parts) == 2:
        name, address = parts[0], parts[1]
        record = address_book.find(name)
        if record:
            address_field = Address(address)
            record.add_address(address_field.value)
            return f"Address {address} added to contact {name}."
        else:
            raise KeyError(f"Contact {name} not found")
    else:
        raise ValueError("Invalid command format. Please enter name and email.")

@input_error
def remove_email_from_contact():
    name = input("Please enter the contact's name: ").strip()
    email = input("Please enter the email to remove: ").strip()

    record = address_book.find(name)
    if record:
        result = record.remove_email(email)
        return result
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def change_email():
    name = input("Please enter the contact's name: ").strip()
    old_email = input("Please enter the old email: ").strip()
    new_email = input("Please enter the new email: ").strip()

    record = address_book.find(name)
    if record:
        new_email_field = Email(new_email)
        result = record.edit_email(old_email, new_email_field.value)
        return result
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def remove_address_from_contact():
    name = input("Please enter the contact's name: ").strip()
    address = input("Please enter the address to remove: ").strip()

    record = address_book.find(name)
    if record:
        result = record.remove_address(address)
        return result
    else:
        raise KeyError(f"Contact {name} not found")

@input_error
def change_address():
    name = input("Please enter the contact's name: ").strip()
    old_address = input("Please enter the old address: ").strip()
    new_address = input("Please enter the new address: ").strip()

    record = address_book.find(name)
    if record:
        new_address_field = Address(new_address)
        result = record.edit_address(old_address, new_address_field.value)
        return result
    else:
        raise KeyError

@input_error
def create_note():
    author = input("Enter the author's name: ").strip()
    title = input("Enter the note's title: ").strip()
    body = input("Enter the note's body: ").strip()    
    tags = tag_conversion(input("Enter the note's tags: ").strip())
    note = Note(author, title, body, tags)
    notebook.add_note(note)    
    return f"Note '{title}' by {author} has been added."

@input_error
def find_note(command):
    query = command.strip()
    if not query:
        return "Please provide a search query."
    results = notebook.find_notes(query)
    if not results:
        return "No notes found with the given query."
    result = "Found notes:\n"
    for note in results:
        result += f"Author: {note.author.value}\nTitle: {note.title.value}\nNote: {note.body}\n"
    return result

@input_error
def change_note_title(command):
    parts = command.split(" ")
    if len(parts) == 2:
        old_title, new_title = parts[0], parts[1]
        note = notebook.get_note(old_title)
        if note:
            notebook.delete_note(old_title)
            note.title.value = new_title
            notebook.add_note(note)
            return f"Note title changed from '{old_title}' to '{new_title}'."
        else:
            raise KeyError(f"Note '{old_title}' not found")
    else:
        raise ValueError("Invalid command format. Please enter old and new titles for the note.")

@input_error
def edit_note_text(command):
    title = command.strip()
    note = notebook.get_note(title)
    if note:
        print(f"Current note text:\n{note.body}")
        new_body = input("Enter the new note text (or press Enter to keep the current text): ").strip()
        if new_body:
            note.edit_note(new_body)
            return f"Note '{title}' updated."
        else:
            return "Note text not changed."
    else:
        raise KeyError(f"Note '{title}' not found")

@input_error
def remove_note(command):
    title = command.strip()
    note = notebook.get_note(title)
    if note:
        notebook.delete_note(title)
        return f"Note '{title}' deleted."
    else:
        raise KeyError(f"Note '{title}' not found")
    
@input_error
def show_all_notes():
    notes = notebook.data.values()
    if notes:
        result = "All notes:\n"
        for note in notes:
            result += f"Title: {note.title.value}\n"
            result += f"Author: {note.author.value}\n"
            result += f"Created at: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += f"Note: {note.body}\n"
            result += f"Tags: {note.tags}\n\n"
        return result
    else:
        return "No notes found in the address book"

@input_error
def add_tag():
    title = input("Enter the title where you want to add tags: ").strip()

    if title not in notebook.data.keys():
        raise ValueError(f"Note '{title}' not found")

    data_tags = notebook.data[title].tags

    tags = tag_conversion(input("Enter a tags: ").strip())
    tag_list = tags.split(', ')

    unique_tags = ''

    for tag in tag_list:

        if tag not in data_tags:    
            unique_tags += f'{tag}' if tag == tag_list[-1] else f'{tag}, '

    if len(tag) != 0:
        notebook.add_tags(title, unique_tags)

    return 'tags added'


def tag_conversion(tags):
        if len(tags) == 0:
            return ''
        tags = re.findall(r'#?\w*\w', tags)

        str_tag = ''
        for tag in tags:
            if tag == tags[-1]:
                str_tag += f'{tag}' if tag[0] == '#' else f'#{tag}'

            else:
                str_tag += f'{tag}, ' if tag[0] == '#' else f'#{tag}, '

        return str_tag

commands = {
    "hello": hello,
    "help": help,
    "add contact": add_contact_interactive,
    #"add phone": ,
    "add email": add_email,
    "add adres": add_address,
    "change phone": change_phone,
    "change birthday": update_birthday,
    #"change name": ,
    "change email": change_email,
    "change address": change_address,
    "remove phone": remove_phone_from_contact,
    "remove email": remove_email_from_contact,
    "remove address": remove_address_from_contact,
    "clear all": address_book.clear_all_contacts,
    "by birthday": search_contact_by_birthday,
    "day to birthday": when_birthday,
    "delete contact": delete_contact,
    "search": search_contacts,
    "finde phone": get_phone,
    "show all contacts": show_all_contacts,
    "good bye": exit_bot,
    "close": exit_bot,
    "exit": exit_bot,
    ".": exit_bot,

    "sort": sort_folder, 
    "save": save_to_disk,
    "load": load_from_disk,

    "create note": create_note,
    "change title": change_note_title,
    'add tags': add_tag,
    "edit note": edit_note_text,
    "delete note": remove_note,
    "find note": find_note,
    "show all notes": show_all_notes
}

def choice_action(data, commands):
    for command in commands:
        if data.startswith(command):
            args = data[len(command):].strip()
            return commands[command], args if args else None
    return unknown_command, None

def main():
    while True:
        data = input("\nEnter command: ").lower().strip()
        func, args = choice_action(data, commands)
        result = func(args) if args else func()
        print(result)
        if result == "Good bye!":
            break

if __name__ == "__main__":
    load_from_disk()
    main()
    
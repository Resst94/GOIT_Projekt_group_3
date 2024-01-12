from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer
from classes import *
import sort
address_book = AddressBook()

#Completer for commands in terminal:
sql_completer = WordCompleter([
    'add', 'birthday', 'change phone', 'search', 'when', 'finde',
    'show all', 'remove', 'delete', 'save', 'load', 'exit', 
    'close', 'good bye', 'clear all'], ignore_case=True)


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
        'add <name_contact> <phone> <birthday>'               - Add a new contact with an optional birthday.
        'add <name_contact> <another_phone>'                  - Add an additional phone number to an existing contact.
        'birthday <name_contact> <new_birthday_date>'         - Add or update the birthday of an existing contact.
        'change phone <name_contact> <old_phone> <new_phone>' - Change an existing phone number of a contact.
        'search'                                              - Search for contacts by name or phone number that match the entered string.
        'when <name_contact>'                                 - Show the number of days until the birthday for a contact.
        'finde <name_contact>'                                - Show all phone numbers for a contact.
        'show all'                                            - Display all contacts.
        'remove <name_contact> <phone_number>'                - Remove a phone number from an existing contact.
        'delete <name_contact>'                               - Delete an entire contact.
        'save'                                                - Save the address book to a file.
        'load'                                                - Load the address book from a file.
        'exit' or 'close' or 'good bye'                       - Exit the program.
        'clear all'                                           - Clear all contacts."""

@input_error
def add_contact(command):
    parts = command.split(" ")
    if len(parts) >= 2:
        name, phone = parts[0], parts[1]
        name_field = Name(name)
        phone_field = Phone(phone)
        record = Record(name=name_field.value)
       

        if len(parts) >= 3:
            birthday = ' '.join(parts[2:])
            birthday_field = Birthday(birthday)
            record.birthday = birthday_field

        record.add_phone(phone_field.value)
        address_book.add_record(record)

        if record.birthday:
            result = f"Contact {name} with number {phone} and birthday {record.birthday} saved."
        else:
            result = f"Contact {name} with number {phone} saved."

        return result
    else:
        raise ValueError("Invalid command format. Please enter name and phone.")

@input_error
def change_contact(command):
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
def display_contacts_pagination(records, items_per_page=3):
    total_pages = (len(records) + items_per_page - 1) // items_per_page

    page = 1
    while True:
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        current_records = records[start_index:end_index]

        if not current_records:
            print("Contact list is empty")
            break

        result = f"Page {page}/{total_pages}:\n"
        for record in current_records:
            phones_info = ', '.join(phone.value for phone in record.phones)
            result += f"{record.name.value}:\n  Phone numbers: {phones_info}\n  Birthday: {record.birthday}\n"

        print(result)

        user_input = input("Type 'next' to view the next page, 'prev' for the previous page, or 'exit' to quit: ").strip().lower()

        if user_input == 'next' and page < total_pages:
            page += 1
        elif user_input == 'prev' and page > 1:
            page -= 1
        elif user_input == 'exit':
            break
        else:
            print("Invalid command. Please enter 'next', 'prev', or 'exit'.")

    return "Showing contacts completed."

@input_error
def show_all_contacts():
    records = address_book.data.values()
    if records:
        result = "All contacts:\n"
        for record in records:
            phones_info = ', '.join(phone.value for phone in record.phones)
            result += f"{record.name.value}:\n  Phone numbers: {phones_info}\n  Birthday: {record.birthday}\n"
        return result
    else:
        return "Contact list is empty"

def exit_bot():
    return "Good bye!"

@input_error
def unknown_command(command):
    return f"Unknown command: {command}. Type 'help' for available commands."

@input_error
def save_to_disk(filename):
    address_book.save_to_disk(filename)
    return f"Address book saved to {filename}"

@input_error
def load_from_disk(filename):
    address_book.load_from_disk(filename)
    return f"Address book loaded from {filename}"

@input_error
def search_contacts():
    query = input("Enter the search query: ").strip()
    results = address_book.search_contacts(query)

    if results:
        print(f"Search results for '{query}':")
        for result in results:
            phones_info = ', '.join(phone.value for phone in result.phones)
            birthday_info = result.birthday if result.birthday else "None"
            print(f"Contact name: {result.name.value}\n  Phones: {phones_info}\n  Birthday: {birthday_info}")
    else:
        print(f"No results found for '{query}'.")

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
    if args is None:
        print("Please specify the source folder.")
    else:
        sort.main(args)

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


commands = {
    "sort": sort_folder,    
    "help": help,
    "hello": hello,
    "add": add_contact,
    "change phone": change_contact,
    "finde": get_phone,
    "when": when_birthday,
    "birthday ": update_birthday,
    "remove": remove_phone_from_contact,
    "delete": delete_contact,
    "show all": show_all_contacts,
    "save": save_to_disk,
    "load": load_from_disk,
    "search": search_contacts,
    "clear all": address_book.clear_all_contacts,
    "good bye": exit_bot,
    "close": exit_bot,
    "exit": exit_bot,
    ".": exit_bot,
}

def choice_action(data, commands):
    for command in commands:
        if data.startswith(command):
            args = data[len(command):].strip()
            return commands[command], args if args else None
    return unknown_command, None

def main():
    filename = input("Enter the filename to load/create the address book: : ").strip()
    load_from_disk(filename)
    session = PromptSession(
        lexer=PygmentsLexer(SqlLexer), completer=sql_completer)

    while True:
        try:
            data = session.prompt("\nEnter command: ").lower().strip()
            func, args = choice_action(data, commands)
            result = func(args) if args else func()
            print(result)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        if result == "Good bye!":
            save_to_disk(filename)
            break
     
if __name__ == "__main__":
    main()

from classes import *
import sort
address_book = AddressBook()

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
        'exit' or 'close' or 'good bye'                         - Exit the program.
        'clear all'                                             - Clear all contacts."""


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
    save_to_disk()
    return "Good bye!"

@input_error
def unknown_command(command):
    return f"Unknown command: {command}. Type 'help' for available commands."

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
def add_address(command):
    parts = command.split(" ")
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


commands = {
    "add contact": add_contact_interactive,
    "add email": add_email,
    "sort": sort_folder,    
    "help": help,
    "hello": hello,
    "change phone": change_contact,
    "delete": delete_contact,
    "load": load_from_disk,
    "remove phone": remove_phone_from_contact,
    "clear all": address_book.clear_all_contacts,
    "good bye": exit_bot,
    "close": exit_bot,
    "exit": exit_bot,
    ".": exit_bot,


    "show all": show_all_contacts, ##  ????????? ##
    "save": save_to_disk, ##  ????????? ##


    "add adres": add_address,
    "finde phone": get_phone,
    "when birthday": when_birthday,
    "birthday add": update_birthday,
    "search": search_contacts,
    
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

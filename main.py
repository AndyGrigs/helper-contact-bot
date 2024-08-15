# from bot.models import AddressBook
import time
from pick import pick
from bot.models import AddressBook
from bot.utils import load_data, save_data
from bot.handlers import add_contact, edit_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays


def parse_input(user_input):
    return user_input.strip().split()



def select_contact_name(book):
    """Helper function to select a contact name from the AddressBook."""
    names = list(book.keys())
    if not names:
        print("No contacts available.")
        return None
    title = "Please select a contact:"
    name, _ = pick(names, title, indicator='=>')
    return name

def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        # Define the list of commands and their descriptions
        commands = [
            ("Add Contact", "add"),
            ("Edit Contact", "edit"),
            ("Change Contact", "change"),
            ("Show Phone", "phone"),
            ("Show All", "all"),
            ("Add Birthday", "add-birthday"),
            ("Show Birthday", "show-birthday"),
            ("Upcoming Birthdays", "birthdays"),
            ("Close", "close"),
            ("Exit", "exit")
        ]

        # Display the dropdown menu and get the user's choice
        title = "Please choose a command:"
        command_description, _ = pick([cmd[0] for cmd in commands], title, indicator='=>')

        # Map the selected command description to the command keyword
        command_keyword = next(cmd[1] for cmd in commands if cmd[0] == command_description)

        if command_keyword in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command_keyword == "hello":
            print("How can I help you?")

        elif command_keyword == "add":
            name = input("Enter the contact name: ").strip()
            phone = input("Enter the phone number: ").strip()
            birthday = input("Enter the birthday (DD.MM.YYYY): ").strip()
            message = add_contact([name, phone, birthday], book)
            print(message)

        elif command_keyword == "edit":
            field_options = ['Phone', 'Email', 'Address']
            field, _ = pick(field_options, "Select the field to edit:", indicator='=>')
            
            name = select_contact_name(book)
            if not name:
                continue

            new_value = input(f"Enter the new {field.lower()}: ").strip()
            message = edit_contact([name, field.lower(), new_value], book)
            print(message)

        elif command_keyword == "change":
            name = select_contact_name(book)
            if not name:
                continue

            old_phone = input("Enter the old phone number: ").strip()
            new_phone = input("Enter the new phone number: ").strip()
            message = change_contact([name, old_phone, new_phone], book)
            print(message)

        elif command_keyword == "phone":
            name = select_contact_name(book)
            if not name:
                continue

            message = show_phone([name], book)
            print(message)

        elif command_keyword == "all":
            message = show_all([], book)
            print(message)
            time.sleep(5)  # Delay for 5 seconds to allow users to read the output

        elif command_keyword == "add-birthday":
            name = select_contact_name(book)
            if not name:
                continue

            birthday = input("Enter the birthday (DD.MM.YYYY): ").strip()
            message = add_birthday([name, birthday], book)
            print(message)

        elif command_keyword == "show-birthday":
            name = select_contact_name(book)
            if not name:
                continue

            message = show_birthday([name], book)
            print(message)

        elif command_keyword == "birthdays":
            message = birthdays([], book)
            print(message)

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
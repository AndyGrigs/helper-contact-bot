import os
from bot.models import AddressBook
import time
from pick import pick
from bot.models import AddressBook
from bot.utils import load_data, save_data
from bot.handlers import add_contact, edit_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays


def parse_input(user_input):
    return user_input.strip().split()



# def select_contact_name(book):
#     """Helper function to select a contact name from the AddressBook."""
#     names = list(book.keys())
#     if not names:
#         print("No contacts available.")
#         return None
#     title = "Please select a contact:"
#     name, _ = pick(names, title, indicator='=>')
#     return name
def select_contact_name(book):
    """Helper function to select a contact name from the AddressBook."""
    names = list(book.keys())
    if not names:
        print("No contacts available.")
        return None
    print("Please select a contact:")
    for idx, name in enumerate(names, 1):
        print(f"{idx}. {name}")
    choice = input("Enter the number of the contact: ").strip()
    try:
        index = int(choice) - 1
        if 0 <= index < len(names):
            return names[index]
        else:
            print("Invalid choice.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

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
        print("Please choose a command:")
        print(" ")
        for idx, (desc, _) in enumerate(commands, 1):
            print(f"{idx}. {desc}")
        
        choice = input("Enter the number of the command: ").strip()
        try:
            command_index = int(choice) - 1
            if 0 <= command_index < len(commands):
                command_description, command_keyword = commands[command_index]
            else:
                print("Invalid choice.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        # Display the dropdown menu and get the user's choice
        # title = "Please choose a command:"
        # command_description, _ = pick([cmd[0] for cmd in commands], title, indicator='=>')

        # # Map the selected command description to the command keyword
        # command_keyword = next(cmd[1] for cmd in commands if cmd[0] == command_description)

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
            email = input("Enter the email: ").strip()
            address = input("Enter the address: ").strip()
            message = add_contact([name, phone, birthday, email, address], book)
            print(message)

        elif command_keyword == "edit":
            field_options = ['Phone', 'Email', 'Address']
            
            # Display field options
            print("Select the field to edit:")
            for idx, field in enumerate(field_options, 1):
                print(f"{idx}. {field}")
            
            # Get user input for field selection
            choice = input("Enter the number of the field: ").strip()
            try:
                field_index = int(choice) - 1
                if 0 <= field_index < len(field_options):
                    field = field_options[field_index].lower()
                else:
                    print("Invalid choice.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            
            name = select_contact_name(book)
            if not name:
                continue

            new_value = input(f"Enter the new {field}: ").strip()
            message = edit_contact([name, field, new_value], book)
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



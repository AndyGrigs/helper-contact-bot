from bot.handlers import add_note, remove_note, add_tag_to_note, remove_tag_from_note, AddressBook
from bot.models import Record

def main():
    book = AddressBook()

    # Example records for demonstration; in a real application, these might come from file or database
    book.add_record(Record("Alice"))
    book.add_record(Record("Bob"))

    print("Welcome to the assistant bot!")
    while True:
        print("\nPlease choose a command:")
        print("1. Add Contact")
        print("2. Edit Contact")
        print("3. Change Contact")
        print("4. Show Phone")
        print("5. Show All")
        print("6. Delete Contact")
        print("7. Add Birthday")
        print("8. Show Birthday")
        print("9. Upcoming Birthdays")
        print("10. Add Note")
        print("11. Remove Note")
        print("12. Add Tag to Note")
        print("13. Remove Tag from Note")
        print("14. Close")
        print("15. Exit")

        choice = input("Enter the number of the command: ")

        if choice == '10':
            name = input("Enter contact name: ")
            note_text = input("Enter note text: ")
            print(add_note((name, note_text), book))
        elif choice == '11':
            name = input("Enter contact name: ")
            note_index = input("Enter note index: ")
            print(remove_note((name, note_index), book))
        elif choice == '12':
            name = input("Enter contact name: ")
            note_index = input("Enter note index: ")
            tag_name = input("Enter tag name: ")
            print(add_tag_to_note((name, note_index, tag_name), book))
        elif choice == '13':
            name = input("Enter contact name: ")
            note_index = input("Enter note index: ")
            tag_name = input("Enter tag name: ")
            print(remove_tag_from_note((name, note_index, tag_name), book))
        elif choice == '14':
            break
        elif choice == '15':
            exit()
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
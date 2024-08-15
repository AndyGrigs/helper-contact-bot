from pick import pick
from .models import AddressBook, Record

def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return f"Error: {e}"
    return wrapper


# def add_contact(args, book: AddressBook):
#     names, phone_number, birthday = args
#     name_str = " ".join(names)
    
#     book.add_contact_to(name_str.strip(), phone_number, birthday)
#     print(name_str)
#     return "Contact added."

@input_error
def add_contact(args, book: AddressBook):
    # args should be a list with name, phone, and birthday
    name, phone, birthday, email = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."

    if phone:
        record.add_phone(phone)
    if birthday:
        record.add_birthday(birthday)

    return message


@input_error
def edit_contact(args, book: AddressBook):
    # Display the menu of fields to edit using pick
    title = 'Please choose the field you want to edit:'
    options = ['Phone', 'Email', 'Address']
    
    # Use pick to get the user's selection
    field, index = pick(options, title, indicator='=>')

    # Map the field to a standardized name
    field_map = {
        'Phone': 'phone',
        'Email': 'email',
        'Address': 'address'
    }

    field_name = field_map[field]
    print(f"Attempting to edit contact: {field_name}")

    # Prompt for the contact name
    name = input("Enter the contact name: ").strip()

    # Find the contact
    record = book.find(name)
    if record is None:
        return "Contact not found."

    if field_name == "phone":
        # Prompt for old phone number and validate
        old_value = input("Enter the current phone number to replace: ").strip()
        if record.find_phone(old_value) is None:
            return "Old phone number not found."
        new_value = input("Enter the new phone number: ").strip()
        try:
            record.edit_phone(old_value, new_value)
        except ValueError as e:
            return f"Error: {e}"
        return "Phone number updated."

    elif field_name == "email":
        # Prompt for new email
        new_value = input("Enter the new email: ").strip()
        try:
            record.add_email(new_value)
        except ValueError as e:
            return f"Error: {e}"
        return "Email updated."

    elif field_name == "address":
        # Prompt for new address
        new_value = input("Enter the new address: ").strip()
        record.add_address(new_value)
        return "Address updated."

    else:
        return "Invalid field. Available fields are: phone, email, address."


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Phone number updated."

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    phones = "; ".join(str(phone) for phone in record.phones)
    return f"Phones for {name}: {phones}"

@input_error
def show_all(args, book: AddressBook):
    if not book:
        return "Address book is empty."

    result = []
    for name, record in book.items():
        phones = "; ".join(str(phone) for phone in record.phones)
        birthday = f"Birthday: {record.birthday.date.strftime('%d.%m.%Y')}" if record.birthday else "Birthday: Not set"
        address = f"Address: {record.address}" if record.address else "Address: Not set"
        email = f"Email: {record.email}" if record.email else "Email: Not set"
        result.append(f"{name}:\n  Phones: {phones}\n  {birthday}\n  {address}\n  {email}")

    return "\n".join(result)

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None or not record.birthday:
        return "Birthday not found."
    return f"Birthday for {name}: {record.birthday.date.strftime('%d.%m.%Y')}"

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays(7)
    if not upcoming_birthdays:
        return "No birthdays in the upcoming week."
    return "\n".join(f"{entry['name']}: {entry['congratulation_date']}" for entry in upcoming_birthdays)
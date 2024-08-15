from pick import pick
from .models import AddressBook, Record

def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return f"Error: {e}"
    return wrapper

@input_error
def add_note(args, book: AddressBook):
    name, note_text = args
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' does not exist."
    
    record.add_note(note_text)
    return f"Note added to '{name}'."


@input_error
def remove_note(args, book: AddressBook):
    name, note_index = args
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' does not exist."
    
    try:
        del record.notes[int(note_index)]
        return f"Note {note_index} removed from '{name}'."
    except IndexError:
        return f"Note index {note_index} out of range for '{name}'."

@input_error
def add_tag_to_note(args, book: AddressBook):
    name, note_index, tag_name = args
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' does not exist."
    
    try:
        record.add_tag_to_note(int(note_index), tag_name)
        return f"Tag '{tag_name}' added to note {note_index} of '{name}'."
    except IndexError:
        return f"Note index {note_index} out of range for '{name}'."

@input_error
def remove_tag_from_note(args, book: AddressBook):
    name, note_index, tag_name = args
    record = book.find(name)
    if record is None:
        return f"Contact '{name}' does not exist."
    
    try:
        record.remove_tag_from_note(int(note_index), tag_name)
        return f"Tag '{tag_name}' removed from note {note_index} of '{name}'."
    except IndexError:
        return f"Note index {note_index} out of range for '{name}'."

# def add_contact(args, book: AddressBook):
#     names, phone_number, birthday = args
#     name_str = " ".join(names)
    
#     book.add_contact_to(name_str.strip(), phone_number, birthday)
#     print(name_str)
#     return "Contact added."

@input_error
def add_contact(args, book: AddressBook):
    # args should be a list with name, phone, and birthday
    name, phone, birthday, email, address = args
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

    if email:
        record.add_email(email)

    if address:
        record.add_address(address)

    return message


@input_error
def edit_contact(args, book: AddressBook):


    if len(args) != 3:
        raise ValueError("Incorrect number of arguments. Expected [contact_name, field_name, new_value].")

    contact_name, field_name, new_value = args

    # Validate contact existence
    if contact_name not in book:
        raise KeyError(f"Contact '{contact_name}' does not exist.")

    # Validate field name
    field_name = field_name.lower()
    if field_name not in ['phone', 'email', 'address']:
        raise ValueError("Invalid field. Valid fields are: phone, email, address.")

    # Update the contact field
    contact = book[contact_name]
    if field_name == 'phone':
        contact.phone = new_value
    elif field_name == 'email':
        contact.email = new_value
    elif field_name == 'address':
        contact.address = new_value

    return f"Contact '{contact_name}' has been updated."

@input_error
def delete_contact(args, book: AddressBook):
    name = args[0]
    if name not in book:
        return f"Contact '{name}' does not exist."
    
    del book[name]
    return f"Contact '{name}' has been removed."

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
    if not args:
        return "No contact name provided."

    name = args[0].strip()
    record = book.find(name)
    
    if record is None:
        return "Contact not found."
    
    if not record.phones:
        return f"{name} has no phone numbers listed."
    
    phones = "; ".join(str(phone) for phone in record.phones)
    return f"\nPhones for {name}: {phones}"


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
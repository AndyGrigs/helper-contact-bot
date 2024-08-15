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
def add_contact(book: AddressBook):
    name = input("Enter the name of the contact: ").strip()
    phone = input("Enter the phone number of the contact: ").strip()
    birthday = input("Enter the birthday of the contact (DD.MM.YYYY) or press Enter to skip: ").strip()

    # Create or update the contact record
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        try:
            record.add_phone(phone)
        except ValueError as e:
            return f"Error: {e}"
    
    if birthday:
        try:
            record.add_birthday(birthday)
        except ValueError as e:
            return f"Error: {e}"

    return message


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
        result.append(f"{name}:\n Phones: {phones}\n {birthday}")
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
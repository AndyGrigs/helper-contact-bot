import re
from collections import UserDict
from datetime import timedelta, datetime, date

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Email(Field):
    def validate(self):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, self.value):
            raise ValueError('Invalid email format.')

class Name(Field):
    pass

class Phone(Field):
    def validate(self):
        pattern = r'^\d{10}$'
        if not re.match(pattern, self.value):
            raise ValueError('Invalid phone number format. Must be 10 digits.')

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')
        
class Tag(Field):
    def __init__(self, tag_name):
        self.tag_name = tag_name

    def __str__(self):
        return self.tag_name

class Note(Field):
    def __init__(self, note_text):
        self.note_text = note_text
        self.tags = []

    def add_tag(self, tag):
        if isinstance(tag, Tag):
            self.tags.append(tag)
        else:
            raise TypeError("Tag must be an instance of the Tag class.")

    def remove_tag(self, tag_name):
        for tag in self.tags:
            if tag.tag_name == tag_name:
                self.tags.remove(tag)
                break

    def __str__(self):
        tags_str = ", ".join([str(tag) for tag in self.tags])
        return f"Note: {self.note_text}. Tags: {tags_str}"
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None
        self.notes= []

    def add_note(self, note_text):
        note = Note(note_text)
        self.notes.append(note)

    def add_tag_to_note(self, note_index, tag_name):
        if 0 <= note_index < len(self.notes):
            note = self.notes[note_index]
            tag = Tag(tag_name)
            note.add_tag(tag)
        else:
            raise IndexError("Note index out of range.")
        
    def remove_tag_from_note(self, note_index, tag_name):
        if 0 <= note_index < len(self.notes):
            note = self.notes[note_index]
            note.remove_tag(tag_name)
        else:
            raise IndexError("Note index out of range.")

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        phone_obj.validate()  
        self.phones.append(phone_obj)

    def remove_phone(self, phone_value):
        for phone in self.phones:
            if phone.value == phone_value:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_phone_value, new_phone_value):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone_value:
                phone_obj = Phone(new_phone_value)
                phone_obj.validate()
                self.phones[i] = phone_obj
                break

    def find_phone(self, phone_value):
        for phone in self.phones:
            if phone.value == phone_value:
                return phone
        return None
    
    def add_birthday(self, birthday_date):
        self.birthday = Birthday(birthday_date)

    def add_address(self, address):
        self.address = address

    def add_email(self, email):
        email_obj = Email(email)
        email_obj.validate()
        self.email = email

    def __str__(self):
        phones = "; ".join(str(phone) for phone in self.phones)
        birthday = f"Birthday: {self.birthday.date.strftime('%d.%m.%Y')}" if self.birthday else "Birthday: Not set"
        address = f"Address: {self.address}" if self.address else "Address: Not set"
        email = f"Email: {self.email}" if self.email else "Email: Not set"
        return f"Contact name: {self.name.value}\n  Phones: {phones}\n  {birthday}\n  {address}\n  {email}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.__setitem__(record.name.value, record)

    def find(self, name):
        # Convert search name to lower case for case-insensitive search
        name = name.lower()
        for contact_name, record in self.items():
            if contact_name.lower() == name:
                return record
        return None
    
    def delete(self, name):
        if name in self:
            del self[name]
        else:
            raise KeyError(f"No contact found with the name: {name}")
    
    def get_upcoming_birthdays(self, days=7):
        today = datetime.today().date()
        upcoming_birthdays = []
        one_week_from_today = today + timedelta(days=days)

        for record in self.values():
            birthday = getattr(record, 'birthday', None)
            if birthday is not None:
                birthday_this_year = date(today.year, birthday.date.month, birthday.date.day)
                
                if birthday_this_year < today:
                    birthday_this_year = date(today.year + 1, birthday.date.month, birthday.date.day)
                
                if birthday_this_year <= one_week_from_today:
                    if birthday_this_year.weekday() >= 5:
                        next_monday = birthday_this_year + timedelta(days=(7 - birthday_this_year.weekday()))
                        congratulation_date = next_monday
                    else:
                        congratulation_date = birthday_this_year
                    
                    upcoming_birthdays.append({
                        'name': record.name.value,
                        'congratulation_date': congratulation_date.strftime("%d.%m.%Y")
                    })

        return upcoming_birthdays



# # Example of how to use the AddressBook class
# book = AddressBook()

# # Adding a record to AddressBook
# record = Record("John Doe")
# record.add_phone("1234567890")
# record.add_email("john.doe@example.com")
# record.add_address("123 Elm Street")
# record.add_birthday("01.01.1990")
# book.add_record(record)

# # Checking records in AddressBook
# print("Current contacts in AddressBook:")
# for name, record in book.items():
#     print(record)

# # Find a record
# print("\nFinding a contact:")
# contact = book.find("John Doe")
# print(contact)

# # Update record's phone
# contact.edit_phone("1234567890", "0987654321")

# # Checking records again
# print("\nUpdated contacts in AddressBook:")
# for name, record in book.items():
#     print(record)

# # Get upcoming birthdays
# print("\nUpcoming birthdays:")
# print(book.get_upcoming_birthdays())

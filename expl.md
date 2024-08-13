To refactor the provided code into separate modules, we'll divide it into several Python files based on functionality. Here's a suggested structure:

1. **models.py** - Contains classes defining the data model.
2. **utils.py** - Utility functions like saving and loading data.
3. **handlers.py** - Command handlers for user inputs.
4. **main.py** - Main application logic and entry point.

### models.py
This file will contain all the classes related to the data model.

```python
# models.py

import pickle
from collections import UserDict
from datetime import timedelta, datetime, date

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

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
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.__setitem__(record.name.value, record)

    def find(self, name):
        return self.get(name)

    def delete(self, name):
        del self[name]

    def get_upcoming_birthdays(self, days=7):
        # Implementation remains the same
```

### utils.py
Utility functions for saving and loading data.

```python
# utils.py

import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
```

### handlers.py
Command handlers for user inputs.

```python
# handlers.py

from models import AddressBook, Record
from utils import load_data, save_data

def add_contact(args, book: AddressBook):
    # Implementation remains the same

def change_contact(args, book: AddressBook):
    # Implementation remains the same

def show_phone(args, book: AddressBook):
    # Implementation remains the same

def show_all(args, book: AddressBook):
    # Implementation remains the same

def add_birthday(args, book: AddressBook):
    # Implementation remains the same

def show_birthday(args, book: AddressBook):
    # Implementation remains the same

def birthdays(args, book: AddressBook):
    # Implementation remains the same
```

### main.py
Main application logic and entry point.

```python
# main.py

from models import AddressBook
from utils import load_data, save_data
from handlers import add_contact, change_contact, show_phone, show_all, add_birthday, show_birthday, birthdays

def parse_input(user_input):
    # Implementation remains the same

def main():
    book = load_data(AddressBook())
    # Rest of the main function implementation

if __name__ == "__main__":
    main()
```

This refactoring separates concerns into distinct modules, making the codebase easier to maintain and extend. Each module focuses on a specific aspect of the application, adhering to the Single Responsibility Principle.
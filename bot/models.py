import re
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
            raise ValueError('"Invalid date format. Use DD.MM.YYYY"')
        
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
        pass
        
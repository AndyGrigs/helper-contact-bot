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
        self.address = None
        self.email = None

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
        return self.get(name)

    def delete(self, name):
        del self[name]

    def find(self, name):
        pass
    
    def get(self, contact_id):
        pass

    def delete(self, name):
        del self[name]

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


     
        
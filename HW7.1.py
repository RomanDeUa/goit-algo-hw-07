from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name.value] = record

    def find(self, name):
        return self.records.get(name, None)

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_birthdays = []
        for record in self.records.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= today + timedelta(days=7):
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime('%d.%m.%Y')
                    })
        return upcoming_birthdays

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Insufficient arguments provided."
        except KeyError:
            return "Contact not found."
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Not enough arguments. Usage: add [name] [phone]")
    name, phone = args[0], args[1]
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_phone(args, book: AddressBook):
    if len(args) < 3:
        raise IndexError("Not enough arguments. Usage: change [name] [old_phone] [new_phone]")
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    record.remove_phone(old_phone)
    record.add_phone(new_phone)
    return "Phone number updated."

@input_error
def show_phones(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("Not enough arguments. Usage: phone [name]")
    name = args[0]
    record = book.find(name)
    return ', '.join([phone.value for phone in record.phones])

@input_error
def show_all(args, book: AddressBook):
    return '\n'.join(f"{name}: {', '.join(phone.value for phone in record.phones)}" for name, record in book.records.items())

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Not enough arguments. Usage: add-birthday [name] [birthday]")
    name, birthday = args[0], args[1]
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("Not enough arguments. Usage: show-birthday [name]")
    name = args[0]
    record = book.find(name)
    return record.birthday.value.strftime('%d.%m.%Y') if record.birthday else "No birthday set."

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    return '\n'.join(f"{entry['name']} - {entry['birthday']}" for entry in upcoming_birthdays) if upcoming_birthdays else "No upcoming birthdays."

def parse_input(user_input):
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:] if len(parts) > 1 else []
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

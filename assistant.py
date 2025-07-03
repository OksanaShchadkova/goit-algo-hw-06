# Implementing classes
from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass  # Ім'я є обов'язковим полем, але додаткових дій не потрібно


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be a string of 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return re.match(r'^\d{10}$', value) is not None


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError("Phone number not found.")

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)  # Видаляємо старий номер
        self.add_phone(new_phone)      # Додаємо новий номер

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
#  Integrate with an assistant


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
    return inner


@input_error
def parse_input(user_input: str):
    parts = user_input.strip().split()
    cmd, *args = parts
    return cmd.lower(), args


@input_error
def add_contact(args, address_book):
    name, phone = args  # ValueError буде автоматично, якщо не 2 аргументи
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"Contact '{name}' added with phone number '{phone}'."


@input_error
def change_contact(args, address_book):
    name, phone = args
    record = address_book.find(name)
    if record:
        record.add_phone(phone)  # Додаємо новий телефон
        return f"Contact '{name}' updated with new phone number '{phone}'."
    raise KeyError


@input_error
def show_phone(args, address_book):
    name = args[0]
    record = address_book.find(name)
    if record:
        return str(record)
    raise KeyError


@input_error
def show_all(_, address_book):
    if not address_book:
        return "No contacts available."
    return str(address_book)


def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Available commands: hello, add <username> <phone>, change <username> <phone>, phone <username>, all, exit, close")

    while True:
        user_input = input("Enter a command: ")

        result = parse_input(user_input)
        if isinstance(result, str):
            print(result)
            continue

        command, args = result

        if command in ("exit", "close"):
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
            continue

        handler = {
            "add": add_contact,
            "change": change_contact,
            "phone": show_phone,
            "all": show_all,
        }.get(command, lambda args, address_book: "Invalid command. Please try again.")

        print(handler(args, address_book))


if __name__ == "__main__":
    main()

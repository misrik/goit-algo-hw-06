class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number format")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {', '.join(str(p) for p in self.phones)}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and correct format of phone (10 digits) please."
        except KeyError:
            return "No contact found."
        except IndexError:
            return "Enter username."

    return inner

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Give me name and correct format of phone (10 digits) please.")
    
    name, phone = args
    if name in contacts:
        return "Contact already exists."
    if not phone.isdigit() or len(phone) != 10:
        raise ValueError("Invalid phone number format")
    record = Record(name)
    record.add_phone(phone)
    contacts[name] = record
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        return "Contact not found."
    contacts[name].phones = [Phone(phone)]
    return "Contact updated successfully"

@input_error
def show_contact(args, contacts):
    name, *_ = args
    record = contacts.get(name)
    if record:
        return str(record)
    else:
        return f"No contact found with username {name}"

@input_error
def phone_contact(args, contacts):
    username = args[0]
    record = contacts.get(username)
    if record:
        return f"Calling a phone number for {username}: {record.phones[0]}"
    else:
        return f"No contact found with username {username}"

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts.data))

        elif command == "change":
            print(change_contact(args, contacts.data))

        elif command == "show":
            print(show_contact(args, contacts.data))

        elif command == "all":
            for record in contacts.data.values():
                print(record)

        elif command == "phone":
            print(phone_contact(args, contacts.data))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

#__________________________________________________________________
#!!!Якщо написати боту "exit", то ми побачимо роботу цього коду:
# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

import pickle
import sys

banks = {}

class Client:
    def __init__(self, first_name, last_name, bank):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = f"{first_name} {last_name}"
        self.bank = bank
        self.bank_balance = 0

class Bank:
    def __init__(self, bank):
        self.bank = bank
        self.clients = {}

    def add_client(self, first_name, last_name):
        client = Client(first_name, last_name, self.bank)
        self.clients[client.full_name] = client

    def show_balance(self, full_name):
        print(f"Your current balance is: {self.clients[full_name].bank_balance}")

    def deposit(self, full_name, amount):
        self.clients[full_name].bank_balance += amount

    def transfer(self, full_name, amount, receiver_full_name, receiver_bank):
        self.clients[full_name].bank_balance -= amount
        banks[receiver_bank].clients[receiver_full_name].bank_balance += amount


def is_client(bank, full_name):
    return full_name in banks[bank].clients


def bank_exists(bank):
    return bank in banks


def add_bank(name):
    """ Creates a new bank if it doesn't already exist """
    if not bank_exists(name):
        banks[name] = Bank(name)
    else:
        print("A bank with this name already exists. Bank is not registered")


def add_client(bank, first_name, last_name):
    full_name = f"{first_name} {last_name}"
    if bank_exists(bank):
        if is_client(bank, full_name):
            print(f"A client with the name {full_name} already exists. Client is not registered.")   
        else:
            banks[bank].add_client(first_name, last_name)
    else:
        print(f"There is no bank named {bank} in our system.")


def show_balance(bank, first_name, last_name):
    full_name = f"{first_name} {last_name}"
    if bank_exists(bank):
        if is_client(bank, full_name):
            banks[bank].show_balance(full_name)
        else:
            print(f"Couldn't show the balance because the client with the name {full_name} does not exist.")   
    else:
        print(f"There is no bank named {bank} in our system.")

def deposit(bank, first_name, last_name, amount):
    full_name = f"{first_name} {last_name}"
    if bank_exists(bank):
        if is_client(bank, full_name):
            banks[bank].deposit(full_name, float(amount))
        else:
            print(f"Couldn't deposit the money because the client with the name {full_name} does not exist.")   
    else:
        print(f"There is no bank named {bank} in our system.")

def transfer(bank, first_name, last_name, receiver_bank, receiver_first_name, receiver_last_name, amount):
    full_name = f"{first_name} {last_name}"
    receiver_full_name = f"{receiver_first_name} {receiver_last_name}"
    if bank_exists(bank):
        if is_client(bank, full_name):
            if bank_exists(receiver_bank):
                if is_client(receiver_bank, receiver_full_name):
                    if amount.isnumeric and 0 < float(amount):
                        banks[bank].transfer(full_name, float(amount), receiver_full_name, receiver_bank)
                else:
                    print(f"The recipient {receiver_full_name} does not exist. Money did not transfer.")
            else:
                print(f"Recipient bank {receiver_bank} does not exist. Money did not transfer.")
        else:
            print(f"The client {full_name} does not exist. Money did not transfer.")
    else:
        print(f"The bank {bank} does not exist. Money did not transfer")


def load():
    with open('banks.pickle', 'rb') as b:
        global banks 
        banks = pickle.load(b)


def save():
    geeky_file = open('banks.pickle', 'wb')
    pickle.dump(banks, geeky_file)
    geeky_file.close()

# Add bank command
# add bank bankname

# Add client command
# add client bank client_first_name client_last_name

# Show balance command
# balance bank firstname lastname

# Deposit
# deposit bank firstname lastname amount

# Transfer
# transfer firstname lastname bank receiver_firstname receiver_lastname receiver_bank amount

load()

arguments = len(sys.argv)

if arguments > 2:
    if sys.argv[1] == 'add':
        if sys.argv[2] == 'bank':
            if arguments == 4:
                add_bank(sys.argv[3])
            else:
                print("Invalid number of arguments")
        elif sys.argv[2] == 'client':
            if arguments == 6:
                add_client(sys.argv[3], sys.argv[4], sys.argv[5])
            else:
                print("Invalid number of arguments")
        else:
            print("Invalid argument")

    elif sys.argv[1] == 'balance':
        if arguments == 5:
            show_balance(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Invalid number of arguments")

    elif sys.argv[1] == 'deposit':
        if arguments == 6:
            deposit(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        else:
            print("Invalid number of arguments")

    elif sys.argv[1] == 'transfer':
        if arguments == 9:
            transfer(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
        else:
            print("Invalid number of arguments")

    elif sys.argv[1] == 'show':
        if arguments == 9:
            pass
        else:
            print("Invalid number of arguments")
    else:
        print(f"{sys.argv[1]} is not a valid command")
else:
    print("You did not pass any arguments")

save()

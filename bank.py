import random
import sqlite3
import itertools

db_container = sqlite3.connect('card.s3db')


def check_and_create_db():
    db_cursor = db_container.cursor()
    db_cursor.execute("CREATE TABLE IF NOT EXISTS card("
                      "id INTEGER, "
                      "number TEXT, "
                      "pin TEXT, "
                      "balance INTEGER DEFAULT 0);")


def take_user_command():
    print("1. Create an account\n"
          "2. Log into account\n"
          "0. Exit\n")

    command = input()
    return command


def create_user_account():
    card_number = generate_new_card_number()
    pin_code = generate_new_pin_code()

    db_cursor = db_container.cursor()
    db_cursor.execute("INSERT INTO card(id, number, pin) VALUES " + "("
                      + str(random.randint(0, 999999)) + ", "
                      + str(card_number) + ", "
                      + str(pin_code)
                      + ");")

    db_cursor.execute("COMMIT;")

    print("Your card has been created\n"
          "Your card number:\n" +
          str(card_number) +
          "\nYour card PIN:\n" +
          str(pin_code) + "\n")


def generate_new_card_number():
    db_cursor = db_container.cursor()
    db_cursor.execute("SELECT number FROM card")
    results = db_cursor.fetchall()
    results = [i for i in itertools.chain(*results)]

    bank_identification_number = '400000'

    while True:
        card_template = bank_identification_number + \
                        str(format(random.randint(000000000, 999999999), '09d'))

        number_to_check = [int(digit) for digit in card_template]

        for digit in range(0, len(number_to_check), 2):
            number_to_check[digit] *= 2

        for digit in range(len(number_to_check)):
            if number_to_check[digit] > 9:
                number_to_check[digit] -= 9
        checksum = sum(number_to_check)
        if checksum % 10 == 0:
            appendix = 0
        else:
            appendix = 10 - checksum % 10
        if card_template + str(appendix) in results:
            continue
        else:
            card_number = card_template + str(appendix)
            return card_number


def generate_new_pin_code():
    pin_code = str(format(random.randint(0000, 9999), '04d'))
    return pin_code


def is_luhn_checksum(number_to_check):
    last_number = number_to_check[-1]
    number_to_check = number_to_check[0:-1]

    number_to_check = [int(digit) for digit in number_to_check]

    for digit in range(0, len(number_to_check), 2):
        number_to_check[digit] *= 2

    for digit in range(len(number_to_check)):
        if number_to_check[digit] > 9:
            number_to_check[digit] -= 9

    number_to_check.append(int(last_number))
    return sum(number_to_check) % 10 == 0


def is_account_exist(user_number):
    db_cursor = db_container.cursor()
    db_cursor.execute("SELECT number FROM card")
    results = db_cursor.fetchall()
    results = [i for i in itertools.chain(*results)]
    return user_number in results


def is_pin_correct(user_number, user_pin):
    db_cursor = db_container.cursor()
    db_cursor.execute("SELECT pin FROM card WHERE number = '"
                      + user_number + "';")
    actual_pin = db_cursor.fetchone()
    return user_pin == actual_pin[0]


def processing_logged_user(user_number):
    print("You have successfully logged in!\n")
    current_card = user_number
    while True:
        print("1. Balance\n"
              "2. Add income\n"
              "3. Do transfer\n"
              "4. Close account\n"
              "5. Log out\n"
              "0. Exit\n")
        account_command = input()
        if account_command.isdigit() and account_command == "1":
            balance = fetch_user_balance(current_card)
            print("Balance: " + str(balance) + "\n")

        elif account_command.isdigit() and account_command == "2":
            deposit_amount = request_income()
            if not deposit_amount:
                continue
            else:
                add_income(current_card, deposit_amount)

        elif account_command.isdigit() and account_command == "3":
            process_money_transfer(current_card)

        elif account_command.isdigit() and account_command == "4":
            close_account(current_card)
            break

        elif account_command.isdigit() and account_command == "5":
            print("You have successfully logged out!\n")
            break

        elif account_command.isdigit() and account_command == "0":
            print("Bye!")
            exit(0)


def fetch_user_balance(card_number):
    db_cursor = db_container.cursor()
    db_cursor.execute("SELECT balance FROM card WHERE number = '" + card_number + "';")
    balance = db_cursor.fetchone()[0]
    return balance


def request_income():
    while True:
        deposit_amount = input("Enter income:\n")
        if deposit_amount == "0":
            return False
        elif deposit_amount.isdigit() and int(deposit_amount) > 0:
            return deposit_amount

        else:
            print("Wrong input, try again.\n"
                  "Input 0 for abort.")


def add_income(card_number, deposit_amount):
    db_cursor = db_container.cursor()
    db_cursor.execute("SELECT balance FROM card WHERE number = '"
                      + card_number + "';")
    balance = db_cursor.fetchone()[0]

    balance = str(balance + int(deposit_amount))
    db_cursor.execute("UPDATE card "
                      "SET balance = " + balance +
                      " WHERE number = '" + card_number + "';")
    db_cursor.execute("COMMIT;")
    print("Income was added!\n")


def process_money_transfer(source_card):
    destination_card = input("Transfer\n"
                             "Enter card number:\n")

    if is_luhn_checksum(destination_card):
        if is_account_exist(destination_card) or destination_card == source_card:

            transfer_amount = request_transfer_amount()
            if transfer_amount <= fetch_user_balance(source_card):
                make_transaction(source_card, destination_card, transfer_amount)
            else:
                print("Not enough money!\n")
                return
        else:
            print("Such a card does not exist.")
    else:
        print("Probably you made a mistake in the card number. "
              "Please try again!\n")
        return


def request_transfer_amount():
    transfer_amount = int(input("Enter how much money you want to transfer:"
                                "\n"))
    return transfer_amount


def make_transaction(source_card, destination_card, transfer_amount):
    db_cursor = db_container.cursor()
    db_cursor.execute("SELECT balance FROM card WHERE number = '"
                      + source_card + "';")
    source_balance = db_cursor.fetchone()[0]
    db_cursor.execute("UPDATE card "
                      "SET balance = " + str(source_balance - transfer_amount)
                      + " WHERE number = '" + source_card + "';")

    db_cursor.execute("SELECT balance FROM card WHERE number = '"
                      + destination_card + "';")
    dest_balance = db_cursor.fetchone()[0]
    db_cursor.execute("UPDATE card "
                      "SET balance = " + str(dest_balance + transfer_amount)
                      + " WHERE number = '" + destination_card + "';")
    db_cursor.execute("COMMIT;")
    print("Success!\n")


def close_account(card_number):
    db_cursor = db_container.cursor()
    db_cursor.execute("DELETE FROM card WHERE number = '"
                      + card_number + "';")
    db_cursor.execute("COMMIT;")
    print("The account has been closed!\n")


def main():
    while True:

        command = take_user_command()

        if command.isdigit() and command == "1":
            create_user_account()

        elif command.isdigit() and command == "2":

            user_number = input("Enter your card number:\n")
            user_pin = input("Enter your PIN:\n")

            if is_account_exist(user_number) and (
                    is_pin_correct(user_number, user_pin)
            ):

                processing_logged_user(user_number)

            else:
                print("Wrong card number or PIN!\n")

        elif command.isdigit() and command == "0":
            exit(0)


check_and_create_db()
main()

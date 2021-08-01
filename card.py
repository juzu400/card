import random


class Card:
    
    list_of_digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    IIN = str(400000)
    user_choice = None
    all_cards = []
    
    def __init__(self):
        account_number = "".join(map(str, random.sample(Card.list_of_digits, 9)))
        checksum = str(random.randrange(10))
        self.number = Card.IIN + account_number + checksum
        self.PIN = "".join(map(str, random.sample(Card.list_of_digits, 4)))
        self.balance = 0
    
    def main_menu():
        while True:
            print("""
            1. Create an account
            2. Log into account
            0. Exit
            """)
            Card.user_choice = int(input())
            if Card.user_choice == 1:
                Card.create_card()
            elif Card.user_choice == 2:
                Card.log_in()

            if Card.user_choice == 0:
                print("Bye!")
                break
                
    def create_card():
        card_instance = Card()
        Card.all_cards.append(card_instance)
        print("Your card number:")
        print(card_instance.number)
        print("Your card PIN:")
        print(card_instance.PIN)
    
    def log_in():
        card_number = input("Enter your card number:\n")
        PIN = input("Enter your PIN:\n")
        for card in Card.all_cards:
            if card.number == card_number:
                if card.PIN == PIN:
                    print("You have successfully logged in!")
                    while True:
                        print("""
                        1. Balance
                        2. Log out
                        0. Exit
                        """)
                        Card.user_choice = int(input())
                        if Card.user_choice == 1:
                            print("Balance:", card.balance)
                        elif Card.user_choice == 2:
                            print("You have successfully logged out!")
                            break
                        elif Card.user_choice == 0:
                            break
                else:
                    print("Wrong card number or PIN!")
                    break
        else:
            print("Wrong card number or PIN!")
            
            
Card.main_menu()

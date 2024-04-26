import os
from openai import OpenAI
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

stack_trace = """ File "/home/hub/Desktop/asraf/assistant_api/python-test/main.py", line 26, in <module>
    menu = MenuItem()
TypeError: MenuItem.__init__() missing 5 required positional arguments: 'name', 'water', 'milk', 'coffee', and 'cost'"""


file_1 = '''
# File Path: python-test/coffee_maker.py

class CoffeeMaker:
    """Models the machine that makes the coffee"""
    def __init__(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }

    def report(self):
        """Prints a report of all resources."""
        print(f"Water: {self.resources['water']}ml")
        print(f"Milk: {self.resources['milk']}ml")
        print(f"Coffee: {self.resources['coffee']}g")

    def is_resource_sufficient(self, drink):
        """Returns True when order can be made, False if ingredients are insufficient."""
        can_make = True
        for item in drink.ingredients:
            if drink.ingredients[item] > self.resources[item]:
                print(f"Sorry there is not enough {item}.")
                can_make = False
        return can_make

    def make_coffee(self, order):
        """Deducts the required ingredients from the resources."""
        for item in order.ingredients:
            self.resources[item] -= order.ingredients[item]
        print(f"""
             )))
            (((
          +-----+
          |     |] - Here's your {order.name}. Enjoy! :)
          `-----'
        """)
'''
file_2 = '''
# File Path: python-test/main.py

from menu.menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money.money_machine import MoneyMachine
from time import sleep

def welcome():
    print("""\033[33m
             )))
            (((
          +-----+
          |     |] - WELCOME TO THE COFFEE MACHINE!
          `-----' 
    
          ------ MENU ------ 
          Espresso ($1.50)
          Latte ($2.50)
          Cappuccino ($3.00)
          ------------------
    
          PS: Type "report" at any moment
          to check our resources available.
          Type "off" to log out from the machine.\033[m
        """)


menu = MenuItem()
money_machine = MoneyMachine()
coffee_maker = CoffeeMaker()
is_on = True

while is_on:
    welcome()
    options = menu.get_items()
    user_choice = str(input(f'What would you like?\nOptions ({options}): ')).strip().lower()
    if user_choice == 'off':
        print('\033[31m<<THE END>>\033[m')
        is_on = False
    elif user_choice == 'report':
        coffee_maker.report()
        money_machine.report()
    elif menu.find_drink(user_choice) is None:
        print('\033[31mError. Please choose an available option.\033[m')
    else:
        beverage = menu.find_drink(user_choice)  # Encapsulates the result
        sufficient_resources = coffee_maker.is_resource_sufficient(beverage)  # TrueFalse result
        sufficient_money = money_machine.make_payment(beverage.cost)
        if sufficient_resources and sufficient_money:
            print('Thank you! Allow us to make your beverage now...')
            coffee_maker.make_coffee(beverage)
            sleep(5)
'''
file_3 = '''
# File Path: python-test/menu/menu.py

class MenuItem:
    """Models each Menu Item."""
    def __init__(self, name, water, milk, coffee, cost):
        self.name = name
        self.cost = cost
        self.ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee
        }


class Menu:
    """Models the Menu with drinks."""
    def __init__(self):
        self.menu = [
            MenuItem(name="latte", water=200, milk=150, coffee=24, cost=2.5),
            MenuItem(name="espresso", water=50, milk=0, coffee=18, cost=1.5),
            MenuItem(name="cappuccino", water=250, milk=50, coffee=24, cost=3),
        ]

    def get_items(self):
        """Returns all the names of the available menu items"""
        options = ""
        for item in self.menu:
            options += f"{item.name}/"
        return options

    def find_drink(self, order_name):
        """Searches the menu for a particular drink by name. Returns that item if it exists, otherwise returns None"""
        for item in self.menu:
            if item.name == order_name:
                return item
        print("Sorry that item is not available.")

'''
file_4 = '''
# File Path: python-test/money/money_machine.py

class MoneyMachine:
    CURRENCY = "$"

    COIN_VALUES = {
        "quarters": 0.25,
        "dimes": 0.10,
        "nickles": 0.05,
        "pennies": 0.01
    }

    def __init__(self):
        self.profit = 0
        self.money_received = 0

    def report(self):
        """Prints the current profit"""
        print(f"Money: {self.CURRENCY}{self.profit}")

    def process_coins(self):
        """Returns the total calculated from coins inserted."""
        print("""\033[33m
        We accept the following coins:
        Quarters ($0.25), dimes ($0.10)
        nickles ($0.05), pennies ($0.01)\033[m
        """)
        for coin in self.COIN_VALUES:
            self.money_received += int(input(f"How many {coin}? Please: ")) * self.COIN_VALUES[coin]
        print(f'You have provided: {self.CURRENCY}{self.money_received}')
        return self.money_received

    def make_payment(self, cost):
        """Returns True when payment is accepted, or False if insufficient."""
        self.process_coins()
        if self.money_received >= cost:
            change = round(self.money_received - cost, 2)
            print(f"Here is {self.CURRENCY}{change} in change.")
            self.profit += cost
            self.money_received = 0
            return True
        else:
            print("Sorry that's not enough money. Money refunded.")
            self.money_received = 0
            return False


'''


file_contents = f"{file_1}\n{file_2}\n{file_3}\n{file_4}"

completion = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"Please fix the code as I am getting following error stack trace:\n {stack_trace}. File path is provided in each file first line. Give me output in json. I need two keys, one should have code before changes and another should have code after changes. Before changes and after changes should also include the line no and filepath with filename. strictly follow this output json format. here is my code files with filepaths:{file_contents}"}
  ],
  temperature=0
)

print(completion)

print(completion.choices[0].message)


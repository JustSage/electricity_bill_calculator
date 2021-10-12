from utils.utils import clean_function_name, list_previous_bills
from bills.elec_bill import calculate_my_electric_bill

def menu():
    commands = { 1 : calculate_my_electric_bill, 2 : list_previous_bills}
    print("_______ WELCOME _______")
    print("Function Menu: ")

    while True:
        for key, val in commands.items():
            name = clean_function_name(val)
            print(str(key) + ") " + name)
        print("Enter Q to quit")
        try:
            user_input = input("Enter menu option: ")
            if user_input in ['Q','q']:
                print("Have a good day!")
                exit()
            if int(user_input) in commands.keys():
                print()
                cmd = commands[int(user_input)]
                cmd()

        except ValueError:
            print("Invalid Input")

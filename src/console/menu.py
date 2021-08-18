from utils.utils import clean_function_name
from bills.elec_bill import calculate_my_electric_bill

def menu():
    print("_______ WELCOME _______")
    print("Function Menu: ")
    commands = {"1": calculate_my_electric_bill}

    for key, val in commands.items():
        name = clean_function_name(val)
        print(key + ") " + name)
    user_input = str(input("Enter Number From Menu: "))
    cmd = commands[user_input]
    cmd()



import json
import os
from datetime import datetime
from typing import List,Dict

PATH = os.path.dirname(os.path.realpath(__file__)) + "/data/elec_bills.json"

def clean_function_name(name) -> str:
    """
    @param name: the name of the function to clean.
    @return a cleaned version of the function name.
    example: "clean_function_name" -> "Clean Function Name"
    """
    return " ".join(name.__name__.split("_")).title()

def get_previous_watt_count() -> float:
    """
    @return if the file is empty it returns 0; indicating it's the first bill, otherwise
    it returns the last (previous) watt count from the list of dicitonaries in PATH.
    """
    if not file_is_empty():
        with open(PATH, "r") as file:
            data = json.load(file)
            previous_watt_count = data['bills'][len(data['bills']) - 1]['watts']
            return previous_watt_count
    else:
        print("Data file is empty, initiating...")
        return 0.0

def construct_bill(watts: float, to_pay: float) -> Dict:
    """
    @param watts: the amount of watts in the electricity counter.
    @param to_pay: the sum required to pay.
    @return dictionary containing an electricity bill dictionary.

    initializes date key with today's date and construct a dictionary
    with given params.
    """
    bill = {}
    bill['watts'] = watts
    bill['to_pay'] = to_pay
    bill['date'] = datetime.today().date().strftime("%-d-%B-%Y")
    return bill

def date_exists(bills:List[Dict], date: datetime) -> bool:
    """
    @param bills: a list of dictionaries containing bills.
    @param date: a datetime object.
    @return boolean state indicating if there's an equal date
            to the date param.
    """
    return any(item for item in bills if date == item['date'])

def file_is_empty() -> bool:
    """
    @return boolean state indicating if the file is empty or not.
    """
    return os.path.getsize(PATH) == 0

def init_bill_data(bill:Dict) -> None:
    """
    @param bill: a bill dictionary to initialize list of dictionaries with.
    writes a list of dictionaries to a json file.
    """
    data = {}
    data['bills'] = [bill]
    with open(PATH, "w") as file:
        file.write(json.dumps(data))

def add_bill(bill:Dict) -> bool:
    """
    @param bill: a bill dictionary to add.
    if the file is not empty, the function appends a bill dictionary to a json file;
    otherwise, it will call @init_bill_data to initialize a list of dictionaries with
    the given bill.
    """
    if file_is_empty():
        init_bill_data(bill)
        return True

    with open(PATH, "r+") as file:
        data = json.load(file)
        # check if the date exists before appending.
        if not date_exists(data['bills'], bill['date']):
            data['bills'].append(bill)
            file.seek(0)
            json.dump(data, file)
            return True
        else: # the date exists within the list of dictionaries
            print("Bill already exists... Aborting bill insertion...")
            return False

def list_previous_bills():
    if file_is_empty():
        print("There are no bills to display")
    else:
        with open(PATH, "r") as file:
            data = json.load(file)
            for item in data['bills']:
                print("Bill of " + item['date'])
                for k,v in item.items():
                    if k != 'date':
                        k = " ".join(k.split("_")).title()
                        print(k,":",v)
                print()

import json
import os
from datetime import datetime
from typing import List,Dict

PATH = os.path.dirname(os.path.realpath(__file__)) + "/data/elec_bills.json"

def clean_function_name(name) -> str:
        return " ".join(name.__name__.split("_")).title()

def get_previous_watt_count() -> float:
    if not file_is_empty(PATH):
        with open(PATH, "r") as file:
            data = json.load(file)
            previous_watt_count = data['bills'][len(data['bills']) - 1]['watts']
            return previous_watt_count
    else:
        print("Data file is empty, initiating...")
        return 0.0

def construct_bill(watts: float, to_pay: float) -> Dict:
    bill = {}
    bill['to_pay'] = to_pay
    bill['watts'] = watts
    bill['date'] = datetime.today().date().strftime("%-d-%B-%Y")
    return bill

def date_exists(data:List[Dict], date: datetime) -> bool:
    return any(item for item in data if date == item['date'])

def file_is_empty(file:str) -> bool:
    return os.path.getsize(file) == 0

def init_bill_data(bill:Dict) -> None:
    data = {}
    data['bills'] = [bill]
    with open(PATH, "w") as f:
        f.write(json.dumps(data))

def write_bill(bill:Dict) -> None:
    if file_is_empty(PATH):
        init_bill_data(bill)
        return

    with open(PATH, "r+") as file:
        data = json.load(file)
        if not date_exists(data['bills'], bill['date']):
            data['bills'].append(bill)
            file.seek(0)
            json.dump(data, file)
        else:
            print("Bill already exists... Aborting bill insertion...")
            return

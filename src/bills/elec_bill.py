import concurrent.futures
from concurrent.futures import Future
from bs4 import BeautifulSoup as bs
from utils.utils import get_previous_watt_count,construct_bill, add_bill

import requests

URL = "https://www.iec.co.il/homeclients/pages/tariffs.aspx"

def calculate_my_electric_bill():
    def get_elec_rate(t_url:str) -> Future[float]:
        def worker(url):
            res = requests.get(url)
            soup = bs(res.content, "html.parser")
            rate_tax_included = soup.select(".ms-rteTableEvenCol-6 p")
            return float(str(rate_tax_included.pop().next_element))
        return concurrent.futures.ThreadPoolExecutor().submit(worker, t_url)

    def calculate_bill(curr_month: float, prev_month: float, watt_rate: float) -> float:
        to_calc = curr_month - prev_month
        result = to_calc * (watt_rate / 100)
        return round(result, 2)


    prev_month_watt_count = get_previous_watt_count()
    # Calculating rates
    while True:
        try:
            curr_watt_count = float(input("Insert the WATT amount displayed on the electricity counter: "))
            if prev_month_watt_count >= curr_watt_count:
                print("Watt count can't be equal or lower than previous count")
            else:
                print("Calculating Electricity Bill...")
                break
            
        except ValueError:
            print("Invalid input") 

    watt_rate = get_elec_rate(URL)
    to_pay = calculate_bill(curr_watt_count, prev_month_watt_count, watt_rate.result())
    bill = construct_bill(curr_watt_count, to_pay)
    bill_added = add_bill(bill)
    if bill_added:
        print(f"Upcoming bill: {bill['to_pay']:.2f} ILS")

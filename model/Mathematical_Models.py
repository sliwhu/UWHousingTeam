# importing required packages
import numpy as np
import pandas as pd

# Model for calculating bidding price for a house

hottest = [98004, 98006, 98007, 98008, 98112, 98033, 98034, 98039, 98040,
           98052, 98053, 98074, 98075, 98077, 98103, 98112, 98177, 98115, 98117]
medium_hot = [98001, 98005, 98023, 98027, 98028, 98029, 98056, 98059, 98105,
              98107, 98116, 98118, 98119, 98122, 98125, 98133, 98155, 98199]

def bidding_price(zipcode, list_price):
    if zipcode in hottest:
        add_price = (np.random.randint(12, 18, None, int)/100)*list_price
        bid_price = list_price + add_price
    elif zipcode in medium_hot:
        add_price = (np.random.randint(5, 10, None, int)/100)*list_price
        bid_price = list_price + add_price
    else:
        add_price = (np.random.randint(5, 10, None, int) / 100) * list_price
        bid_price = list_price - add_price

    return bid_price

def monthly_expenses(list_price, mortgage_period, interest_rate, house_type):
    mortgage = list_price/(mortgage_period*12)
    interest = (interest_rate/100)*mortgage

    # the following percentage values are specifically for king county areas
    property_tax = 0.15 * mortgage
    insurance = 0.07 * mortgage
    utilities = 0.15 * mortgage
    services = 0.035 * mortgage
    if house_type in ['condo', 'townhouse']:
        hoa = 0.11 * mortgage
    else:
        hoa = 0.035 * mortgage
    monthly_expenses = mortgage + interest + property_tax + insurance + utilities + services + hoa

    return monthly_expenses

#testing
bid = bidding_price(98053, 650000)
print(bid)

exp = monthly_expenses(700000, 30, 5, 'condo')
print(exp)

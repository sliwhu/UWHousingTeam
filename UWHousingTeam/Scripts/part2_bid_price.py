# importing required packages
'''
How to initiate bokeh server using this file:

type bokeh serve --port 5002 widgets_part2.py in your terminal
Then you may go to the FirstStop landing page to click the bidding price link

'''


from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models.widgets import Button, TextInput, Paragraph, Div
import numpy as np

LOGO = Div(text="""<img src="https://s3-us-west-2.amazonaws.com/data515logo/logo_title_thinner.PNG"
alt="" />""")

# Create Input Controls
LISTPRICE = TextInput(title="enter list price/predict price here ($)")
ZIPCODE = TextInput(title="enter zipcode here")

BUTTON_1 = Button(label="Submit")
BUTTON_2 = Button(label="Reset")
OUTPUT = Paragraph(width=600, height=300) #or use pretext, for a <pre> tag in html

HOTTEST = [98004, 98006, 98007, 98008, 98112, 98033, 98034, 98039, 98040,
           98052, 98053, 98074, 98075, 98077, 98103, 98112, 98177, 98115, 98117]
MEDIUM_HOT = [98001, 98005, 98023, 98027, 98028, 98029, 98056, 98059, 98105,
              98107, 98116, 98118, 98119, 98122, 98125, 98133, 98155, 98199]

def bidding_price(zipcode, list_price):
    """
    This function implements a mathematical model to calculate bidding price of a house
    :param zipcode: Zipcode of house entered by user
    :param list_price: List price of house entered by user
    :return: returns the estimated bidding price
    """
    if zipcode in HOTTEST:
        add_price = (np.random.randint(12, 18, None, int)/100)*list_price
        bid_price = list_price + add_price
    elif zipcode in MEDIUM_HOT:
        add_price = (np.random.randint(5, 10, None, int)/100)*list_price
        bid_price = list_price + add_price
    else:
        add_price = (np.random.randint(5, 10, None, int) / 100) * list_price
        bid_price = list_price - add_price

    return bid_price

def submit():
    """
    these are made up coefficients for now
    """
    value = bidding_price(float(ZIPCODE.value), float(LISTPRICE.value))
    OUTPUT.text = 'Your suggested bidding price is: ' + str(int(value)) + ' $'

def reset():
    """
    This function resets the output
    """
    OUTPUT.text = None

BUTTON_1.on_click(submit)
BUTTON_2.on_click(reset)

LAY_OUT = layout(children=[[LOGO], [LISTPRICE, ZIPCODE], [BUTTON_1], [BUTTON_2], [OUTPUT]],
                 sizing_mode='fixed')
curdoc().add_root(LAY_OUT)
curdoc().title = "Predict the bidding price of your first home"

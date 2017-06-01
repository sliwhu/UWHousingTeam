# importing required packages
'''
How to initiate bokeh server using this file:

type bokeh serve --port 5002 widgets_part2.py in your terminal
Then you may go to the FirstStop landing page to click the bidding price link

'''


from bokeh.io import curdoc, output_file, show, reset_output
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import Button, TextInput, RadioButtonGroup, Select, Slider, Paragraph
import numpy as np
import pandas as pd

Logo = Div(text="""<img src="https://s3-us-west-2.amazonaws.com/data515logo/logo_title_thinner.PNG" alt="" />""")

# Create Input Controls 
listprice = TextInput(title="enter list price/predict price here ($)")
zipcode = TextInput(title="enter zipcode here")

button_1 = Button(label="Submit")
button_2 = Button(label="Reset")
output = Paragraph(width=600, height=300) #or use pretext, for a <pre> tag in html

hottest = [98004, 98006, 98007, 98008, 98112, 98033, 98034, 98039, 98040, 98052, 98053, 98074, 98075, 98077, 98103, 98112, 98177, 98115, 98117]
medium_hot = [98001, 98005, 98023, 98027, 98028, 98029, 98056, 98059, 98105, 98107, 98116, 98118, 98119, 98122, 98125, 98133, 98155, 98199]

def bidding_price(zipcode,list_price):
    if zipcode in hottest:
        add_price=(np.random.randint(12, 18, None, int)/100)*list_price
        bid_price = list_price + add_price
    elif zipcode in medium_hot:
        add_price=(np.random.randint(5, 10, None, int)/100)*list_price
        bid_price = list_price + add_price
    else:
        add_price = (np.random.randint(5, 10, None, int) / 100) * list_price
        bid_price = list_price - add_price

    return bid_price

def submit():
    #these are made up coefficients for now
    value = bidding_price(float(zipcode.value), float(listprice.value))
    output.text = 'Your suggested bidding price is: ' + str(int(value)) + ' $'
    
def reset():
    #reset_output()
    output.text = None

button_1.on_click(submit)

button_2.on_click(reset)

#lay_out = layout([[select1, select2, select3, select4], [button_1, button_2], [output]])
lay_out = layout(
            children=[
            [listprice, zipcode],
            [button_1],
            [button_2],
            [output]
            ],
            sizing_mode='fixed',
            )
curdoc().add_root(lay_out)
curdoc().title = "Predict the bidding price of your first home"



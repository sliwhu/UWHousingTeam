# importing required packages
'''
How to use this file:

How to initiate bokeh server using this file:

type bokeh serve --port 5003 widgets_part3.py in your terminal
Then you may go to the FirstStop landing page to click the calculating monthly cost link


'''

from bokeh.io import curdoc, output_file, show, reset_output
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import Button, TextInput, RadioButtonGroup, Select, Slider, Paragraph
import numpy as np
import pandas as pd


# Create Input Controls 
listprice = TextInput(title="enter list price/predict price here")
mortgage_period = Select(title="Mortgage period:", value="30", options=['7', '10', '15', '20', '30'])
interest_rate = Slider(title="Interest rate (%):", value=5, start=2, end=10, step=0.1)
house_type = Select(title="House type:", value="single family house", options=['condo', 'townhouse', 'single family house'])

button_1 = Button(label="Submit")
button_2 = Button(label="Reset")
output = Paragraph(width=600, height=300) #or use pretext, for a <pre> tag in html


def monthly_expenses(list_price, mortgage_period,interest_rate,house_type):
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

def submit():
    #these are made up coefficients for now
    value = monthly_expenses(float(listprice.value), float(mortgage_period.value), float(interest_rate.value), house_type.value)
    output.text = 'Your estimated monthly cost is: ' + str(value) + ' $'
    
def reset():
    reset_output()
    output.text = None

button_1.on_click(submit)

button_2.on_click(reset)

#lay_out = layout([[select1, select2, select3, select4], [button_1, button_2], [output]])
lay_out = layout(
            children=[
            [listprice],
            [mortgage_period],
            [interest_rate],
            [house_type],
            [button_1],
            [button_2],
            [output]
            ],
            sizing_mode='fixed',
            )
curdoc().add_root(lay_out)
curdoc().title = "Predict the monthly cost of your first home"



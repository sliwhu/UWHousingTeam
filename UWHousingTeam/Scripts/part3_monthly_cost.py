# importing required packages
'''
How to use this file:

How to initiate bokeh server using this file:

type bokeh serve --port 5003 widgets_part3.py in your terminal
Then you may go to the FirstStop landing page to click the calculating monthly cost link


'''

from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models.widgets import Button, TextInput, Select, Slider, Paragraph, Div


LOGO = Div(text="""<img src="https://s3-us-west-2.amazonaws.com/data515logo/logo_title_thinner.PNG" \
    alt="" />""")
# Create Input Controls
LISTPRICE = TextInput(title="enter list price/predict price here")
MORTGATE_PERIOD = Select(title="Mortgage period:", value="30", options=['7', '10', '15', '20', '30'])
INTEREST_RATE = Slider(title="Interest rate (%):", value=5, start=2, end=10, step=0.1)
HOUSE_TYPE = Select(title="House type:", value="single family house", options=['condo', \
    'townhouse', 'single family house'])

BUTTON_1 = Button(label="Submit")
BUTTON_2 = Button(label="Reset")
OUTPUT = Paragraph(width=600, height=300) #or use pretext, for a <pre> tag in html


def monthly_expenses(list_price, mortgage_period, interest_rate, house_type):
    '''
    calculate monthly expenses
    '''
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
    '''
    click to submit
    '''
    value = monthly_expenses(float(LISTPRICE.value), float(MORTGATE_PERIOD.value), \
        float(INTEREST_RATE.value), HOUSE_TYPE.value)
    OUTPUT.text = 'Your estimated monthly cost is: ' + str(int(value)) + ' $'
    
def reset():
    '''
    click to reset
    '''
    OUTPUT.text = None

BUTTON_1.on_click(submit)

BUTTON_2.on_click(reset)

LAY_OUT = layout(children=[[LOGO], [LISTPRICE], [MORTGATE_PERIOD], [INTEREST_RATE], \
    [HOUSE_TYPE], [BUTTON_1], [BUTTON_2], [OUTPUT]], sizing_mode='fixed')

curdoc().add_root(LAY_OUT)
curdoc().title = "Predict the monthly cost of your first home"



"""
How to use this file:
have the data, main_data.csv, and the machine learning model file,
house_price_model_2.py, in the same folder with this file

change data path follow instructions in the house_price_model_2.py file:
for windows user -
os.environ["SALES_DATA_PATH"] = r'the path where Merged_Data.csv is saved', e.g.: "~/directory"
os.environ["SALES_DATA_FILE"] = 'Merged_Data.csv'

type bokeh serve --port 5001 main2.py in your terminal
Then you may go to the FirstStop landing page to click the predicting price link
"""
import pandas as pd
from bokeh.io import curdoc
#from bokeh.tile_providers import STAMEN_TONER
from bokeh.models import (
    GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d,
    PanTool, WheelZoomTool, BoxSelectTool, HoverTool
)
from bokeh.layouts import layout
from bokeh.models.widgets import Button, \
    Select, Slider, Paragraph, Div
from house_price_model_2 import HousePriceModel

MODEL = HousePriceModel()
MODEL.initialize_model()

LOGO = Div(text="""<img src="https://s3-us-west-2.amazonaws.com/data515logo/logo_title_thinner.PNG"
alt="" />""")
DELIM_1 = Div(text="""<h2><span style="color: #800080;"
width=500 height=15>STEP 1:</span></h2>""")
DELIM_2 = Div(text="""<h2><span style="color: #800080;" width=500 height=15>STEP 2:</span></h2>""")
DELIM_3 = Div(text="""<h2><span style="color: #800080;" width=500 height=15>STEP 3:</span></h2>""")
DELIM_4 = Div(text="""<h2><span style="color: #800080;"
width=500 height=15>Almost Done. Just Submit!</span></h2>""")
DELIM_5 = Div(text="""<h2><span style="color: #800080;"
width=500 height=15>Ta Daa .....!</span></h2>""")

# Import dataset, the first sheet in the merged dataset
MAIN_DATA = pd.read_csv("main_data.csv", sep=",")

# Create widgets
BED = Select(title="Bedroom number:", value="3", options=['2', '3', '4', '5'])
BATH = Select(title="Bathroom number:", value="2", options=['2', '3', '4', '5'])
BUILTYEAR = Slider(title="Built year:", value=1900, start=1900, end=2015, step=1)
ZIPCODE = Select(title="Zipcode:", value="98004",
                 options=[str(x) for x in sorted(list(set(MAIN_DATA.zipcode.values)))])
SQFT_LIVING = Slider(title="Living Sqft:",
                     value=500, start=500, end=5500, step=10)
SQFT_LOT = Slider(title="Lot Sqft:", value=500, start=500, end=5500, step=10)
WATERFRONT = Select(title="Waterfront:", value="Either", options=['Either', 'Yes', 'No'])
#renovation = Select(title="Renovation:", value="either", options=['Yes', 'No', 'either'])
VIEW = Select(title="House view:", value="1",
              options=[str(x) for x in sorted(list(set(MAIN_DATA.view.values)))])
CONDITION = Select(title="House Condition:", value="3",
                   options=[str(x) for x in sorted(list(set(MAIN_DATA.condition.values)))])
GRADE = Select(title="House grade:", value="3",
               options=[str(x) for x in sorted(list(set(MAIN_DATA.grade.values)))])
YEAR = Select(title="Year to buy the house:", value="2017",
              options=['2017', '2018'])
MONTH = Select(title="Month to buy the house:", value="10",
               options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])


BUTTON_1 = Button(label="Submit")
BUTTON_2 = Button(label="Reset")
OUTPUT1 = Paragraph(width=300, height=25) #or use pretext, for a <pre> tag in html
OUTPUT2 = Paragraph(width=1000, height=25)

# Set the parameters and add tools to the map
MAP_OPTIONS = GMapOptions(lat=47.5480, lng=-121.9836, map_type="roadmap", zoom=8)
PLOT = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(),
                map_options=MAP_OPTIONS, plot_width=520, plot_height=520)
PLOT.api_key = "AIzaSyAA875-_BZDwKoR4bMonQUJgLxYIIZ3wzw"
SOURCE = ColumnDataSource(data=dict(lat=[],
                                    lon=[],
                                    br=[]))
CIRCLE = Circle(x="lon", y="lat", size=4, fill_color="blue", fill_alpha=0.9, line_color=None)
PLOT.add_glyph(SOURCE, CIRCLE)
MY_HOVER = HoverTool()
MY_HOVER.tooltips = [('Zipcode', '@zipcode'),
                     ('Number of bedrooms', '@br'), ('Number of bathrooms', '@ba'),
                     ('List price', '@list_price'), ('Final price', '@final_price')]
PLOT.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
PLOT.add_tools(MY_HOVER)

def update():
    """
    Callback function to subset data and update map based on inputs from the user
    """
    if WATERFRONT.value == 'Either':
        WATERFRONT.value = '0.5'
    elif WATERFRONT.value == 'Yes':
        WATERFRONT.value = '1'
    else:
        WATERFRONT.value = '0'
    features = {'sale_day':
                    MODEL.calculate_sale_day_by_day(int(YEAR.value), int(MONTH.value), 15),
                'bathrooms': float(BATH.value),
                'sqft_living': float(SQFT_LIVING.value),
                'sqft_lot': float(SQFT_LOT.value),
                'waterfront': float(WATERFRONT.value),
                'view': int(VIEW.value),
                'condition': int(CONDITION.value),
                'grade': int(GRADE.value),
                'location':
                    MODEL.look_up_zipcode_by_string(ZIPCODE.value)
               }
    value = MODEL.predict(features)
    OUTPUT1.text = 'The predicted price of your house is: $' + str(value)
    sub_data = MAIN_DATA[MAIN_DATA.bedrooms == int(BED.value)]
    sub_data = sub_data[sub_data.bathrooms == float(BATH.value)]
    #sub_data = sub_data[sub_data.zipcode == int(zipcode.value)]
    select_on_price_lower_limit = int(value) - 10000
    select_on_price_upper_limit = int(value) + 10000
    sub_data = sub_data[sub_data['List price'] > select_on_price_lower_limit]
    sub_data = sub_data[sub_data['List price'] < select_on_price_upper_limit]
    sub_data = sub_data[sub_data.yr_built > int(BUILTYEAR.value)]
    SOURCE.data = {'lat':sub_data['lat'], 'lon':sub_data['long'], 'br':sub_data['bedrooms'],
                   'ba':sub_data['bathrooms'], 'zipcode':sub_data['zipcode'],
                   'list_price':sub_data['List price'], 'final_price': sub_data['price']}
    OUTPUT2.text = 'Houses with ' + str(BED.value) + ' bedrooms, ' \
                   + str(BATH.value) + ' bathrooms, built after year ' \
                   + str(BUILTYEAR.value) + \
                    ' and list price as ' + str(value) + \
                   '(+/-10000$) are shown on this map. Hover to see detail information'


def reset():
    """
    Function to clear output
    """
    OUTPUT1.text = None
    OUTPUT2.text = None

# Submit prediction and update map at each clicking of button 1
BUTTON_1.on_click(update)
# Clear output at each clicking of button 2
BUTTON_2.on_click(reset)

# Load initial map
update()

# Define UI layout
L1 = layout(children=[[LOGO], [DELIM_1], [BED, BATH, BUILTYEAR, ZIPCODE], [DELIM_2],
                      [SQFT_LIVING, SQFT_LOT, WATERFRONT, VIEW], [DELIM_3], [GRADE, CONDITION],
                      [DELIM_4], [BUTTON_1, BUTTON_2], [DELIM_5], [OUTPUT1], [OUTPUT2], [PLOT]])
curdoc().add_root(L1)
curdoc().title = "Predict the price of your first home"

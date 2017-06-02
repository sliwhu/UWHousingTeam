"""
How to use this file:
have the data, main_data.csv, and the machine learning model file, house_price_model_2.py, in the same folder with this file

change data path follow instructions in the house_price_model_2.py file:
for windows user - 
os.environ["SALES_DATA_PATH"] = r'the path where Merged_Data.csv is saved', e.g.: "~/directory"
os.environ["SALES_DATA_FILE"] = 'Merged_Data.csv'

type bokeh serve --port 5001 main2.py in your terminal
Then you may go to the FirstStop landing page to click the predicting price link
"""
import pandas as pd
from bokeh.io import output_file, show, save, curdoc, reset_output
from bokeh.tile_providers import STAMEN_TONER
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, Patches, HoverTool
)
from bokeh.layouts import widgetbox, layout, column
from bokeh.models.widgets import Button, TextInput, RadioButtonGroup, Select, Slider, Paragraph, Panel, Tabs, Div
from bokeh.plotting import figure, show
from house_price_model_2 import HousePriceModel

model = HousePriceModel()
model.initialize_model()

#Logo = Div(text="""<img src="https://s3-us-west-2.amazonaws.com/data515logo/logo_title.PNG" />""")

Logo = Div(text="""<img src="https://s3-us-west-2.amazonaws.com/data515logo/logo_title_thinner.PNG" alt="" />""")
#delim1 = Div(text="""<h2><span style="color: #800080;">STEP 1: Please select the first set of inputs.&nbsp;</span></h2>""")
delim1 = Div(text="""<h2><span style="color: #800080;" width=500 height=15>STEP 1:</span></h2>""")
delim2 = Div(text="""<h2><span style="color: #800080;" width=500 height=15>STEP 2:</span></h2>""")
delim3 = Div(text="""<h2><span style="color: #800080;" width=500 height=15>STEP 3:</span></h2>""")
delim4 = Div(text="""<h2><span style="color: #800080;" width=500 height=15>Almost Done. Just Submit!</span></h2>""")
delim5 = Div(text="""<h2><span style="color: #800080;" width=500 height=15>Ta Daa .....!</span></h2>""")
#Title = Div(text="""<blockquote>
#<h4 style="text-align: left;">You are one step closer to your dream home.&nbsp;Please enter your inputs below</h4>
#</blockquote>""")

# Import dataset, the first sheet in the merged dataset
main_data = pd.read_csv("main_data.csv", sep = ",")

# Create widgets
bed = Select(title="Bedroom number:", value="3", options=['2', '3', '4', '5'])
bath = Select(title="Bathroom number:", value="2", options=['2', '3', '4', '5'])
builtyear = Slider(title="Built year:", value=1900, start=1900, end=2015, step=1)
zipcode = Select(title="Zipcode:", value = "98004", options=[str(x) for x in sorted(list(set(main_data.zipcode.values)))])
sqft_living = Slider(title="Living Sqft:", value=500, start=500, end=5500, step=10)
sqft_lot = Slider(title="Lot Sqft:", value=500, start=500, end=5500, step=10)
waterfront = Select(title="Waterfront:", value="Either", options=['Either', 'Yes', 'No'])
#renovation = Select(title="Renovation:", value="either", options=['Yes', 'No', 'either'])
view = Select(title="House view:", value="1", options=[str(x) for x in sorted(list(set(main_data.view.values)))])
condition = Select(title="House Condition:", value="3", options=[str(x) for x in sorted(list(set(main_data.condition.values)))])
grade = Select(title="House grade:", value="3", options=[str(x) for x in sorted(list(set(main_data.grade.values)))])
year = Select(title="Year to buy the house:", value="2017", options=['2017', '2018'])
month = Select(title="Month to buy the house:", value="10", options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])


button_1 = Button(label="Submit")
button_2 = Button(label="Reset")
output1 = Paragraph(width=300, height=25) #or use pretext, for a <pre> tag in html
output2 = Paragraph(width=1000, height=25)

# Set the parameters and add tools to the map
map_options = GMapOptions(lat=47.5480, lng=-121.9836, map_type="roadmap", zoom=8)
plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, plot_width=520, plot_height=520)
plot.api_key = "AIzaSyAA875-_BZDwKoR4bMonQUJgLxYIIZ3wzw"
source = ColumnDataSource(data=dict(lat=[], 
                                    lon=[],
                                    br=[]))
circle = Circle(x="lon", y="lat", size=4, fill_color="blue", fill_alpha=0.9, line_color=None)
plot.add_glyph(source, circle)
my_hover = HoverTool()
my_hover.tooltips = [('Zipcode', '@zipcode'), ('Number of bedrooms', '@br'), ('Number of bathrooms', '@ba'), ('List price', '@list_price'), ('Final price', '@final_price')]
plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
plot.add_tools(my_hover)

# Callback function to subset data and update map based on inputs from the user
def update():
    if waterfront.value == 'Either':
        waterfront.value = '0.5'
    elif waterfront.value == 'Yes':
        waterfront.value = '1'
    else:
        waterfront.value = '0'
    features = {'sale_day':
                    model.calculate_sale_day_by_day(int(year.value), int(month.value), 15),
                'bathrooms': float(bath.value),
                'sqft_living': float(sqft_living.value),
                'sqft_lot': float(sqft_lot.value),
                'waterfront': float(waterfront.value),
                'view': int(view.value),
                'condition': int(condition.value),
                'grade': int(grade.value),
                'location':
                    model.look_up_zipcode_by_string(zipcode.value)
               }
    value = model.predict(features)
    output1.text = 'The predicted price of your house is: $' + str(value)
    sub_data = main_data[main_data.bedrooms == int(bed.value)]
    sub_data = sub_data[sub_data.bathrooms == float(bath.value)]
    #sub_data = sub_data[sub_data.zipcode == int(zipcode.value)]
    select_on_price_lower_limit = int(value) - 10000
    select_on_price_upper_limit = int(value) + 10000
    sub_data = sub_data[sub_data['List price'] > select_on_price_lower_limit]
    sub_data = sub_data[sub_data['List price'] < select_on_price_upper_limit]
    sub_data = sub_data[sub_data.yr_built > int(builtyear.value)]
    source.data = {'lat':sub_data['lat'], 'lon':sub_data['long'], 'br':sub_data['bedrooms'], 'ba':sub_data['bathrooms'], 'zipcode':sub_data['zipcode'], 'list_price':sub_data['List price'], 'final_price': sub_data['price']}
    output2.text = 'Houses with ' + str(bed.value) + ' bedrooms, ' + str(bath.value) + ' bathrooms, built after year ' + str(builtyear.value) + \
                    ' and list price as ' + str(value) + '(+/-10000$) are shown on this map. Hover to see detail information'


# Function to clear output
def reset():
    #reset_output()
    output1.text = None
    output2.text = None
    
    
    
# Submit prediction and update map at each clicking of button 1
button_1.on_click(update)
# Clear output at each clicking of button 2
button_2.on_click(reset)

# Load initial map
update()

# Define UI layout
l1 = layout(children=[[Logo],[delim1],[bed, bath, builtyear, zipcode], [delim2], [sqft_living, sqft_lot, waterfront, view], [delim3], [grade, condition], [delim4], [button_1, button_2], [delim5], [output1],[output2],[plot]])
curdoc().add_root(l1)
curdoc().title = "Predict the price of your first home"
#tab1 = Panel(child=l1,title="Housing Price Prediction")
#tab2 = Panel(child=l2,title="Bidding Price Prediction")

#tabs = Tabs(tabs=[tab1, tab2])

#curdoc().add_root(tabs)



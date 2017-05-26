'''
How to use this file:

have the data, main_data.csv, in the same folder with this file
type bokeh serve main1.py in your terminal
open a web brower and go to localhost:5006, the page will show

'''

import pandas as pd
from bokeh.io import output_file, show, save
from bokeh.tile_providers import STAMEN_TONER
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, Patches
)
from bokeh.models import HoverTool
from bokeh.io import curdoc, output_file, show
from bokeh.layouts import widgetbox, layout, column
from bokeh.models.widgets import Button, TextInput, RadioButtonGroup, Select, Slider, Paragraph, Panel, Tabs
from bokeh.plotting import figure, show, output_server

# create widgets
text_input = TextInput(value='Lisa')
select1 = Select(title="Bedroom number:", value="2", options=['2', '3', '4', '5'])
select2 = Select(title="Bathroom number:", value="2", options=['2', '3', '4', '5'])
select3 = Select(title="Sqft:", value="1000", options=['1000', '1500', '2000', '2500'])
select4 = Select(title="Built year:", value="2", options=['2', '3', '4', '5'])

button_1 = Button(label="Submit")
button_2 = Button(label="Reset")
output = Paragraph()

# Predict housing price using a linear model
def submit():
	coefficients = [100000, 10000, 1, 1]
	# value = select1.value * coefficients[0]  
	# + select2.value * coefficients[1] + \
 #    select3.value * coefficients[2] + select4.value*coefficients[3]
	output.text = 'Your house is predicted as, ' + select3.value + '$'

# Import dataset, the first sheet in the merged dataset
main_data = pd.read_csv("main_data.csv", sep = ",")

# Set the parameters and add tools for the map
map_options = GMapOptions(lat=47.5480, lng=-121.9836, map_type="roadmap", zoom=10)
plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, plot_width=240, plot_height=360, title="Title")
plot.api_key = "AIzaSyAA875-_BZDwKoR4bMonQUJgLxYIIZ3wzw"
circle = Circle(x="lon", y="lat", size=2, fill_color="blue", fill_alpha=0.9, line_color=None)

# Subset data and update map based on inputs from the user
def update():
    sub_data = main_data[main_data.bedrooms == int(select1.value)]
    sub_data = sub_data[main_data.bedrooms == int(select2.value)]
    source = ColumnDataSource(data=dict(lat=sub_data['lat'], 
                                        lon=sub_data['long'],
                                        br=sub_data['bedrooms']))
    plot.add_glyph(source, circle)

my_hover = HoverTool()
my_hover.tooltips = [('Lattitude of the point', '@lat'), ('Longitude of the point', '@lon'), ('Number of Bedrooms', '@br')]
plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
plot.add_tools(my_hover)

# Load initial map
update()

# Submit prediction and update map at each clicking of button 1
button_1.on_click(submit)
button_1.on_click(update)

#inputs = widgetbox(children=[select1, select2, select3, select4, button_1, button_2], sizing_mode=sizing_mode)
#lay_out = layout([inputs, plot], sizing_mode=sizing_mode)

#lay_out = layout([[select1, select2], [select3, select4, plot], [button_1, button_2], [output]])

# How to do tabs

l1 = layout(children=[[select1, select2], [select3, select4, plot], [button_1, button_2], [output]], sizing_mode='fixed')
l2 = layout(children=[[select1, select2], [select3, select4, plot], [button_1, button_2], [output]], sizing_mode='fixed')

tab1 = Panel(child=l1,title="Housing Price Prediction")
tab2 = Panel(child=l2,title="Bidding Price Prediction")

tabs = Tabs(tabs=[tab1, tab2])

curdoc().add_root(tabs)

curdoc().add_root(lay_out)

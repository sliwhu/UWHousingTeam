import pandas as pd
from bokeh.io import output_file, show, save, curdoc
from bokeh.tile_providers import STAMEN_TONER
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool, Patches, HoverTool
)
from bokeh.layouts import widgetbox, layout, column
from bokeh.models.widgets import Button, TextInput, RadioButtonGroup, Select, Slider, Paragraph, Panel, Tabs
from bokeh.plotting import figure, show

# Create widgets
select1 = Select(title="Bedroom number:", value="2", options=['2', '3', '4', '5'])
select2 = Select(title="Bathroom number:", value="2", options=['2', '3', '4', '5'])
select3 = Select(title="Sqft:", value="1000", options=['1000', '1500', '2000', '2500'])
select4 = Select(title="Built year:", value="2", options=['2', '3', '4', '5'])

button_1 = Button(label="Submit")
button_2 = Button(label="Reset")
output = Paragraph()

# Import dataset, the first sheet in the merged dataset
main_data = pd.read_csv("main_data.csv", sep = ",")

# Set the parameters and add tools to the map
map_options = GMapOptions(lat=47.5480, lng=-121.9836, map_type="roadmap", zoom=10)
plot = GMapPlot(x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, plot_width=520, plot_height=520)
plot.api_key = "AIzaSyAA875-_BZDwKoR4bMonQUJgLxYIIZ3wzw"
source = ColumnDataSource(data=dict(lat=[], 
                                    lon=[],
                                    br=[]))
circle = Circle(x="lon", y="lat", size=4, fill_color="blue", fill_alpha=0.9, line_color=None)
plot.add_glyph(source, circle)
my_hover = HoverTool()
my_hover.tooltips = [('Lattitude of the point', '@lat'), ('Longitude of the point', '@lon'), ('Number of Bedrooms', '@br')]
plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
plot.add_tools(my_hover)

# Callback function to subset data and update map based on inputs from the user
def update():
    output.text = 'Your house is predicted as, $' + select1.value 
    sub_data = main_data[main_data.bedrooms == int(select1.value)]
    sub_data = sub_data[sub_data.bathrooms == float(select2.value)]
    source.data = {'lat':sub_data['lat'], 'lon':sub_data['long'], 'br':sub_data['bedrooms']}
    
    
    
# Submit prediction and update map at each clicking of button 1
button_1.on_click(update)

# Load initial map
update()

# Define UI layout
l1 = layout(children=[[select1, select2], [select3, select4, plot], [button_1, button_2], [output]], sizing_mode='fixed')
curdoc().add_root(l1)

#tab1 = Panel(child=l1,title="Housing Price Prediction")
#tab2 = Panel(child=l2,title="Bidding Price Prediction")

#tabs = Tabs(tabs=[tab1, tab2])

#curdoc().add_root(tabs)



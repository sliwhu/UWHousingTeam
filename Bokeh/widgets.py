'''
How to use this file:

type bokeh serve widgets.py in your terminal
open a web brower and go to localhost:5006, the page will show

'''


from bokeh.io import curdoc, output_file, show, reset_output
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import Button, TextInput, RadioButtonGroup, Select, Slider, Paragraph


# Create Input Controls 
bed = Select(title="Bedroom number:", value="0", options=['2', '3', '4', '5'])
bath = Select(title="Bathroom number:", value="0", options=['2', '3', '4', '5'])
sqft = Slider(title="Sqft:", value=1800, start=500, end=5500, step=10)
builtyear = Slider(title="Built year:", value=2000, start=1960, end=2015, step=1)
waterfront = Select(title="Waterfront:", value="either", options=['Yes', 'No', 'either'])
renovation = Select(title="Renovation:", value="either", options=['Yes', 'No', 'either'])
zipcode = TextInput(title="enter zipcode here")

button_1 = Button(label="Submit")
button_2 = Button(label="Reset")
output = Paragraph(width=600, height=300) #or use pretext, for a <pre> tag in html

def determine(parameter):
	if parameter.value == 'Yes':
		parameter.value = str(1)
	elif parameter.value == 'No':
		parameter.value = str(0)
	else:
		parameter.value = str(0.5)

def submit():
	#these are made up coefficients for now
	coefficients = [100000, 10000, 1, 1, 5, 5]
	determine(waterfront)
	determine(renovation)
	value = float(bed.value) * coefficients[0] + float(bath.value) * coefficients[1] + \
 		 float(sqft.value) * coefficients[2] + float(builtyear.value)*coefficients[3] + \
 		 float(waterfront.value)*coefficients[4] + float(renovation.value)*coefficients[5]
	output.text = 'Your house is predicted as, ' + str(value) + ' $'
	
def reset():
	reset_output()
	output.text = None

button_1.on_click(submit)

button_2.on_click(reset)

#lay_out = layout([[select1, select2, select3, select4], [button_1, button_2], [output]])
lay_out = layout(
			children=[
			[bed, bath],
			[sqft, builtyear],
			[waterfront, renovation],
			[button_1],
			[button_2],
			[output]
			],
			sizing_mode='fixed',
			)
curdoc().add_root(lay_out)
curdoc().title = "Predict the price of your first home"
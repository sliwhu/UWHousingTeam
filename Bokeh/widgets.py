'''
How to use this file:

type bokeh serve widgets.py in your terminal
open a web brower and go to localhost:5006, the page will show

'''


from bokeh.io import curdoc, output_file, show
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import Button, TextInput, RadioButtonGroup, Select, Slider, Paragraph


# create some widgets
text_input = TextInput(value='Lisa')
select1 = Select(title="Bedroom number:", value="0", options=['2', '3', '4', '5'])
select2 = Select(title="Bathroom number:", value="0", options=['2', '3', '4', '5'])
select3 = Select(title="Sqft:", value="0", options=['1000', '1500', '2000', '2500'])
select4 = Select(title="Built year:", value="0", options=['2', '3', '4', '5'])


button_1 = Button(label="Submit")
button_2 = Button(label="Reset")
output = Paragraph()

def submit():
	coefficients = [100000, 10000, 1, 1]
	# value = select1.value * coefficients[0]  
	# + select2.value * coefficients[1] + \
 #    select3.value * coefficients[2] + select4.value*coefficients[3]
	output.text = 'Your house is predicted as, ' + select3.value + '$'

button_1.on_click(submit)

lay_out = layout([[select1, select2, select3, select4, button_1, button_2], [output]])

curdoc().add_root(lay_out)
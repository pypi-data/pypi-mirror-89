## Cereals.py

import pandas as pd
import pygal
from IPython.display import SVG, display
from pygal.style import Style 

class Cereals_nutrition:
    def display_Cereals(self):
        data = pd.read_excel("cereal.xlsx", sheet_name='Modified_Cereal', index_col=0)
        self.bar_chart = pygal.HorizontalStackedBar() 
        self.bar_chart.title = "Nutrient composition of cereals"
        self.bar_chart.add('protein', data['protein'] ) 
        self.bar_chart.add('calories (X100)', data['calories']/100) 
        self.bar_chart.add('fat', data['fat'])
        self.bar_chart.add('sodium (X100)', data['sodium']/100 )
        self.bar_chart.add('fiber', data['fiber'])
        self.bar_chart.add('carbohydrates', data['carbo'])
        self.bar_chart.add('sugar', data['sugars'])
        self.bar_chart.add('potassium (X100)', data['potass']/100)
        self.bar_chart.add('vitamins (X10)', data['vitamins']/10)


        self.bar_chart.render_to_file('HorizontalStackedBar.svg')
        display(SVG(self.bar_chart.render (disable_xml_declaration=True)))

class deficiency_nutrition:
    def display_worldmap(self):
        custom_style = Style( colors = ('#FF0000' , '#0000FF' , '#00FF00' , '#000000', '#FFD700')) 
        self.worldmap =  pygal.maps.world.World(style = custom_style) 
        self.worldmap.title = "Nutrient deficient countries"
        self.worldmap.add('Protein deficient', ['in', 'br', 'sa'])
        self.worldmap.add('Calories deficient',['so', 'tg', 'mw'])
        self.worldmap.add('vitamin deficient', ['ke', 'ml', 'ng', 'sd', 'ao'])
        self.worldmap.add('sodium deficient', ['ph', 'eg', 'gh'])
        self.worldmap.add('iron deficient', ['ye','za', 'pk'])
        self.worldmap.render_to_file('nutrient.svg')
        display(SVG(self.worldmap.render (disable_xml_declaration=True))) 

## We were trying to add hover for the Cereals horizontal stacked bar but just ran out of time. We will try to add that for 
## Lab 3 so that we can distinguish bars for each cereal type.
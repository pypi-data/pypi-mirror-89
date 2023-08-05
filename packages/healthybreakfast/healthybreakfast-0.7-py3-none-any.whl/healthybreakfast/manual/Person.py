import pandas as pd
import matplotlib.pyplot as plt

def New_error():
    pass

class diet:
    def default_values(self,gender,nutrient):
        # Add more default values:
        diet={"man": {"protein": 56,"cal": 2500,"fat":83, "sodium":2300, "fiber":38, "carbs":300,"potassium":3000},
               "woman": {"protein": 46,"cal": 2000, "fat":67,"sodium": 2000, "fiber":25,"carbs":250,"potassium":2300}}
        
        try:
            if (type(gender)!=str):
                raise New_error()
        except New_error:
            print("Enter a valid gender, male or female only!")
        
        try:
            diet[gender]
        except KeyError:
            print("Invalid key, please check!")
        else:
            return diet[gender]
        
  
    def display_function():
        print("Hey there! Here is your Nutrional Manual!!")
        
        
class manual_display(diet):
    def __init__(self,gender,nutrient):
        self.gender=gender
        self.nutrient=nutrient
    
    def required_bar_graphs(self):
        diet.display_function()

        dict_mw=diet.default_values(self,self.gender, self.nutrient)

        keys=dict_mw.keys()
        values=dict_mw.values()
        plt.bar(keys,values)
        return plt.gca()
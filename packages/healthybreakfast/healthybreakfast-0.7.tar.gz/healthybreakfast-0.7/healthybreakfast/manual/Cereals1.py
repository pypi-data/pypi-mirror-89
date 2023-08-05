# Cereals1.py
import pandas as pd
import matplotlib.pyplot as plt
class Cereals_nutrition1:
    def display_Cereals1(self):
        data = pd.read_excel("cereal.xlsx", sheet_name='Modified_Cereal', index_col=0)
        bar = data.loc[:, ['calories', 'protein', 'fat', 'sodium', 'fiber', 'carbo', 'sugars', 'potass', 'vitamins']]
        fig = bar.plot(kind='barh', stacked=True, figsize=(12,12), title="Nutrient composition of cereals")
        fig.set_ylabel("Cereals")
            
        return plt.gca()

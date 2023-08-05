import pandas as pd
import matplotlib.pyplot as plt
df_1=pd.read_excel("cereal.xlsx",sheet_name='Modified_Cereal')

def recommend(protein,calories):
    
    one=df_1[(df_1['protein']>=protein)]
    two=one[(one['calories']<=calories)]
    sorted_= two.sort_values(by='protein',ascending=False)
    #bar=sorted_.plot.bar(x='name',y=['protein','fat'])
    return sorted_.iloc[0,0]


def my_cereal(name1,name2=0):
    x=[]
    # Filter the DataFrame in accordance to the cereal we want:
    data_filter=df_1.drop(['weight','cups'],axis=1)
    
    if name2!=0:
        plot_data=data_filter[(data_filter['name']==name1)|(data_filter['name']==name2)]
    else:
        plot_data=data_filter[(data_filter['name']==name1)]
    
    # Plot the graph for nutritional information between two different cereals, for comparison:
    ax=plot_data.plot.bar(x='name',grid='on',figsize=(14,4))
    for p in ax.patches:
        x.append(p.get_height())
        ax.annotate(str(round(p.get_height())), (p.get_x() * 1.005, p.get_height() * 1.005))
        
    return plt.gca()
    
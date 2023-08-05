# Import the required Packages information:
import pandas as pd
import matplotlib.pyplot as plt
#import sys

# User defined errors:
class InputError(Exception):
    print("Wrong Input Value")

# Defining the parent class which has all the default nutritional values and some default display statements:
class Diet:
    import pandas as pd
    diet={}
    def __init__(self,name):
        self.name=name
        #self.age=age

    def default_values(self,gender,nutrient):
        diet={"man": {"p": 65,"cal": 2900},
               "woman": {"p": 50,"cal": 2000}}
        
        ############################### key error statement ############################
        try:
            diet[gender][nutrient]
        except KeyError:
            print("Please enter a valid key value")
        else:
            return diet[gender][nutrient]
            
            
        #return diet[gender][nutrient]
    
    def display_values(self,name=0):
        if name==0:
            print("Hi!",self.name,"OOPS! Your nutrient levels are not up to the mark!")
            print("You are deficient by: \n")
            
        else:
            print("Hi",name,"OOPS! Your nutrient levels are not up to the mark!")
            print("You are deficient by: \n")
   
        
# Defining the child class as calculation the deficient values and giving a pictorical representation,
# for the deficient amount:

class Deficiency(Diet):
    import pandas as pd
    
    def __init__(self,w_protein=0,w_cal=0,w_name=0):
        Diet.__init__(self,w_name)
        self.w_name=w_name
        self.w_protein=w_protein
        self.w_cal=w_cal
        
    def women(self):
        ###################### Check for the datatype of the input values ########################
        try:
            self.w_protein=int(self.w_protein)
        except ValueError:
            print("Enter a valid numeric value and try again")
            self.dif_p=0
        else:
            self.dif_p = self.w_protein-Diet.default_values(self,"woman","p")
            
        try:
            if self.w_cal<0:
                raise InputError
        except InputError:
            print("Enter a positive value")
            self.dif_cal=0
        except TypeError: 
            print("Enter a valid numeric value and try again")
            self.dif_cal=0
        else:
            self.dif_cal=Diet.default_values(self,"woman","cal") - self.w_cal
        
        
        
        if (self.dif_p<0 or self.dif_cal<0):
            Diet.display_values(self)
            fig,axes=plt.subplots(nrows=1,ncols=2,figsize=(14,2))
            df=pd.DataFrame({"your_protein_value": [self.w_protein],
                         "required_value":[Diet.default_values(self,"woman","p")]})
            df.plot.barh(color={"your_protein_value":"red", "required_value":"green"},rot=0,align='center',ax=axes[0])
            df_1=pd.DataFrame({"your_cal_value":[self.w_cal],
                          "required_value":[Diet.default_values(self,"woman","cal")]})
            df_1.plot.barh(rot=0,align='edge',ax=axes[1])
        
        elif (self.dif_p==0 and self.dif_cal==0):
            print("Please enter valid set of values")

        else:
            print("Hey!!{} You are having all the required nutrient contents! Way to go!\n".format(self.w_name))
        return plt.gca()
        
        
    def couple(self,m_protein,m_cal,m_name):
        if self.w_protein==0:
            Diet.display_values(self,m_name)
            self.deficiency_m(m_protein,m_cal,m_name)
        else:
            self.women()
            self.men(m_protein,m_cal,m_name)
                   

        
    def men(self,m_protein,m_cal,m_name):
        self.dif_p_m=Diet.default_values(self,"man","p") - m_protein
        self.dif_cal_m=Diet.default_values(self,"man","p")- m_cal
        if (self.dif_p_m<0 or self.dif_cal_m<0):
            Diet.display_values(self,m_name)
            fig,axes=plt.subplots(nrows=1,ncols=2,figsize=(14,2))
            df=pd.DataFrame({"your_protein_value": [m_protein],
                         "required_value":[Diet.default_values(self,"man","p")]})
            df.plot.barh(color={"your_protein_value":"red", "required_value":"green"},rot=0,ax=axes[0])
            df_1=pd.DataFrame({"your_cal_value":[m_cal],
                          "required_value":[Diet.default_values(self,"man","cal")]})
            df_1.plot.barh(rot=0,align='edge',ax=axes[1])
        
            

        else:
            print("Hey!! You have all the required nutrient contents! Way to go!")
        return plt.gca()
        
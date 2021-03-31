import pandas as pd
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns

#import the file as a pandas df
#variable name "stalcDF" - which references ST.udent ALC.ohol.
stalcDF = pd.read_csv("kaggle-alcohol/student-mat.csv", encoding = "ISO-8859-1") 

#first thing to do is pair up the data headers with the data in the first row
ob = stalcDF.iloc[0].reset_index().apply(tuple, axis=1)  #write array col head & row1 to a dict_items
                                        # https://stackoverflow.com/questions/62244179/how-to-convert-dict-items-object-to-list
colHeader_row1_list = [] 
for key, value in ob:
    list_item = (key,value)
    colHeader_row1_list.append(list_item)

categorical_cols = [] #this will be the list of categorical attributes
numeric_cols = []     #this will be the list of numeric attributes

for i, x in colHeader_row1_list:
#     print((type(x)),i,x) # just check what kind of format the data is in (e.g., int or numpy.int64)
    if type(x) != str: 
        numeric_cols.append(i)
    else:
        categorical_cols.append(i)
        
print("There are:", (len(categorical_cols)), "text columns")
                            # 'school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob', 
                            # 'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities', 
                            # 'nursery', 'higher', 'internet', 'romantic']
print("There are:", (len(numeric_cols)), "numeric columns")
                            # ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 
                            #  'failures', 'famrel', 'freetime', 
                            #  'goout', 'Dalc', 'Walc', 'health', 
                            #  'absences', 'G1', 'G2', 'G3']
                
#Should print: 
  #There are: 17 text columns
  #There are: 16 numeric columns
  
  
#convert text in the columns with text data to numeric form via label encoding..
#which adds 17 new features to my set.
for i in categorical_cols:
#     print(i)
    stalcDF[i] = stalcDF[i].astype("category")
    stalcDF[(i+"_CAT")]  = stalcDF[i].cat.codes #duplicate each column encoded, and add "_CAT" after it
#len(stalcDF.columns) # prints = 50

#duplicate the DataFrame
stalcDF_N= stalcDF.copy() 

print("Length of stalcDF_N before dropping textual columns:",len(stalcDF_N.columns)) #should print 50 on the first run
for i in categorical_cols:
    if i in stalcDF_N:
        print("dropping", i, "\n....")
        stalcDF_N.drop([i], axis=1, inplace=True) 
        print("dropped", i, "!")
    else:
        pass
print("\nLength of stalcDF_N after dropping textual columns:",len(stalcDF_N.columns)) #should print 31


###Actual encoding happens here

stalcDF['Avg_Grade'] = stalcDF[['G1', 'G2','G3']].mean(axis=1) 
stalcDF.drop(['G1', 'G2','G3'], axis=1, inplace=True) #drop the 3 colums
#Create the new merged and rounded-up column for Alcohol Consumption 
stalcDF['Avg_Alc_Cnsmptn'] = stalcDF[['Dalc', 'Walc']].mean(axis=1) 
stalcDF.drop(['G1', 'G2','G3'], axis=1, inplace=True) #drop the 3 colums



"""You just need to call the get_informations() function with the parameters :temperature or rainfall or emissions and the function relations() with the parameters temperature and rainfall """
"""for the second parameter of these functions you can add a title of your choice """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
#loading all the dataset
meteo = pd.read_excel("mto.xlsx")
ghg = pd.read_csv("ghg.csv")
#explatory data analysis
print(meteo.head())
print(ghg.head())
# we don't need to check NA values because there aren't any unavaible values
#ghg dataset cleaning
indexes = np.arange(1993,2023).astype("str")
population  = 3.5 #this is the average population number of the analamanga region
emissions =((np.array(ghg[indexes]).T)*3.5).reshape((30,))

#meteo dataset cleaning
meteo["mean_temperature"] = (meteo["Tmax(°C)"]+meteo["Tmin(°C)"])/2
temperature = meteo["mean_temperature"].groupby(by = meteo["date"].dt.year).mean()
rainfall = meteo["RR(mm)"].groupby(by = meteo["date"].dt.year).sum()
#plot size configuration
plt.grid()
plt.figure(figsize = (30,25))
plt.rc("xtick",labelsize = 20)
plt.rc("ytick",labelsize = 25)
plt.rc("font",size = 25)
plt.style.use("ggplot")
font = {"size":35}
#getting all the needed information
def get_information(parameter,title = None):
    #trendline configuration
    model = LinearRegression()
    model.fit(indexes.astype("int64").reshape((30,1)),parameter)
    trend = model.predict(indexes.astype("int64").reshape((30,1)))
    #plotting the distribution
    plt.subplot(2,1,1)
    plt.plot(indexes,parameter,lw = 6,color = "blue")
    plt.ylabel(title,**font)
    plt.subplot(2,1,2)
    plt.scatter(indexes,parameter,lw = 20,color = "blue")
    plt.plot(indexes,trend,lw = 6,color = "red")
    plt.title("Annual {} distribution for the Analamanga region(1993-2022)".format(title),**font)
    plt.ylabel(title,**font)
    plt.xlabel("Years",**font)
    #additionnal information
    mean = np.mean(parameter)
    std = np.std(parameter)
    coeff,p_value = pearsonr(parameter,indexes.astype("int64"))
    maximum = np.max(parameter)
    minimum = np.min(parameter)
    print("Mean value of {}".format(title),mean)
    print("Standart deviation :",std)
    print("Minimum in ",1993 + np.argmin(parameter))
    print("Value :",minimum)
    print("Maximum in",1993+np.argmax(parameter))
    print("Value",maximum) 
    print("Variation with time of {}".format(title),model.coef_)
    if p_value > 0.05:
        print("Absence of relation with time")
        print("Correlation coefficient",coeff)
        
    else:
        print("Presence of relation with time")
        print("Correlation coefficient",coeff)


#getting the relation between all the parameters
def relation(y,y_title = None):
    coeff1,p1 = pearsonr(emissions,y)
    if p1 > 0.05:
        print("Absence of relation with carbon dioxyde emission")
        print("Correlation coefficient",coeff1)
    
    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            print("Presence of relation with carbon dioxyde emission")
            print("Correlation coefficient",coeff1)
            
    fig,axis1 = plt.subplots(figsize = (30,25))
    plt.grid()
    axis1.set_xlabel("Year",**font)
    axis1.set_ylabel("Carbon dioxyde emission (MtCO2equ)",**font)
    axis1.plot(indexes,emissions,lw = 6,color = "blue",label = "Carbon dioxyde emission[MtCO2equ]")
    plt.legend(loc = "upper left")
    axis2 = axis1.twinx()
    axis2.set_ylabel(y_title,**font)
    axis2.plot(indexes,y,lw = 6,label = y_title)
    plt.legend(loc = "lower right")
    


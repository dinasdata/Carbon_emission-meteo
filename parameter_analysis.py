import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
#loading all the dataset
meteo = pd.read_excel("mto.xlsx")
ghg = pd.read_csv("historical_emissions.csv")
#explatory data analysis
"""print(meteo.head())
print(ghg.head())"""
# we don't need to check NA values because there aren't any unavaible values
#ghg dataset cleaning
indexes = np.arange(1993,2023).astype("str")
emissions = np.array(ghg[indexes])
#meteo dataset cleaning
meteo["mean_temperature"] = (meteo["Tmax(°C)"]+meteo["Tmin(°C)"])/2
temperature = meteo["mean_temperature"].groupby(by = meteo["date"].dt.year).mean()
rainfall = meteo["RR(mm)"].groupby(by = meteo["date"].dt.year).sum()
#getting all the needed information
def get_information(parameter,title):
    #trendline configuration
    model = LinearRegression()
    model.fit(indexes.astype("int64").reshape((30,1)),parameter)
    trend = model.predict(indexes.astype("int64").reshape((30,1)))
    #plot size configuration
    plt.figure(figsize = (30,25))
    plt.rc("xtick",labelsize = 20)
    plt.rc("ytick",labelsize = 25)
    font = {"size":35}
    #plotting the distribution
    plt.subplot(2,1,1)
    plt.plot(indexes,parameter,lw = 6)
    plt.grid()
    plt.subplot(2,1,2)
    plt.scatter(indexes,parameter,lw = 20)
    plt.plot(indexes,trend,lw = 6,color = "red")
    plt.grid()
    plt.title("Annual {} distribution for the Analamanga region(1993-2022)".format(title),**font)
    

#get_information(emissions.T,"CO2 emission")    
print(emissions)
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error,mean_squared_error
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn import svm
import pandas as pd
"""this is a modelisation of temperature and carbon dioxyde emission with the Support Vector Machine Regressor model"""
#dataset loadingmeteo = pd.read_excel("mto.xlsx")
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

#plot size configuration
plt.grid()
plt.figure(figsize = (30,25))
plt.rc("xtick",labelsize = 20)
plt.rc("ytick",labelsize = 25)
plt.rc("font",size = 30)
plt.style.use("ggplot")
font = {"size":30}
#data preprocessing
def preprocess(x,y):
    x = np.array(x).reshape((30,1))
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.75, random_state = 35)
    scale_model = StandardScaler()
    x_train_scaled = scale_model.fit_transform(x_train)
    x_test_scaled = scale_model.transform(x_test)
    return (x_train_scaled,x_test_scaled,y_train,y_test)
    
#Tunning hyperparameters with GridSearchCV
def grid_search_cv(x,y,gamma,kernel,C,epsilon):
    model_name = svm.SVR()
    parameters = {"gamma":gamma,"kernel":kernel,"C":C,"epsilon":epsilon}
    cross_validation = GridSearchCV(estimator = model_name,param_grid = parameters,cv = 7, scoring = "neg_mean_squared_error")
    cross_validation.fit(x,y)
    return cross_validation.best_params_["gamma"],cross_validation.best_params_["kernel"],cross_validation.best_params_["C"],cross_validation.best_params_["epsilon"]

#model creation
def model(x,y,x_prediction,y_real,gamma,kernel,C,epsilon):
    model = svm.SVR(C = grid_search_cv(x, y, gamma, kernel, C, epsilon)[2],kernel = grid_search_cv(x,y,gamma,kernel,C,epsilon)[1],gamma = grid_search_cv(x, y, gamma, kernel, C, epsilon)[0],epsilon = grid_search_cv(x, y, gamma, kernel, C, epsilon)[3])
    #model train
    model.fit(x,y)
    #model test
    predicted = model.predict(x_prediction)
    #evaluation
    r_square = model.score(x,y)
    MAE = mean_absolute_error(predicted,y_real)
    RMSE = mean_squared_error(predicted,y_real)
    print("R-2 : {}".format(r_square))
    print("MAE: {}".format(MAE))
    print("RMSE : {}".format(RMSE))
    print(grid_search_cv(x, y, gamma, kernel, C, epsilon))
    sns.kdeplot(y,fill = True,label = "fitted")
    sns.kdeplot(predicted,fill = True,label = "observed")
    plt.legend(loc = "best",fontsize = 35)
    plt.ylabel("Frequency value",**font)
    plt.xlabel("Test index",**font) 
    
  
model(preprocess(temperature,emissions)[0],preprocess(temperature,emissions)[2],preprocess(temperature,emissions)[1],preprocess(temperature,emissions)[3],[0.01,0.1,1],["linear","rbf","poly"],[20,35,50],[0.1,1,10])
    
    

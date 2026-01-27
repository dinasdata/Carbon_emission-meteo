from sklearn.linear_model import LinearRegression,Lasso
from sklearn.model_selection import train_test_split,KFold
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.pipeline import Pipeline
import numpy as np 
import pandas as pd 
import pickle 
# dataset importation
meteo = pd.read_excel("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/mto.xlsx")
meteo = meteo.dropna()
selected = meteo[["date","Tmin(°C)","Tmax(°C)"]]
selected["mean_temperature"] = (selected["Tmax(°C)"]+selected["Tmin(°C)"])/2
temperature = selected["mean_temperature"].groupby(by = selected["date"].dt.year).mean()
temperature = np.array(temperature).reshape((30,))
ghg = pd.read_csv("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/ghg.csv")
indexes = np.arange(1993,2023).astype("str")
population  = 3.5 #this is the average population number of the analamanga region
emissions =((np.array(ghg[indexes]).T)*3.5).reshape((30,1))

# Linear regression model

def linear_regression(x,y):
    global lr
    # splitting train and test split 
    x_train,x_test,y_train,y_test = train_test_split(x,y)
    # scaling train & test features
    
    def scale(train,test):
    
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(train)
        x_test_scaled = scaler.transform(test)
        return {"train_scaled":x_train_scaled,"test_scaled":x_test_scaled}
    
    x_scaled = scale(x_train,x_test)["train_scaled"]
    x_test_scaled = scale(x_train,x_test)["test_scaled"]
    model = LinearRegression()
    model.fit(x_scaled,y_train)
    lr = pickle.dumps(model)
    


# Lasso regression model

def lasso_regression(x,y):
    global lassoreg
    # splitting train and test split 
    x_train,x_test,y_train,y_test = train_test_split(x,y)
    # scaling train & test features
    
    def scale(train,test):
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(train)
        x_test_scaled = scaler.transform(test)
        return {"train_scaled":x_train_scaled,"test_scaled":x_test_scaled}
    
    x_scaled = scale(x_train,x_test)["train_scaled"]
    x_test_scaled = scale(x_train,x_test)["test_scaled"]
    model = Lasso(alpha = 1e-07)
    model.fit(x_scaled,y_train)
    lassoreg = pickle.dumps(model)

# Polynomial regression model
def polynomial_regression(x,y):
    global polyreg
    # splitting train and test split 
    x_train,x_test,y_train,y_test = train_test_split(x,y)
    # scaling train & test features
    
    def scale(train,test):
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(train)
        x_test_scaled = scaler.transform(test)
        return {"train_scaled":x_train_scaled,"test_scaled":x_test_scaled}
    
    x_scaled = scale(x_train,x_test)["train_scaled"]
    x_test_scaled = scale(x_train,x_test)["test_scaled"]
    pipe = Pipeline([("poly",PolynomialFeatures(degree = 2,include_bias = False)),("linreg",LinearRegression())])
    pipe.fit(x_scaled,y_train)
    polyreg = pickle.dumps(pipe)

# Support Vector Machine Regressor 
def svm_regressor(x,y):
    global svreg
    # splitting train and test split 
    x_train,x_test,y_train,y_test = train_test_split(x,y)
    # scaling train & test features
    
    def scale(train,test):
        scaler = StandardScaler()
        x_train_scaled = scaler.fit_transform(train)
        x_test_scaled = scaler.transform(test)
        return {"train_scaled":x_train_scaled,"test_scaled":x_test_scaled}
    
    x_scaled = scale(x_train,x_test)["train_scaled"]
    x_test_scaled = scale(x_train,x_test)["test_scaled"]
    model = SVR (C = 35, gamma = 1, kernel = 'rbf')
    model.fit(x_scaled,y_train)
    svreg = pickle.dumps(model)
    

lasso_regression(emissions.reshape((30,1)),np.array(temperature).reshape((30,1)))
polynomial_regression(emissions.reshape((30,1)),np.array(temperature).reshape((30,1)))
svm_regressor(emissions.reshape((30,1)),np.array(temperature).reshape((30,1)))
lasso = pickle.loads(polyreg)
p = lasso.predict(np.linspace(0,0.9,10).reshape((10,1)))
print(p)
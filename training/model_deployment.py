
from fastapi import FastAPI 
from pydantic import BaseModel
import model_prediction 
import numpy as np

# defining input data format
class Features(BaseModel):
    carbon_dioxyde:float
    
# building FastAPI app
app = FastAPI()
@ app.post("/predict")
def predict(data:Features):
    predicted = model_prediction.linear_regression.predict([[data.carbon_dioxyde]])[0]
    predicted2 = model_prediction.lasso_regression.predict([[data.carbon_dioxyde]])[0]
    predicted3 = model_prediction.poly_regression.predict([[data.carbon_dioxyde]])[0]
    predicted4 = model_prediction.svm.predict([[data.carbon_dioxyde]])[0]
    
    return {"Linear regression prediction":predicted.tolist(),"Lasso regression prediction":predicted2.tolist(),
            "Polynomial regression prediction":predicted3.tolist(),
            "svr prediction":predicted4.tolist()}



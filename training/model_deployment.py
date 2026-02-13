
from fastapi import FastAPI 
from pydantic import BaseModel
import joblib

#model importation
linear_regression = joblib.load("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/models/lr_model.joblib")
lasso_regression  = joblib.load("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/models/lasso_regression.joblib")
poly_regression = joblib.load("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/models/poly_regression.joblib")
svm = joblib.load("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/models/svm_regressor.joblib")
# defining input data format
class Features(BaseModel):
    carbon_dioxyde:float
    
# building FastAPI app
app = FastAPI()
@ app.post("/predict")
def predict(data:Features):
    predicted = linear_regression.predict([[data.carbon_dioxyde]])[0]
    predicted2 = lasso_regression.predict([[data.carbon_dioxyde]])[0]
    predicted3 = poly_regression.predict([[data.carbon_dioxyde]])[0]
    predicted4 = svm.predict([[data.carbon_dioxyde]])[0]
    
    return {"Linear regression prediction":predicted.tolist(),"Lasso regression prediction":predicted2.tolist(),
            "Polynomial regression prediction":predicted3.tolist(),
            "svr prediction":predicted4.tolist()}



import joblib

#model importation
linear_regression = joblib.load("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/models/lr_model.joblib")
lasso_regression  = joblib.load("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/models/lasso_regression.joblib")
poly_regression = joblib.load("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/models/poly_regression.joblib")
svm = joblib.load("/media/dina/f4c07323-3819-4c76-ad53-95f7d45b7ae2/temperature/models/svm_regressor.joblib")



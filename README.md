# A repo about analysins rainfall, temperature and CO2 emission of the analamanga region, with ML models integrated

---

## 📊 Data Analysis
**File:** `analysis.ipynb`

This notebook contains:
- Data cleaning and preprocessing
- Trend analysis of annual temperature, rainfall, and carbon emissions
- Statistical summaries and visualizations
- Interpretation of climate evolution from 1993 to 2022

---

## 🤖 Machine Learning Models
**File:** `model_creation.ipynb`

The following regression models are developed and evaluated:

- Linear Regression
- Lasso Regression
- Polynomial Regression
- Support Vector Regression (SVR)

Each model includes:
- Feature engineering
- Training and validation
- Performance evaluation
- Model persistence for deployment

---

## 🚀 Model Deployment (FastAPI)
**Directory:** `training/model_deployment/`

The trained machine learning models are deployed using **FastAPI**, providing a REST API for prediction.

### 🔧 Python Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```
## ▶️ Start the FastAPI Server

After installing Python dependencies, run the API server:

```bash
uvicorn model_deployment:app --host 127.0.0.1 --port 8000
```
## ▶️ Call the API from terminal 
```bash
curl -X POST http://127.0.0.1:8000/predict \
     -H "Content-Type: application/json" \
     -d '{
           "carbon_emission": 0.45,
         }'

```
## 🚀 Using interface (FastAPI)
Run the file packages.R 
The interface looks like :
<img src="training/screen.png">
A sample dataset can be used :**file** `training/sample_ghg.csv`

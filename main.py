import csv
import pandas as pd
import joblib
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from schema.sentiment import senti
from schema.churn_predict import predict_out
from schema.classs import CustomerIntelligenceRequest, CustomerIntelligenceResponse
from schema.feature_enginering import engineer_features
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

 
@asynccontextmanager
async def lifespan(app: FastAPI):
    customer_db = {}
    models = {}

    # ----------Load CSV----------------
    csv_file_path = "data1/test.csv"
    try:
        raw_df = pd.read_csv(csv_file_path)
        engineered_df = engineer_features(raw_df)
        for _, row in engineered_df.iterrows():
           cust_id = str(row['id'])   
           feature_list = row.drop('id').tolist()
           customer_db[cust_id] = feature_list

        print(f"🚀 Lifespan Startup: Cached {len(customer_db)} fully engineered feature vectors.")
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{csv_file_path}'.")
        
    # ---------- Load ML models ----------
    try:
        models["churn"] = joblib.load("models/churn_model.pkl")
        models["sentiment"] = SentimentIntensityAnalyzer()
        print("🚀 Lifespan Startup: All ML models successfully loaded into memory.")
    except Exception as e:
        print(f"❌ Error loading ML models: {e}")

    app.state.customer_db = customer_db
    app.state.models = models

    yield {"customer_db": customer_db, "models": models}

    # ---------- Shutdown ----------
    print("🛑 Lifespan Shutdown: Cleaning up memory resources.")
    customer_db.clear()
    models.clear()


app = FastAPI(title="Customer Intelligence API", lifespan=lifespan)


@app.post(
    "/predict",
    response_model=CustomerIntelligenceResponse,
    status_code=status.HTTP_200_OK
)
def predict_customer_intelligence(
    request: Request,
    payload: CustomerIntelligenceRequest
):
    
    customer_db = request.app.state.customer_db
    models = request.app.state.models

    customer_id = payload.customer_id
    review_text = payload.customer_review

   
    if customer_id not in customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lookup Failed: Customer ID '{customer_id}' does not exist in records."
        )

    features = customer_db[customer_id]
    x =[features]
    churn_model = models["churn"]
    churn1, risk_label = predict_out(x,churn_model)

    # 5. Sentiment inference
    vader_analyzer = models["sentiment"]
    sentiment_label, compound_score = senti(review_text,vader_analyzer)

    # 6. Response
    return {
        "customer_id": customer_id,
        "churn_probability": churn1,
        "churn_risk_label": risk_label,
        "sentiment_score": compound_score,
        "sentiment_label": sentiment_label
    }
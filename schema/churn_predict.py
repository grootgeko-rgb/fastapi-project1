

def predict_out(X ,churn_model):
    probabilities = churn_model.predict_proba(X)
    churn_prob = float(probabilities[0][1])
    churn1 =round(churn_prob, 2)
    if churn_prob >= 0.7:
        risk_label = "High"
    elif churn_prob >= 0.4:
        risk_label = "Medium"
    else:
        risk_label = "Low"

    return churn1, risk_label
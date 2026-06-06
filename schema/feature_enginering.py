
import pandas as pd



def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1.tenure_group binning
    bins = [0, 12, 35, 62, 72]
    labels = ['Newbie', 'Establishing', 'Stable', 'Veteran']
    df['tenure_group'] = pd.cut(df['tenure'], bins=bins, labels=labels, right=False)

    # 2.calculated_tenure
    df['calculated_tenure'] = df['TotalCharges'] / df['MonthlyCharges']

    # 3.TotalServices
    services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                'TechSupport', 'StreamingTV', 'StreamingMovies']
    df['TotalServices'] = (df[services] == 'Yes').sum(axis=1)

   
    feature_cols = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
        'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'PaymentMethod',
        'MonthlyCharges', 'TotalCharges',
        'tenure_group', 'calculated_tenure', 'TotalServices'
    ]   
    return df[['id'] + feature_cols]


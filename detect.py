from sklearn.ensemble import IsolationForest


# Anomaly detection function using Isolation Forest
def detect_anomalies(data):
    model = IsolationForest(contamination=0.05, random_state=42)
    data['Anomaly'] = model.fit_predict(data[['Price']])
    
    # Mark anomalies (-1 means anomaly in Isolation Forest)
    data['Anomaly'] = data['Anomaly'].apply(lambda x: True if x == -1 else False)
    
    return data
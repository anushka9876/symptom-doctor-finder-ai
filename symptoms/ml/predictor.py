import joblib
import numpy as np
import os

# Absolute path — works from anywhere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

clf        = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'vectorizer.pkl'))

def predict_disease(symptoms_list: list) -> list:
    if not symptoms_list:
        return [{'disease': 'Unknown', 'confidence': 0}]

    symptom_text = ' '.join(symptoms_list)
    X = vectorizer.transform([symptom_text])
    probabilities = clf.predict_proba(X)[0]
    classes = clf.classes_

    top3_idx = np.argsort(probabilities)[::-1][:3]

    results = []
    for idx in top3_idx:
        results.append({
            'disease':    classes[idx],
            'confidence': round(float(probabilities[idx]) * 100, 1)
        })

    return results
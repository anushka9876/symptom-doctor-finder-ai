import os, sys, django
import pandas as pd
import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# ── Load dataset ─────────────────────────────────────────────
df = pd.read_csv('symptoms/ml/dataset.csv')

symptom_cols = [c for c in df.columns if c.startswith('Symptom')]

# Combine all symptom columns into one string per row
def combine_symptoms(row):
    parts = []
    for col in symptom_cols:
        val = str(row[col]).strip()
        if val and val != 'nan':
            parts.append(val.lower().replace('_', ' '))
    return ' '.join(parts)

df['symptom_text'] = df.apply(combine_symptoms, axis=1)

X = df['symptom_text']
y = df['Disease']

# ── Vectorize ────────────────────────────────────────────────
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)

# ── Train ────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

clf = MultinomialNB()
clf.fit(X_train, y_train)

# ── Accuracy ─────────────────────────────────────────────────
preds = clf.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, preds) * 100:.1f}%')

# ── Save model and vectorizer ────────────────────────────────
joblib.dump(clf,        'symptoms/ml/model.pkl')
joblib.dump(vectorizer, 'symptoms/ml/vectorizer.pkl')
print('Model saved to symptoms/ml/model.pkl')
import os
import sys
import django
import pandas as pd
import joblib

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ── Setup Django ─────────────────────────────────────────────
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# ── File Paths ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)

csv_path = os.path.join(BASE_DIR, 'dataset.csv')
model_path = os.path.join(BASE_DIR, 'model.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'vectorizer.pkl')

# ── Load Dataset ─────────────────────────────────────────────
df = pd.read_csv(csv_path)

symptom_cols = [c for c in df.columns if c.startswith('Symptom')]

# ── Combine Symptoms Into One String ─────────────────────────
def combine_symptoms(row):
    parts = []

    for col in symptom_cols:
        val = str(row[col]).strip()

        if val and val != 'nan':
            parts.append(
                val.lower().replace('_', ' ')
            )

    return ' '.join(parts)

df['symptom_text'] = df.apply(combine_symptoms, axis=1)

X = df['symptom_text']
y = df['Disease']

# ── Vectorize Text ───────────────────────────────────────────
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)

# ── Train/Test Split ─────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_vec,
    y,
    test_size=0.2,
    random_state=42
)

# ── Train Model ──────────────────────────────────────────────
clf = MultinomialNB()
clf.fit(X_train, y_train)

# ── Evaluate Accuracy ────────────────────────────────────────
preds = clf.predict(X_test)

accuracy = accuracy_score(y_test, preds) * 100

print(f'Accuracy: {accuracy:.1f}%')

# ── Save Model + Vectorizer ──────────────────────────────────
joblib.dump(clf, model_path)
joblib.dump(vectorizer, vectorizer_path)

print(f'Model saved to: {model_path}')
print(f'Vectorizer saved to: {vectorizer_path}')
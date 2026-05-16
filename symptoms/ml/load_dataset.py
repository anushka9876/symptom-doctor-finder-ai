import os, sys, django, pandas as pd

# Setup Django so we can use models
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from symptoms.models import Disease, Symptom

df = pd.read_csv('symptoms/ml/dataset.csv')

# Get all unique diseases
diseases = df['Disease'].unique()

for disease_name in diseases:
    # Get all symptoms for this disease
    rows = df[df['Disease'] == disease_name]
    symptom_cols = [c for c in df.columns if c.startswith('Symptom')]

    symptom_names = set()
    for _, row in rows.iterrows():
        for col in symptom_cols:
            val = str(row[col]).strip()
            if val and val != 'nan':
                symptom_names.add(val.lower().replace('_', ' '))

    # Create Disease object
    disease_obj, created = Disease.objects.get_or_create(name=disease_name)
    if created:
        print(f'Created disease: {disease_name}')

    # Link symptoms to disease
    for s_name in symptom_names:
        symptom_obj, _ = Symptom.objects.get_or_create(name=s_name)
        disease_obj.symptoms.add(symptom_obj)

print('Done! Diseases in DB:', Disease.objects.count())
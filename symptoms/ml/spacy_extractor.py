import spacy
from symptoms.models import Symptom

nlp = spacy.load('en_core_web_sm')

# Load all known symptoms from DB once
def get_known_symptoms():
    return list(Symptom.objects.values_list('name', flat=True))

def extract_symptoms(text: str) -> list:
    """
    Takes raw user text, returns list of matched symptom names.
    Example: "I have fever and itching" -> ["fever", "itching"]
    """
    known = get_known_symptoms()
    text_lower = text.lower()
    doc = nlp(text_lower)

    found = set()

    # Method 1: direct substring match against known symptoms
    for symptom in known:
        if symptom in text_lower:
            found.add(symptom)

    # Method 2: spaCy lemmatization for word variations
    # "itching" matches "itch", "vomiting" matches "vomit" etc.
    lemmas = {token.lemma_ for token in doc
              if not token.is_stop and not token.is_punct}

    for symptom in known:
        symptom_lemma = nlp(symptom)[0].lemma_
        if symptom_lemma in lemmas:
            found.add(symptom)

    return list(set(symptom.lower() for symptom in found))

print(extract_symptoms("I have fever and itching"))
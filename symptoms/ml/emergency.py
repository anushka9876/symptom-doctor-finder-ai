EMERGENCY_SYMPTOMS = [
    'chest pain',
    'difficulty breathing',
    'breathlessness',
    'loss of consciousness',
    'sudden numbness',
    'severe headache',
    'coughing blood',
    'blood in urine',
    'slurred speech',
    'seizures',
    'high fever',
    'altered sensorium',
]

def check_emergency(symptoms_found: list) -> tuple:
    """
    Returns (is_emergency: bool, message: str)
    """
    found_critical = [s for s in symptoms_found if s in EMERGENCY_SYMPTOMS]

    if found_critical:
        msg = f"⚠️ Critical symptoms detected: {', '.join(found_critical)}. Please go to the nearest emergency room immediately or call 112."
        return True, msg

    return False, ''
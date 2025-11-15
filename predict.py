import pickle

# Load model and vectorizer
with open('model.pkl', 'rb') as f:
    dv, model = pickle.load(f)

def predict(patient_data):
    """
    Predict heart disease probability for a patient.

    Args:
        patient_data: dict with patient features

    Returns:
        float: probability of heart disease (0-1)
    """
    X = dv.transform([patient_data])
    y_pred = model.predict_proba(X)[:, 1]
    return y_pred[0]


if __name__ == '__main__':
    # Example patient data
    patient = {
        'age': 52,
        'sex': 1,
        'cp': 0,
        'trestbps': 125,
        'chol': 212,
        'fbs': 0,
        'restecg': 1,
        'thalach': 168,
        'exang': 0,
        'oldpeak': 1.0,
        'slope': 2,
        'ca': 2,
        'thal': 3
    }

    probability = predict(patient)
    print(f"Heart disease probability: {probability:.3f}")

    if probability >= 0.5:
        print("Prediction: Heart disease detected")
    else:
        print("Prediction: No heart disease")

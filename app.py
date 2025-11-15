from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model at startup
with open('model.pkl', 'rb') as f:
    dv, model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict heart disease probability.

    Expected JSON input:
    {
        "age": 52,
        "sex": 1,
        "cp": 0,
        "trestbps": 125,
        "chol": 212,
        "fbs": 0,
        "restecg": 1,
        "thalach": 168,
        "exang": 0,
        "oldpeak": 1.0,
        "slope": 2,
        "ca": 2,
        "thal": 3
    }
    """
    patient_data = request.get_json()

    X = dv.transform([patient_data])
    y_pred = model.predict_proba(X)[:, 1][0]

    result = {
        'heart_disease_probability': float(y_pred),
        'heart_disease': bool(y_pred >= 0.5)
    }

    return jsonify(result)

@app.route('/', methods=['GET'])
def root():
    return jsonify({'status': 'ok', 'message': 'Heart Disease Prediction API'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

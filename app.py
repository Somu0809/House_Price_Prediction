from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the model, encoder, and scaler
with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('encoder.pkl', 'rb') as encoder_file:
    encoder = pickle.load(encoder_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # Receive JSON input
        area = data['area']
        int_sqft = float(data['int_sqft'])
        dist_mainroad = float(data['dist_mainroad'])
        n_bedroom = int(data['n_bedroom'])
        n_bathroom = int(data['n_bathroom'])
        n_room = int(data['n_room'])
        sale_cond = data['sale_cond']
        park_facil = data['park_facil']

        input_data = np.array([[area, int_sqft, dist_mainroad, n_bedroom, n_bathroom, n_room, sale_cond, park_facil]])
        encoded_features = encoder.transform(input_data[:, [0, 6, 7]])
        scaled_features = scaler.transform(input_data[:, 1:6])
        input_features = np.hstack((scaled_features, encoded_features.toarray()))

        predicted_price = model.predict(input_features)[0]

        return jsonify({'predicted_price': predicted_price})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

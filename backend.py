from flask import Flask, request, jsonify
import numpy as np
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__)

# Dummy training data (replace with your real dataset later)
X = np.array([
    [20, 40, 5, 10],
    [25, 50, 10, 12],
    [30, 60, 15, 14],
    [35, 70, 20, 16]
])

y = np.array([100, 150, 200, 250])

# Train model
model = RandomForestRegressor(n_estimators=5)
model.fit(X, y)

# Home route
@app.route('/')
def home():
    return "Energy Forecasting Backend Running"

# Prediction API
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    temp = data['temperature']
    humidity = data['humidity']
    occupancy = data['occupancy']
    hour = data['hour']
    
    input_data = np.array([[temp, humidity, occupancy, hour]])
    prediction = model.predict(input_data)
    
    return jsonify({
        "predicted_energy": float(prediction[0])
    })

if __name__ == '__main__':
    app.run(debug=True)

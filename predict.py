import numpy as np

def predict_energy(model, scaler, temp, occ, hour, hum):
    data = np.array([[temp, occ, hour, hum]])
    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)

    return prediction[0]

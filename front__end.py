import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# Title
st.title("Smart Building Energy Forecasting")

# Inputs
temp = st.slider("Temperature (°C)", 0, 50, 25)
humidity = st.slider("Humidity (%)", 0, 100, 50)
occupancy = st.slider("Occupancy", 0, 100, 10)
hour = st.slider("Hour of Day", 0, 23, 12)

# Dummy dataset (for demo)
X = np.array([[20, 40, 5, 10],
              [25, 50, 10, 12],
              [30, 60, 15, 14],
              [35, 70, 20, 16]])

y = np.array([100, 150, 200, 250])

# Model (Random Forest)
model = RandomForestRegressor(n_estimators=5)
model.fit(X, y)

# Prediction
if st.button("Predict Energy"):
    input_data = np.array([[temp, humidity, occupancy, hour]])
    prediction = model.predict(input_data)

    st.success(f"Predicted Energy Consumption: {prediction[0]:.2f} kW")

    # Plot
    actual = y
    predicted = model.predict(X)

    plt.figure()
    plt.plot(actual, label="Actual")
    plt.plot(predicted, label="Predicted")
    plt.legend()
    plt.title("Energy Prediction Graph")

    st.pyplot(plt)

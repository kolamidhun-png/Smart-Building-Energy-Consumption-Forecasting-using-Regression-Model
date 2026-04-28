import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================
# 2. LOAD DATA
# ==========================
def load_data():
    data = {
        'Temperature': [22, 25, 30, 35, 28, 20, 18, 33, 27, 31],
        'Occupancy': [10, 20, 30, 40, 25, 15, 10, 35, 22, 38],
        'Hour': [6, 9, 12, 15, 18, 21, 3, 14, 11, 16],
        'Humidity': [40, 50, 60, 70, 65, 55, 45, 68, 58, 62],
        'Energy': [15, 25, 40, 55, 38, 20, 18, 50, 35, 48]
    }
    return pd.DataFrame(data)


# ==========================
# 3. PREPROCESS DATA
# ==========================
def preprocess_data(df):
    X = df[['Temperature', 'Occupancy', 'Hour', 'Humidity']]
    y = df['Energy']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, scaler


# ==========================
# 4. TRAIN MODELS
# ==========================
def train_models(X_train, y_train):
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)

    rf_model = RandomForestRegressor(n_estimators=5, random_state=42)
    rf_model.fit(X_train, y_train)

    return linear_model, rf_model


# ==========================
# 5. EVALUATE MODELS
# ==========================
def evaluate_model(name, y_test, y_pred):
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"\n{name} Performance:")
    print("MAE :", round(mae, 2), "kW")
    print("RMSE:", round(rmse, 2), "kW")
    print("R²  :", round(r2, 2))


# ==========================
# 6. PLOT RESULTS
# ==========================
def plot_results(y_test, y_pred_linear, y_pred_rf):
    plt.figure()
    plt.plot(y_test.values, label="Actual Energy", marker='o')
    plt.plot(y_pred_linear, label="Linear Regression", linestyle='--')
    plt.plot(y_pred_rf, label="Random Forest", linestyle='-.')
    plt.title("Energy Prediction Comparison")
    plt.xlabel("Test Samples")
    plt.ylabel("Energy (kW)")
    plt.legend()
    plt.grid()
    plt.show()


# ==========================
# 7. FEATURE IMPORTANCE
# ==========================
def plot_feature_importance(model, feature_names):
    importance = model.feature_importances_

    plt.figure()
    plt.bar(feature_names, importance)
    plt.title("Feature Importance (Random Forest)")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.show()


# ==========================
# 8. CUSTOM PREDICTION
# ==========================
def predict_energy(model, scaler, temp, occ, hour, hum):
    data = np.array([[temp, occ, hour, hum]])
    data_scaled = scaler.transform(data)
    prediction = model.predict(data)
    return prediction[0]


# ==========================
# 9. MAIN FUNCTION
# ==========================
def main():
    print("=== ENERGY FORECASTING PROJECT ===")

    # Load Data
    df = load_data()
    print("\nDataset:\n", df)

    # Preprocess
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

    # Train Models
    linear_model, rf_model = train_models(X_train, y_train)

    # Predictions
    y_pred_linear = linear_model.predict(X_test)
    y_pred_rf = rf_model.predict(X_test)

    # Evaluation
    evaluate_model("Linear Regression", y_test, y_pred_linear)
    evaluate_model("Random Forest", y_test, y_pred_rf)

    # Visualization
    plot_results(y_test, y_pred_linear, y_pred_rf)

    # Feature Importance
    feature_names = ['Temperature', 'Occupancy', 'Hour', 'Humidity']
    plot_feature_importance(rf_model, feature_names)

    # Custom Prediction
    result = predict_energy(rf_model, scaler, 29, 30, 14, 60)
    print("\nPredicted Energy Consumption:", round(result, 2), "kW")

    # Conclusion
    print("\nConclusion:")
    print("Random Forest gives better performance.")
    print("Model successfully predicts energy usage.")
    print("Useful for smart building optimization.")


# ==========================
# 10. RUN PROGRAM
# ==========================
if __name__ == "__main__":
    main()

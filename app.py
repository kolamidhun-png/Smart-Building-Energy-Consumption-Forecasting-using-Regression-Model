import matplotlib.pyplot as plt

from read import load_data
from preprocess import preprocess_data
from model import train_models
from evaluate import evaluate
from predict import predict_energy

# Step 1: Load Data
df = load_data()
print("Dataset:\n", df)

# Step 2: Preprocess
X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

# Step 3: Train Models
linear_model, rf_model = train_models(X_train, y_train)

# Step 4: Predictions
y_pred_linear = linear_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)

# Step 5: Evaluation
evaluate("Linear Regression", y_test, y_pred_linear)
evaluate("Random Forest", y_test, y_pred_rf)

# Step 6: Plot
plt.figure()
plt.plot(y_test.values, label="Actual")
plt.plot(y_pred_linear, label="Linear")
plt.plot(y_pred_rf, label="Random Forest")
plt.legend()
plt.title("Energy Prediction")
plt.show()

# Step 7: Custom Prediction
result = predict_energy(rf_model, scaler, 29, 30, 14, 60)
print("\nPredicted Energy:", round(result, 2), "kW")

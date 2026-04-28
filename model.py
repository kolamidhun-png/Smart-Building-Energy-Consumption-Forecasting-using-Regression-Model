from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def train_models(X_train, y_train):
    linear = LinearRegression()
    linear.fit(X_train, y_train)

    rf = RandomForestRegressor(n_estimators=5, random_state=42)
    rf.fit(X_train, y_train)

    return linear, rf

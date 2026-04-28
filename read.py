import pandas as pd

def load_data():
    data = {
        'Temperature': [22, 25, 30, 35, 28, 20, 18, 33, 27, 31],
        'Occupancy': [10, 20, 30, 40, 25, 15, 10, 35, 22, 38],
        'Hour': [6, 9, 12, 15, 18, 21, 3, 14, 11, 16],
        'Humidity': [40, 50, 60, 70, 65, 55, 45, 68, 58, 62],
        'Energy': [15, 25, 40, 55, 38, 20, 18, 50, 35, 48]
    }
    return pd.DataFrame(data)

from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle

df = pd.read_csv('processed_data.csv')
X = df[['humidity', 'wind_speed']]  # Example features
y = df['temperature']

model = LinearRegression()
model.fit(X, y)

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
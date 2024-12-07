import mlflow
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from mlflow.models import infer_signature


# Setup MLflow connection and experiment
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Linear Regression Experiment")
logged_model = 'mlflow-artifacts:/647844585667991767/057865c7358146b790bb18ffba1d1839/artifacts/linear-regression-model'


# Load the model
loaded_model = mlflow.sklearn.load_model(logged_model)

# Load preprocessed data
file_path = 'D:\\MLOps\\MLOP-Activity-7\\processed_data.csv'
df = pd.read_csv(file_path)

# Select features and target
X = df[["humidity", "wind_speed"]].values
y = df["temperature"].values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Use the loaded model to predict
predictions = loaded_model.predict(X_test)

# Show the predictions
results_df = pd.DataFrame({
    "Actual": y_test,
    "Predicted": predictions
})

print("Prediction Results:")
print(results_df)

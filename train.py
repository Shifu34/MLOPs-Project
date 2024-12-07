import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature


def train_and_log_model(X_train, y_train, X_test, y_test):
    """Train the model, evaluate, and log it with MLflow."""
    # Start MLflow run
    with mlflow.start_run():
        # Initialize and train Linear Regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate metrics
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Log metrics
        mlflow.log_metric("mean_squared_error", mse)
        mlflow.log_metric("mean_absolute_error", mae)
        mlflow.log_metric("r2_score", r2)

        # Infer the signature of the model for input/output validation
        signature = infer_signature(X_train, model.predict(X_train))

        # Log the trained model with MLflow
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="linear-regression-model",
            signature=signature,
            input_example=X_train[0].reshape(1, -1),
        )

        print(f"Model logged to MLflow with run ID: {mlflow.active_run().info.run_uuid}")
        return model


def main():
    # Setup MLflow connection and experiment
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Linear Regression Experiment")
    
    # Load processed data
    file_path = 'D:\\MLOps\\MLOP-Activity-7\\processed_data.csv'
    df = pd.read_csv(file_path)
    
    # Select features and target
    X = df[["humidity", "wind_speed"]].values
    y = df["temperature"].values

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model and log it with MLflow
    model = train_and_log_model(X_train, y_train, X_test, y_test)

    print("Model evaluation completed.")


if __name__ == "__main__":
    main()

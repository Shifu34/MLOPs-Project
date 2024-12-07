import datetime
import os
import pandas as pd
import requests
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
from airflow import DAG
from airflow.operators.python import PythonOperator

# Define the DVC remote storage path (local or remote)
DVC_REMOTE = "D:\\MLOps\\dvc-data"
LOCAL_STORAGE_PATH = "D:\\MLOps\\MLOP-Activity-7"

# Define the API URL for fetching weather data
API_URL = "http://api.openweathermap.org/data/2.5/forecast"
API_KEY = "01c705b3591b2cfc2fb27de51c0b5ad7"  # Replace with your actual API key

# 1. Fetch Weather Data
def fetch_weather_data():
    params = {
        "q": "London,GB",  # Example: You can change the city here
        "appid": API_KEY,
        "units": "metric",  # Temperature in Celsius
        "cnt": 100  # Number of data points (can adjust this based on desired interval)
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    # Extract the relevant data (date, temperature, humidity, etc.)
    weather_data = []
    for entry in data['list']:
        weather_data.append({
            "date_time": entry["dt_txt"],
            "temperature": entry["main"]["temp"],
            "humidity": entry["main"]["humidity"],
            "wind_speed": entry["wind"]["speed"],
            "condition": entry["weather"][0]["description"]
        })
    
    # Save to CSV file
    df = pd.DataFrame(weather_data)
    df.to_csv(f"{LOCAL_STORAGE_PATH}\\raw_weather_data.csv", index=False)

    # Use DVC to track the raw data
    os.system(f"dvc add {LOCAL_STORAGE_PATH}\\raw_weather_data.csv")
    os.system(f"git add {LOCAL_STORAGE_PATH}\\raw_weather_data.csv.dvc")
    os.system("git commit -m 'Add raw weather data'")
    os.system("dvc push")

# 2. Preprocess Data
def preprocess_data():
    # Load the raw data
    df = pd.read_csv(f"{LOCAL_STORAGE_PATH}\\raw_weather_data.csv")

    # Handle missing values (fill with mean)
    df['temperature'] = df['temperature'].fillna(df['temperature'].mean())
    df['humidity'] = df['humidity'].fillna(df['humidity'].mean())
    df['wind_speed'] = df['wind_speed'].fillna(df['wind_speed'].mean())
    df['condition'] = df['condition'].fillna(df['condition'].mode()[0])

    # Standardize numerical data (temperature, humidity, wind_speed)
    scaler = StandardScaler()
    df[['temperature', 'humidity', 'wind_speed']] = scaler.fit_transform(df[['temperature', 'humidity', 'wind_speed']])

    # Encode categorical data (weather condition)
    df['condition_encoded'] = df['condition'].astype('category').cat.codes

    # Save preprocessed data to a new CSV
    df.to_csv(f"{LOCAL_STORAGE_PATH}\\processed_weather_data.csv", index=False)

    # Use DVC to track the processed data
    os.system(f"dvc add {LOCAL_STORAGE_PATH}\\processed_weather_data.csv")
    os.system(f"git add {LOCAL_STORAGE_PATH}\\processed_weather_data.csv.dvc")
    os.system("git commit -m 'Add preprocessed weather data'")
    os.system("dvc push")

# 3. Train Machine Learning Model
def train_model():
    # Load the preprocessed data
    df = pd.read_csv(f"{LOCAL_STORAGE_PATH}\\processed_weather_data.csv")

    # Prepare the features and target variable
    X = df[['humidity', 'wind_speed', 'condition_encoded']]
    y = df['temperature']  # Example: predicting temperature

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a simple linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the trained model as a pickle file
    with open(f"{LOCAL_STORAGE_PATH}\\model.pkl", "wb") as f:
        pickle.dump(model, f)

    # Use DVC to track the model
    os.system(f"dvc add {LOCAL_STORAGE_PATH}\\model.pkl")
    os.system(f"git add {LOCAL_STORAGE_PATH}\\model.pkl.dvc")
    os.system("git commit -m 'Add trained model'")
    os.system("dvc push")

# Define the Airflow DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime(2024, 11, 26),
    'retries': 1,
}

dag = DAG(
    'weather_data_pipeline',
    default_args=default_args,
    description='A pipeline to fetch, preprocess weather data, and train a model',
    schedule_interval=datetime.timedelta(days=1),  # Run once a day
)

# Define the tasks
fetch_data_task = PythonOperator(
    task_id='fetch_weather_data',
    python_callable=fetch_weather_data,
    dag=dag,
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

# Set the task dependencies (order of execution)
fetch_data_task >> preprocess_data_task >> train_model_task

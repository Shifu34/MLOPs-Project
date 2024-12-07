import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

# Load the raw data
df = pd.read_csv('raw_data.csv')

# 1. Handle Missing Values
# Check for missing values
print("Missing values in each column:")
print(df.isnull().sum())

# Option to fill missing values (with mean or median for numerical columns)
df['temperature'] = df['temperature'].fillna(df['temperature'].mean())
df['humidity'] = df['humidity'].fillna(df['humidity'].mean())
df['wind_speed'] = df['wind_speed'].fillna(df['wind_speed'].mean())
df['condition'] = df['condition'].fillna(df['condition'].mode()[0])  # Filling categorical missing values with mode

# 2. Normalize or Standardize Numerical Data (temperature, humidity, wind_speed)
# Standardizing numerical data (using StandardScaler)
scaler = StandardScaler()
df[['temperature', 'humidity', 'wind_speed']] = scaler.fit_transform(df[['temperature', 'humidity', 'wind_speed']])

# 3. Convert 'date_time' column to datetime format
df['date_time'] = pd.to_datetime(df['date_time'])

# 4. Encode Categorical Data ('condition')
# Option 1: Label Encoding (for machine learning purposes)
label_encoder = LabelEncoder()
df['condition_encoded'] = label_encoder.fit_transform(df['condition'])

# Option 2: One-Hot Encoding (if you want dummy variables for categorical columns)
# df = pd.get_dummies(df, columns=['condition'], drop_first=True)

# 5. Save the Preprocessed Data to a new CSV file
df.to_csv('processed_data.csv', index=False)

# Print the preprocessed data for review
print(df.head())

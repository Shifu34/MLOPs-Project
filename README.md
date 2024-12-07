
# MLOps Activity: Data Engineering Pipeline

This repository demonstrates the construction of a data engineering pipeline using Airflow and DVC (Data Version Control). The pipeline collects live weather data, preprocesses it, trains a machine learning model, and tracks datasets and models using DVC.

---

## Objective

The aim of this project is to provide practical experience in:
- Using DVC for managing datasets and machine learning models.
- Implementing data versioning and model versioning using DVC.
- Streamlining workflows using Apache Airflow.

---

## Steps

### 1. Setting Up the Environment and Data Collection

#### Project Setup
- Initialized a Git repository.
- Initialized DVC (`dvc init`).
- Configured remote storage for DVC (e.g., Google Drive or AWS S3).

#### Data Collection
- Collected weather data from an API (e.g., OpenWeatherMap API).
- Gathered the following fields for 5 days of weather data:
  - Temperature
  - Humidity
  - Wind Speed
  - Weather Condition
  - Date and Time
- Saved the raw data in `raw_data.csv` and tracked it using DVC.

### 2. Data Preprocessing and Workflow Automation

#### Data Preprocessing
- Handled missing values.
- Normalized numerical fields (temperature and wind speed).
- Saved preprocessed data as `processed_data.csv` and tracked it with DVC.

#### Workflow Automation
- Created an Airflow pipeline with two tasks:
  - **Data Collection**: Fetch and save raw weather data.
  - **Data Preprocessing**: Clean and preprocess the raw data.
- Configured the pipeline for end-to-end automation.

### 3. Model Training

#### Training
- Trained a linear regression model to predict temperature using other features.
- Saved the trained model as `model.pkl`.

#### Version Control
- Tracked the trained model file with DVC.

#### DVC Pipeline
- Defined a DVC pipeline with the following stages:
  - Data Collection
  - Data Preprocessing
  - Model Training

---

## How to Run the Project

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up DVC Remote**:
   Configure your remote storage for DVC:
   ```bash
   dvc remote add -d <remote-name> <remote-url>
   ```

4. **Run Airflow**:
   - Initialize Airflow:
     ```bash
     airflow db init
     ```
   - Start the scheduler and webserver:
     ```bash
     airflow scheduler &
     airflow webserver
     ```
   - Trigger the DAG from the Airflow UI.

5. **Execute DVC Pipeline**:
   ```bash
   dvc repro
   ```

---

## Project Structure

```
|-- raw_data.csv         # Raw weather data
|-- processed_data.csv   # Preprocessed weather data
|-- model.pkl            # Trained linear regression model
|-- dvc.yaml             # DVC pipeline definition
|-- airflow/             # Airflow DAGs and configurations
|-- README.md            # Project documentation
|-- airflow/requirements.txt     # Python dependencies
```

---

## Dependencies

- Python (3.7+)
- DVC
- Apache Airflow
- scikit-learn
- Pandas
- NumPy

Install dependencies with:
```bash
pip install -r requirements.txt
```

---

## Contributors

This project was completed by a group of 3 contributors as part of a learning activity.

---

## License

This project is licensed under the MIT License.

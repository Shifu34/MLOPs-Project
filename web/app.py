from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the pickled model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def index():
    """Render the main interface."""
    return render_template('index.html', temprature=None)

@app.route('/process', methods=['POST'])
def process_input():
    """Handle form input and make predictions."""
    try:
        # Get wind speed and humidity from the form
        wind_speed = float(request.form['wind'])
        humidity = float(request.form['humidity'])

        # Prepare data for prediction
        input_data = np.array([[humidity, wind_speed]])

        # Predict temperature using the loaded model
        prediction = model.predict(input_data)[0]

        prediction = abs(prediction)

        # Render the result on the front-end
        return render_template('index.html', temprature=round(prediction, 2))
    except Exception as e:
        # Handle exceptions and display the error message
        return render_template('index.html', temprature=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
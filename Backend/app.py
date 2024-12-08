from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pickle
import numpy as np
import secrets
from mlflow.models import infer_signature
import mlflow
app = Flask(
    __name__,
    template_folder='/app/templates',  # Adjusted to the container path
    static_folder='/app/static'        # Adjusted to the container path
)

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Setup MLflow connection and experiment
mlflow.set_tracking_uri("http://host.docker.internal:5000")
mlflow.set_experiment("Linear Regression Experiment")
logged_model = 'mlflow-artifacts:/647844585667991767/057865c7358146b790bb18ffba1d1839/artifacts/linear-regression-model'


# Load the model
model = mlflow.sklearn.load_model(logged_model)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('predict'))
        flash('Login failed. Check username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    return render_template('predict.html', temprature=None)

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
        return render_template('predict.html', temprature=round(prediction, 2))
    except Exception as e:
        # Handle exceptions and display the error message
        return render_template('predict.html', temprature=f"Error: {str(e)}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables within the application context
    app.run(host="0.0.0.0", port=8080, debug=True)

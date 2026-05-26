from flask import Flask, request, jsonify, render_template, url_for
import tensorflow as tf
import numpy as np
import pickle
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import io
import os
from flask import Flask, request, render_template
import contextlib
import joblib
import re
import sqlite3
import pandas as pd
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from create_database import setup_database
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.vgg16 import preprocess_input
from utils import login_required, set_session
from flask import (
    Flask, render_template, 
    request, session, redirect
)

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('models/food_classifier.h5')

database = "users.db"
setup_database(name=database)

app.secret_key = 'xpSm7p5bgJY8rNoBjGWiz5yjxM-NEBlW6SIBI62OkLc='

# Load class labels
with open('models/class_labels.pkl', 'rb') as f:
    class_labels = pickle.load(f)

# Calorie dictionary
calorie_dict = {
    'Apple': 52,       # Calories per 100g
    'Banana': 89,
    'Peanuts': 567,
    'Pizza': 266,
    # Add more classes as needed
}

@app.route('/')
def index():
    return render_template('index.html')


# Homepage route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Set data to variables
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Attempt to query associated user data
    query = 'select username, password, email from users where username = :username'

    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            account = conn.execute(query, {'username': username}).fetchone()

    if not account: 
        return render_template('login.html', error='Username does not exist')

    # Verify password
    try:
        ph = PasswordHasher()
        ph.verify(account[1], password)
    except VerifyMismatchError:
        return render_template('login.html', error='Incorrect password')

    # Check if password hash needs to be updated
    if ph.check_needs_rehash(account[1]):
        query = 'update set password = :password where username = :username'
        params = {'password': ph.hash(password), 'username': account[0]}

        with contextlib.closing(sqlite3.connect(database)) as conn:
            with conn:
                conn.execute(query, params)

    # Set cookie for user session
    set_session(
        username=account[0], 
        email=account[2], 
        remember_me='remember-me' in request.form
    )
    
    return redirect('/predict_page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    # Store data to variables 
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    username = request.form.get('username')
    email = request.form.get('email')

    # Verify data
    if len(password) < 8:
        return render_template('register.html', error='Your password must be 8 or more characters')
    if password != confirm_password:
        return render_template('register.html', error='Passwords do not match')
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        return render_template('register.html', error='Username must only be letters and numbers')
    if not 3 < len(username) < 26:
        return render_template('register.html', error='Username must be between 4 and 25 characters')

    query = 'select username from users where username = :username;'
    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            result = conn.execute(query, {'username': username}).fetchone()
    if result:
        return render_template('register.html', error='Username already exists')

    # Create password hash
    pw = PasswordHasher()
    hashed_password = pw.hash(password)

    query = 'insert into users(username, password, email) values (:username, :password, :email);'
    params = {
        'username': username,
        'password': hashed_password,
        'email': email
    }

    with contextlib.closing(sqlite3.connect(database)) as conn:
        with conn:
            result = conn.execute(query, params)

    # We can log the user in right away since no email verification
    set_session( username=username, email=email)
    return redirect('/')

@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')


@app.route('/predict_page', methods=['POST'])
def predict_food_and_calories():
    try:
        # Get image and weight from the request
        if 'image' not in request.files:
            return "No image uploaded", 400

        image_file = request.files['image']
        weight = request.form.get('weight')

        if not weight:
            return "No weight provided", 400

        # Read the image file as bytes
        img_bytes = image_file.read()
        img = load_img(io.BytesIO(img_bytes), target_size=(150, 150))  # Resize image to model's input size
        img_array = img_to_array(img) / 255.0  # Normalize the image
        img_array = np.expand_dims(img_array, axis=0)

        # Predict the food category
        predictions = model.predict(img_array)
        predicted_class_idx = np.argmax(predictions, axis=1)[0]
        predicted_class = class_labels[predicted_class_idx]

        # Calculate calories
        weight = float(weight)  # Convert weight to float
        if predicted_class in calorie_dict:
            calories = calorie_dict[predicted_class] * (weight / 100.0)
        else:
            return f"No calorie data for {predicted_class}", 400

        # Redirect to result page with prediction data
        return redirect(url_for('result', food=predicted_class, calories=round(calories, 2)))

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/result')
def result():
    # Get food and calorie values from URL parameters
    food = request.args.get('food', 'Unknown')
    calories = request.args.get('calories', '0')

    return render_template('result.html', food=food, calories=calories)

if __name__ == '__main__':
    app.run(debug=True)

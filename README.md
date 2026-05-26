# 🍽️ Food Calorie Prediction System

A Machine Learning and Deep Learning based web application that predicts the calorie content of food items from uploaded food images using a Convolutional Neural Network (CNN).

---

# 🚀 Project Overview

The Food Calorie Prediction System is designed to help users estimate food calories by simply uploading an image of a food item. The system uses a trained CNN model for image classification and calorie estimation.

This project combines:

* Machine Learning
* Deep Learning
* Flask Web Development
* Database Integration
* Image Processing

---

# 🎯 Features

✅ Food image upload
✅ Food item prediction using CNN
✅ Calorie estimation
✅ User Registration & Login
✅ Prediction history storage
✅ Responsive web interface
✅ SQLite database integration

---

# 🛠️ Technologies Used

## 💻 Programming Language

* Python

## 🤖 Machine Learning / Deep Learning

* TensorFlow
* Keras
* CNN (Convolutional Neural Network)
* NumPy
* OpenCV
* Scikit-learn
* Pandas

## 🌐 Web Development

* Flask
* HTML
* CSS
* JavaScript
* Bootstrap

## 🗄️ Database

* SQLite3

---

# 📂 Project Structure

```bash
food_calorie_prediction/
│
├── app.py                     # Main Flask application
├── train_model.py             # Model training script
├── create_database.py         # Database setup
├── utils.py                   # Helper functions
├── requirements.txt           # Required libraries
├── users.db                   # SQLite database
│
├── dataset/                   # Food image dataset
├── models/                    # Trained model files
├── static/                    # CSS, JS, images
├── templates/                 # HTML pages
├── uploads/                   # Uploaded images
│
└── README.md
```

---

# ⚙️ How the Project Works

## 1️⃣ Dataset Collection

* Food images are collected and organized into categories.
* Example:

  * Pizza
  * Burger
  * Dosa
  * Idli
  * Biryani

---

## 2️⃣ Model Training

* Images are preprocessed:

  * Resizing
  * Normalization
* CNN model is trained using TensorFlow/Keras.
* Trained model is saved in the `models/` folder.

---

## 3️⃣ Web Application

* User uploads a food image through the Flask web app.
* Backend loads the trained model.
* Image is processed and passed to the model.
* Predicted food name and calorie value are displayed.

---

## 4️⃣ Database Integration

* User login and registration data are stored in SQLite.
* Prediction history can also be stored.

---

# 🔥 CNN Model Workflow

```text
Input Image
     ↓
Image Preprocessing
     ↓
CNN Feature Extraction
     ↓
Food Classification
     ↓
Calorie Prediction
     ↓
Display Result
```

---

# 📦 Installation

## Step 1: Clone Repository

```bash
git clone https://github.com/your-username/food-calorie-prediction.git
```

---

## Step 2: Navigate to Project Folder

```bash
cd food-calorie-prediction
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Create Database

```bash
python create_database.py
```

---

## Step 5: Run Application

```bash
python app.py
```

---

# 🌐 Run in Browser

```bash
http://127.0.0.1:5000/
```

---

# 📸 Screenshots

## Home Page

* Upload food image
* User authentication

## Prediction Page

* Displays:

  * Food name
  * Calorie value
  * Uploaded image

---

# 🧠 Machine Learning Concepts Used

* Convolutional Neural Network (CNN)
* Image Classification
* Feature Extraction
* Data Augmentation
* Model Training & Prediction

---

# 🚧 Challenges Faced

* Dataset imbalance
* Overfitting
* Image preprocessing issues
* Flask model integration
* Improving prediction accuracy

---

# 🔮 Future Enhancements

✅ Multi-food detection
✅ Cloud deployment (AWS/GCP)
✅ Mobile application
✅ Nutrition breakdown (Protein, Fat, Carbs)
✅ Real-time camera detection

---

# 👨‍💻 Author

**Surendhar**
Computer Science and Engineering Graduate
Java Full Stack & Machine Learning Enthusiast

---

# 📄 License

This project is developed for educational and learning purposes.

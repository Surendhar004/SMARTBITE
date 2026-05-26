import os
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define the calorie dictionary
calorie_dict = {
    'Apple': 52,       # Calories per 100g
    'Banana': 89,
    'Peanuts': 567,
    'Pizza': 266,
    # Add more classes here
}

# Define paths for dataset
train_dir = 'dataset/train'  # Training images directory
test_dir = 'dataset/test'    # Test images directory

# Define image dimensions
img_width, img_height = 150, 150

# Data augmentation for training and testing
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1.0 / 255)

# Load training data
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='categorical'
)

# Load testing data
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='categorical'
)

# Build the model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(train_generator.class_indices), activation='softmax')
])

# Compile the model
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Train the model
model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=10,
    validation_data=test_generator,
    validation_steps=len(test_generator)
)

# Create a directory for saving the model and class labels
os.makedirs('models', exist_ok=True)

# Save the trained model
model.save('models/food_classifier.h5')

# Create a mapping of class indices to class labels
class_indices = {v: k for k, v in train_generator.class_indices.items()}

# Save class labels to a file
with open('models/class_labels.pkl', 'wb') as f:
    pickle.dump(class_indices, f)

print("Training completed and model saved!")

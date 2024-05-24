import json
import numpy as np
import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing
import traceback
import sys

try:
    # Load data
    with open('bot/data/intents.json') as file:
        data = json.load(file)

    # Extract patterns and labels
    intents = data['intents']

    patterns = []
    labels = []

    for intent in intents:
        for pattern in intent['patterns']:
            patterns.append(pattern)
            labels.append(intent['tag'])

    # Tokenize patterns
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(patterns)

    # Encode labels
    label_encoder = preprocessing.LabelEncoder()
    y = label_encoder.fit_transform(labels)

    # Define and train model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, input_shape=(X.shape[1],), activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(len(np.unique(y)), activation='softmax')
    ])

    model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(X.toarray(), y, epochs=200, batch_size=5)

    # Save model
    model.save('bot/models/chatbot_model.h5')

except UnicodeEncodeError:
    print("An error occurred during training: [UnicodeEncodeError - error message cannot be displayed]")




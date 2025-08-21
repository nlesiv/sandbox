
import numpy as np
from sklearn.datasets import load_iris
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
iris = load_iris()

# print("Iris", iris)
# print(iris.DESCR)

X = iris.data
y = iris.target

# Class 0 -> [1,0,0]
# Class 1 -> [0,1,0]
# Class 2 -> [0,0,1]
# Hot encoding
y = to_categorical(y)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.33, random_state=42)

scaler_object = MinMaxScaler()
scaler_object.fit(X_train)
scaled_X_train = scaler_object.transform(X_train)
scaled_X_test = scaler_object.transform(X_test)

from keras.models import Sequential
from keras.layers import Dense

model = Sequential()
model.add(Dense(8, input_dim=4, activation='relu'))
model.add(Dense(8, input_dim=4, activation='relu'))
model.add(Dense(3, activation='softmax')) # [0.2, 0.3, 0.5]
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())

model.fit(scaled_X_train, y_train, epochs=150, verbose=2)

result = model.predict(scaled_X_test)
predictions = result.argmax(axis=-1)
print("predictions:", predictions)

y_test.argmax(axis=1)

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print("Confusion Matrix:\n", confusion_matrix(y_test.argmax(axis=1), predictions))
print("Classification Report:\n", classification_report(y_test.argmax(axis=1), predictions))
print("Accuracy Score:", accuracy_score(y_test.argmax(axis=1), predictions))
print("Model Evaluation:", model.evaluate(scaled_X_test, y_test, verbose=0))

# Save the model
model.save('myfirstmodel.h5')

new_model = load_model('myfirstmodel.h5')

print("Loaded Model Prediction", new_model.predict(scaled_X_test))

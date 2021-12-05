# Import tensorflow, and tensorflow_datasets
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Create the train set and test set
data_train = pd.read_csv('train.csv')
data_test = pd.read_csv('test.csv')

# Create de labels
class_names = ['Manzana', 'Galleta', 'Shampoe', 'Sapolio', 'Pepino', 'Helado', '---', '---', '---', '---']

# Create the train set and its labels
x_train = data_train.copy()
label = x_train['label']
x_train.drop(['label'], axis = 1, inplace = True)
x_train.head()

# Create the model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(units=32, activation='sigmoid', input_shape=(784,)))
model.add(tf.keras.layers.Dense(units=64, activation='sigmoid'))
model.add(tf.keras.layers.Dense(units=1))

# Print the model summary
model.summary()

# Compile the model
model.compile(optimizer='sgd', loss='mean_squared_error', metrics=['mean_squared_error'])

# Fit the model
train = model.fit(x_train, label.values.reshape(42000,1),batch_size=32, epochs=500,validation_split=.3)

# Plot the training and validation loss
plt.plot(train.history['loss'])
plt.plot(train.history['mean_squared_error'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['training', 'validation'], loc='best')
plt.show()

# Make predictions
pred = model.predict(data_test)
pred = pred.round(0)
print(pred)

# Predic only one image
test = data_test.copy()
test = tf.convert_to_tensor(test.values)
test = np.array(test[1])
test = test.reshape(784,1)
print(test.shape)
y = model.predict(np.expand_dims(np.array(test, dtype=np.float32), 0))
print(y)

# Save the model
model.save('fsmodel.h5')
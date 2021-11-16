# Import tensorflow, and tensorflow_datasets
import math
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds

# Import the Fashion MNIST dataset
dataset, metadata = tfds.load('fashion_mnist', as_supervised=True, with_info=True)
trainset, testset = dataset["train"], dataset["test"]

# Creta the list of the labels
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# Add the data to the train and test sets
num_train_examples = metadata.splits['train'].num_examples
num_test_examples = metadata.splits['test'].num_examples
print("Number of training examples: {}".format(num_train_examples))
print("Number of test examples:     {}".format(num_test_examples))

# Define the function to preprocess the data
def normalize(image, label):
    image = tf.cast(image, tf.float32)
    image /= 255
    return image, label

# Create the train and test datasets
train_dataset = trainset.map(normalize)
test_dataset = testset.map(normalize)

# Create the model
# model = tf.keras.Sequential([
#     tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
#     tf.keras.layers.MaxPooling2D(2,2),
#     tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
#     tf.keras.layers.MaxPooling2D(2,2),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(10, activation='softmax')
# ])
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(100, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Create the batch size
batch_size = 32
train_dataset = train_dataset.repeat().shuffle(num_train_examples).batch(batch_size)
test_dataset = test_dataset.repeat().shuffle(num_test_examples).batch(batch_size)

# Fit the model
model.fit(train_dataset, epochs=10, steps_per_epoch=math.ceil(num_train_examples/batch_size))

# Evaluate the model
test_loss, test_accuracy = model.evaluate(test_dataset, steps=math.ceil(num_test_examples/batch_size))
print('Lost: ', test_loss)
print('Accuracy on test dataset:', test_accuracy)

# Export the model
# model.save('fast_store.h5')

# Test the model
for test_images, test_labels in test_dataset.take(1):
    test_images = test_images.numpy()
    test_labels = test_labels.numpy()
    predictions = model.predict(test_images)
    print(predictions[0])
    print(test_labels[0])
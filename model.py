# Import tensorflow, and tensorflow_datasets
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import confusion_matrix
from keras.utils.np_utils import to_categorical

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from tensorflow.keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

def init_model():
    ###  Model Definition
    model = Sequential()
    model.add(Conv2D(filters=32, kernel_size=(5, 5), padding='Valid', activation='relu', input_shape=(48, 48, 1)))
    model.add(Conv2D(filters=32, kernel_size=(3, 3), padding='Same', activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(filters=64, kernel_size=(5, 5), padding='Valid', activation='relu'))
    model.add(Conv2D(filters=64, kernel_size=(3, 3), padding='Same', activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(519, activation="relu"))  # [[521,0.9962,70],[519,0.9969,51]
    model.add(Dropout(0.5))
    model.add(Dense(10, activation="softmax"))

    model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=1e-3), metrics=["accuracy"])
    print(model.summary())

    datagen = ImageDataGenerator(
        featurewise_center=False,
        samplewise_center=False,
        featurewise_std_normalization=False,
        samplewise_std_normalization=False,
        zca_whitening=False,
        rotation_range=10,
        zoom_range=0.1,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=False,
        vertical_flip=False)  # , preprocessing_function=random_add_or_erase_spot)

    return model,datagen

train = pd.read_csv("train.csv")
print(train.shape)

#Prepare dataset
y = train["labels"]
X = train.drop("labels", axis = 1)
print(y.value_counts().to_dict())
y = to_categorical(y, num_classes = 10)
del train

X = X / 255.0
X = X.values.reshape(-1,48,48,1)

# Shuffle Split Train and Test from original dataset
seed=2
train_index, valid_index = ShuffleSplit(n_splits=1,
                                        train_size=0.9,
                                        test_size=None,
                                        random_state=seed).split(X).__next__()
x_train = X[train_index]
Y_train = y[train_index]
x_test = X[valid_index]
Y_test = y[valid_index]

# Parameters
epochs = 30
batch_size = 64
validation_steps = 10000

# initialize Model, Annealer and Datagen
model, datagen = init_model()

# Start training
train_generator = datagen.flow(x_train, Y_train, batch_size=batch_size)
test_generator = datagen.flow(x_test, Y_test, batch_size=batch_size)

history = model.fit_generator(train_generator,
                    steps_per_epoch=x_train.shape[0]//batch_size,
                    epochs=epochs,
                    validation_data=test_generator,
                    validation_steps=validation_steps//batch_size,
                    )

score = model.evaluate(x_test, Y_test)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

# Saving Model for future API
model.save('fs_model.h5')
print("Saved model to disk")

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='lower right')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

## Model predict
test = pd.read_csv("test.csv")
print(test.shape)
test = test / 255
test = test.values.reshape(-1, 48, 48, 1)
p = np.argmax(model.predict(test), axis=1)

print('Base model scores:')
valid_loss, valid_acc = model.evaluate(x_test, Y_test, verbose=0)
valid_p = np.argmax(model.predict(x_test), axis=1)
target = np.argmax(Y_test, axis=1)
cm = confusion_matrix(target, valid_p)
print(cm)

labels = ['Manzana', 'Shampoo', 'Insecticida', 'Atún', 'Galleta', 'Helado', 'Pepino', 'Pescado']

n = 45

prd = model.predict(np.expand_dims(np.array(test[n], dtype=np.float32), 0))
prd = np.argmax(prd)
print(prd)
print(labels[prd])

plt.imshow(test[n].reshape(48,48), cmap="gray")
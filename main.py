# %%
# Importing used libraries
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from keras.utils import image_dataset_from_directory
from keras.models import Sequential
from keras import layers

from keras.callbacks import EarlyStopping
from keras.losses import SparseCategoricalCrossentropy

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# %%
# Loading in data
main_path = './Animals-10/'
img_size = (96, 96)
batch_size = 64

Xtrain, Xval = image_dataset_from_directory(main_path,
                                            subset='both',
                                            validation_split=0.2,
                                            image_size=img_size,
                                            batch_size=batch_size,
                                            shuffle=True,
                                            seed=123)

classes = Xtrain.class_names
num_classes = len(classes)
print(f'Dataset ima sledece klase: {classes}')

# %%
# Visualising data with examples of each class
img, lab = next(iter(Xtrain))
plt.figure()
cnt = 0
i = 0
class_set = set()
while cnt < 10:
    if classes[lab[i]] not in class_set:
        class_set.add(classes[lab[i]])
        cnt += 1
        plt.subplot(2, 5, cnt)
        plt.imshow(img[i].numpy().astype('uint8'))
        plt.title(classes[lab[i]])
        plt.axis('off')
    i += 1
plt.show()

# %%
# Histogram
labels = []

for _, lab in Xtrain.concatenate(Xval):
    labels.extend(lab.numpy())

labels = np.array(labels)

unique, counts = np.unique(labels, return_counts=True)

plt.bar(classes, counts)
plt.title("Raspodela klasa u celom dataset-u")
plt.xlabel("Klasa")
plt.ylabel("Broj uzoraka")
plt.xticks(rotation=30)
plt.show()

# %%
# Data augmentation
data_augmentation = Sequential(
    [
        layers.Input((img_size[0], img_size[1], 3)),
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.2),
        layers.RandomBrightness(0.2),
    ]
)

for i in range(10):
    aug_img = data_augmentation(img)
    plt.subplot(2, 5, i + 1)
    plt.imshow(aug_img[0].numpy().astype('uint8'))
    plt.axis('off')
plt.show()


# %%
# CNN model architecture
def cnn_model(num_classes):
    model = Sequential([
        data_augmentation,

        layers.Conv2D(8, 5, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),

        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),

        layers.Conv2D(48, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(48, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(),

        layers.Dropout(0.5),
        layers.Flatten(),

        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile('adam',
                  loss=SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])

    return model


# %%
# Model summary
model = cnn_model(num_classes)
model.summary()

# %%
# Model training
es = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True, verbose=1)
history = model.fit(Xtrain,
                    epochs=30,
                    validation_data=Xval,
                    callbacks=[es],
                    verbose=1,
                    class_weight={0: 1, 1: 1.25, 2: 0.67, 3: 1.11, 4: 0.42, 5: 1.33, 6: 0.77, 7: 1.1, 8: 0.41, 9: 1.1})

# %%
# Performance graph plot
plt.figure()
plt.subplot(121)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Accuracy')
plt.subplot(122)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Loss')
plt.show()

# %%
# Calculating accuracy on validation set + sorting good and bad matches
y_true = np.array([])
y_pred = np.array([])

bad_prediction = []
good_prediction = []

for img, lab in Xval:
    y_true = np.concatenate([y_true, lab.numpy()])
    pred = np.argmax(model.predict(img, verbose=0), axis=1)
    y_pred = np.concatenate([y_pred, pred])

    for i in range(len(lab)):
        if lab[i] != pred[i]:
            bad_prediction.append((
                img[i],
                classes[int(lab[i])],
                classes[int(pred[i])]
            ))
        else:
            good_prediction.append((
                img[i],
                classes[int(lab[i])],
                classes[int(pred[i])]
            ))

# %%
# Bad prediction examples
plt.figure(figsize=(18, 5))
for i in range(10):
    img, true, pred = bad_prediction[i]
    plt.subplot(2, 5, i+1)
    plt.imshow(img.numpy().astype('uint8'))
    plt.title(f'True: {true} / Prediction: {pred}')
    plt.axis('off')
plt.show()

# %%
# Good prediction examples
plt.figure(figsize=(18, 5))
for i in range(10):
    img, true, pred = good_prediction[i]
    plt.subplot(2, 5, i+1)
    plt.imshow(img.numpy().astype('uint8'))
    plt.title(f'True/Prediction: {pred}')
    plt.axis('off')
plt.show()

# %%
# Displaying model metrics
print(f"Tačnost modela je: {100 * accuracy_score(y_true, y_pred):.2f}%")
print(f"Preciznost modela je: {100 * precision_score(y_true, y_pred, average='weighted'):.2f}%")
print(f"F1 skor modela je: {100 * f1_score(y_true, y_pred, average='weighted'):.2f}%")
print(f"Senzitivnost modela je: {100 * recall_score(y_true, y_pred, average='weighted'):.2f}%")

# %%
# Confusion matrix for validation set
cm = confusion_matrix(y_true, y_pred, normalize='true')
fig, ax = plt.subplots(figsize=(8, 8))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
disp.plot(ax=ax, cmap='viridis', values_format=".2f")
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.show()

# %%
# Calculating accuracy on train set
y_true_train = np.array([])
y_pred_train = np.array([])

for img, lab in Xtrain:
    y_true_train = np.concatenate([y_true_train, lab.numpy()])
    pred = np.argmax(model.predict(img, verbose=0), axis=1)
    y_pred_train = np.concatenate([y_pred_train, pred])

# %%
# Confusion matrix for training set
cm = confusion_matrix(y_true_train, y_pred_train, normalize='true')
fig, ax = plt.subplots(figsize=(8, 8))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
disp.plot(ax=ax, cmap='viridis', values_format=".2f")
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.show()

# Animal Classification

A deep learning project for classifying animal images into 10 categories using a custom Convolutional Neural Network (CNN) built with TensorFlow and Keras.

## Overview

The project trains a CNN on the **Animals-10** image dataset. The pipeline includes dataset preparation, class distribution analysis, data augmentation, model training, evaluation, and visualization of predictions and classification performance.

The model uses image augmentation and class weighting to improve robustness and account for differences in class distribution.

## Features

- Image classification across 10 animal classes
- 80/20 training-validation split
- Image resizing to `96 × 96`
- Data augmentation using:
  - Random horizontal flipping
  - Random rotation
  - Random zoom
  - Random contrast
  - Random brightness
- Custom CNN architecture with:
  - Convolutional layers
  - Batch normalization
  - Max pooling
  - Dropout
  - Fully connected layers
- Early stopping with restoration of the best model weights
- Class weighting during training
- Training and validation accuracy/loss visualization
- Evaluation using:
  - Accuracy
  - Precision
  - Recall
  - F1 score
- Confusion matrix visualization
- Visualization of correctly and incorrectly classified images

## Model Architecture

The CNN consists of several convolutional blocks followed by a fully connected classification head.

```text
Input Image (96 × 96 × 3)
        │
Data Augmentation
        │
Conv2D → BatchNorm → MaxPooling
        │
Conv2D → BatchNorm → MaxPooling
        │
Conv2D → BatchNorm
        │
Conv2D → BatchNorm
        │
Conv2D → BatchNorm → MaxPooling
        │
Dropout (0.5)
        │
Flatten
        │
Dense (128, ReLU)
        │
Dense (10, Softmax)
```

The model is trained using the **Adam optimizer** and `SparseCategoricalCrossentropy` loss.

## Dataset

The project uses the **Animals-10** dataset, available on Kaggle:

**Dataset:** https://www.kaggle.com/datasets/alessiocorrado99/animals10

Download the dataset and place the `Animals-10` directory in the project root:

```text
AnimalClassification/
└── Animals-10/
```

The dataset is loaded using Keras' `image_dataset_from_directory` utility and split into:

- **80% training data**
- **20% validation data**

Images are resized to `96 × 96` pixels and processed in batches of 64.

## Project Structure

```text
AnimalClassification/
│
├── Animals-10/          # Dataset (not included in repository)
├── photos/              # Project images
├── main.py              # Data processing, model, training and evaluation
├── requirements.txt     # Python dependencies
├── LICENSE              # MIT License
└── README.md
```

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/MihajloSicovic/AnimalClassification.git
cd AnimalClassification

pip install -r requirements.txt
```

Required packages:

```text
numpy
scikit-learn
keras
tensorflow
```

## Usage

After downloading the dataset, place it in the project directory:

```text
AnimalClassification/
└── Animals-10/
```

Then run:

```bash
python main.py
```

The script will:

1. Load and split the dataset.
2. Display examples from the dataset.
3. Analyze class distribution.
4. Apply data augmentation.
5. Build and train the CNN.
6. Plot training and validation metrics.
7. Evaluate predictions on the validation set.
8. Display correctly and incorrectly classified examples.
9. Calculate classification metrics.
10. Generate confusion matrices for the validation and training sets.

## Training

The model is trained for up to **30 epochs** with early stopping based on validation accuracy.

```python
EarlyStopping(
    monitor='val_accuracy',
    patience=5,
    restore_best_weights=True
)
```

Class weights are also used during training to compensate for differences in the number of samples between classes.

## Evaluation

The model is evaluated using weighted:

- **Accuracy**
- **Precision**
- **Recall**
- **F1 Score**

Normalized confusion matrices are generated for both the validation and training sets to analyze classification performance between individual animal classes.

The project also stores correctly and incorrectly classified validation images, allowing individual predictions to be inspected visually.

## Technologies

- **Python**
- **TensorFlow**
- **Keras**
- **NumPy**
- **Scikit-learn**
- **Matplotlib**

## License

This project is licensed under the MIT License.

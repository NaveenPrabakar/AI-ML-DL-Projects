# Vegetable Image Classification

A deep learning project that classifies 7 different types of vegetables using Convolutional Neural Networks (CNN) with TensorFlow and Keras.

## Authors
- Naveen Prabakar
- Gregory Chernyavskiy  
- Riza Danurdoro

## Project Overview

This project implements an image classification model capable of identifying 7 different types of vegetables with high accuracy. The model achieved an average accuracy of 96% across 1400 test images.

## Dataset

- **Source**: Kaggle Vegetable Image Dataset
- **Structure**: 7 different vegetables with 1000 photos each
- **Total Images**: 7000 training images + 1400 test images (200 per vegetable)
- **Split**: 80% training / 20% validation

## Technologies Used

- **TensorFlow & Keras**: For CNN model development
- **Pandas & Seaborn**: Data visualization and analysis
- **NumPy**: Image manipulation and processing
- **ImageDataGenerator**: Data augmentation and preprocessing

## Model Architecture

### CNN Structure
- **Sequential Model** with the following layers:
  - Conv2D layers with ReLU activation
  - MaxPooling2D for dimensionality reduction
  - Flatten layer to convert 2D to 1D
  - Dense layers for classification
  - Batch Normalization and kernel regularization

### Key Parameters
- **Image Dimensions**: 180 × 180 pixels
- **Batch Size**: 32 images
- **Color Channels**: 3 (RGB)
- **Output Classes**: 7 vegetables

## Data Preprocessing & Augmentation

The ImageDataGenerator applies several augmentation techniques:
- **Rescaling**: Pixel values normalized to 0-1 range
- **Rotation**: Random rotation up to 20 degrees
- **Width/Height Shift**: Random horizontal/vertical shifts
- **Shear Range**: Image tilting transformation
- **Zoom Range**: Random zoom in/out
- **Horizontal Flip**: Random left-right flipping

## Model Training

### Initial Training
- **Epochs**: 10
- **Optimizer**: Adam
- **Loss Function**: Categorical Crossentropy
- **Metrics**: Accuracy

### Parameter Tuning
After observing fluctuations in validation accuracy, the following improvements were made:
- **Increased Epochs**: From 10 to 20
- **Reduced Learning Rate**: For more stable learning
- **Early Stopping**: To prevent overfitting

## Results

### Performance Metrics
- **Training Accuracy**: 96.94% (improved from 93.17%)
- **Validation Accuracy**: 96.93% (improved from 94.36%)
- **Test Accuracy**: 96% average across all vegetables

### Detailed Test Results
- **Precision, Recall, F1-Score**: Calculated for each vegetable class
- **Best Performance**: Vegetable class 3 achieved 100% accuracy
- **Challenging Class**: Brinjal (eggplant) had 87% accuracy due to color/shape similarity with other vegetables

### Confusion Matrix Analysis
- **Correct Predictions**: 1341 out of 1400 test images
- **Incorrect Predictions**: 59 images
- **Main Challenge**: Similar characteristics (colors, shapes) between certain vegetables

## Key Findings

### Model Behavior
- **No Underfitting**: High training accuracy indicates good learning
- **Minimal Overfitting**: Training and validation accuracies are comparable
- **Improved Consistency**: Parameter tuning eliminated accuracy fluctuations

### Error Analysis
- Primary misclassifications occurred due to similar visual characteristics
- Brinjal (eggplant) was the most challenging vegetable to classify correctly

## Future Improvements

1. **Enhanced Data Augmentation**: Better techniques to differentiate similar-looking vegetables
2. **Parameter Optimization**: Experiment with different target sizes and batch sizes
3. **Alternative Architectures**: Test other CNN models or transfer learning approaches
4. **Dataset Expansion**: Include more diverse images to improve robustness

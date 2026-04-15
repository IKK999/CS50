# Traffic AI (Traffic Sign Classification CNN)

A deep learning system that classifies **traffic signs from images** using a **Convolutional Neural Network (CNN)**. This project demonstrates end-to-end development of a computer vision pipeline for multi-class image classification.

---

## Overview
This model processes labeled traffic sign images and predicts one of **43 categories**, simulating real-world applications such as **autonomous driving and driver assistance systems**.

It includes:
- Image preprocessing and normalization  
- Train/test data splitting  
- CNN model design and training  
- Model evaluation and optional persistence  

---

## Features
- **Convolutional Neural Network (CNN)** built with TensorFlow/Keras  
- **Image preprocessing pipeline**
  - Resizing (30×30)
  - Normalization (pixel scaling)
  - Color space conversion (BGR → RGB)  
- **Multi-class classification (43 classes)**  
- **Dropout regularization** to reduce overfitting  
- **Model saving for deployment**  

---

## Tech Stack
- Python 3.x  
- TensorFlow / Keras  
- OpenCV (image processing)  
- NumPy, scikit-learn

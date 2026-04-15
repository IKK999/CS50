# Shopping AI (Customer Conversion Predictor)

A machine learning pipeline that predicts **e-commerce purchase intent** using behavioral session data. This project demonstrates end-to-end development of a **classification system**, from data preprocessing to model evaluation.

---

## Overview
This system analyzes user session data (e.g., page visits, duration, traffic source) to predict whether a visitor will generate **revenue (conversion)**.

It includes:
- Data cleaning and feature engineering  
- Train/test split for evaluation  
- K-Nearest Neighbors (KNN) classification  
- Performance metrics for business relevance  

---

## Features
- **Structured data preprocessing pipeline**
  - Categorical encoding (month, visitor type, weekend)
  - Type normalization (int/float conversion)
- **Supervised learning model (KNN)**
- **Evaluation using key classification metrics**
  - Sensitivity (True Positive Rate)
  - Specificity (True Negative Rate)
- **Reproducible ML workflow**

---

## Tech Stack
- Python 3.x  
- scikit-learn (KNeighborsClassifier, train/test split)

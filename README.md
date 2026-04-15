# Attention AI (Transformer Attention Visualizer)

A deep learning application that leverages **BERT (Transformer architecture)** to perform **masked language modeling** and visualize **self-attention mechanisms** across layers and heads.

---

## Overview
This project demonstrates how modern NLP models understand context by:
- Predicting missing words using a pre-trained **BERT model**
- Visualizing **attention weights** to interpret how tokens influence each other

It bridges **model performance and interpretability**, a critical area in modern AI systems.

---

## Features
- **Pre-trained Transformer (BERT)** for masked word prediction  
- **Top-K token predictions** for `[MASK]` inputs  
- **Attention visualization**
  - Per layer and per head  
  - Heatmap-style diagrams  
- **Token-level interpretability** of model behavior  

---

## Tech Stack
- Python 3.x  
- TensorFlow (Keras backend)  
- Hugging Face Transformers  
- PIL (image generation)

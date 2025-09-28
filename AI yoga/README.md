# Chair Pose Classification - Yoga AI Project

This project implements a machine learning model to classify chair poses (Utkatasana) in yoga using Convolutional Neural Networks (CNN). The model provides detailed evaluation metrics including **F1 Score**, **Precision**, **Accuracy**, and **Recall**.

## 🎯 Project Objectives

- Train a CNN model to detect chair poses in yoga images
- Achieve high performance metrics:
  - **Accuracy**: Overall correctness of predictions
  - **Precision**: Accuracy of positive predictions (chair pose detection)
  - **Recall**: Ability to find all chair poses
  - **F1 Score**: Harmonic mean of precision and recall

## 📁 Project Structure

```
C:\AI yoga\
├── chair_pose_classifier.py    # Main training script
├── evaluate_metrics.py         # Evaluation and metrics calculation
├── prepare_dataset.py          # Dataset preparation utilities
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── index.html                  # Web interface (existing)
├── script.js                   # Web scripts (existing)
├── styles.css                  # Web styles (existing)
└── data/                       # Dataset directory
    ├── train/
    │   ├── chair_pose/         # Training chair pose images
    │   └── other_poses/        # Training other yoga poses
    ├── validation/
    │   ├── chair_pose/         # Validation chair pose images
    │   └── other_poses/        # Validation other yoga poses
    └── test/
        ├── chair_pose/         # Test chair pose images
        └── other_poses/        # Test other yoga poses
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Dataset
```bash
python prepare_dataset.py
```
This script will:
- Create the required directory structure
- Provide options to download from Kaggle/GitHub
- Create synthetic data for testing if needed

### 3. Train the Model
```bash
python chair_pose_classifier.py
```
This will:
- Create and train a CNN model
- Save the best model weights
- Generate training history plots
- Calculate initial metrics

### 4. Evaluate with Detailed Metrics
```bash
python evaluate_metrics.py
```
This provides:
- **F1 Score**: Harmonic mean of precision and recall
- **Precision**: True positives / (True positives + False positives)
- **Accuracy**: (True positives + True negatives) / Total samples
- **Recall**: True positives / (True positives + False negatives)

## 📊 Key Features

### Model Architecture
- **CNN with 4 convolutional blocks**
- **Batch normalization** for stable training
- **Dropout layers** to prevent overfitting
- **Data augmentation** for better generalization
- **Early stopping** to prevent overtraining

### Evaluation Metrics

1. **Accuracy**: Measures overall correctness
   - Formula: (TP + TN) / (TP + TN + FP + FN)

2. **Precision**: Measures quality of positive predictions
   - Formula: TP / (TP + FP)
   - Important for minimizing false chair pose detections

3. **Recall**: Measures ability to find all chair poses
   - Formula: TP / (TP + FN)
   - Important for not missing actual chair poses

4. **F1 Score**: Balanced measure combining precision and recall
   - Formula: 2 × (Precision × Recall) / (Precision + Recall)

### Output Files
- `chair_pose_classifier_final.h5`: Trained model
- `chair_pose_metrics.csv`: Detailed metrics results
- `chair_pose_confusion_matrix.png`: Visual confusion matrix
- `chair_pose_metrics_chart.png`: Metrics visualization
- `training_history.png`: Training progress plots

## 📈 Expected Performance

Target metrics for a well-trained model:
- **Accuracy**: > 85%
- **Precision**: > 80%
- **Recall**: > 80%
- **F1 Score**: > 80%

## 🔧 Customization

### Adjust Model Parameters
Edit `chair_pose_classifier.py`:
```python
classifier = ChairPoseClassifier(
    img_height=224,    # Image height
    img_width=224,     # Image width
    batch_size=32      # Batch size
)
```

### Training Parameters
```python
history = classifier.train_model(
    train_generator, 
    validation_generator, 
    epochs=30  # Number of training epochs
)
```

## 📚 Data Sources

The project supports data from:
1. **Kaggle**: [Yoga Pose Image Classification Dataset](https://www.kaggle.com/datasets/shrutisaxena/yoga-pose-image-classification-dataset/data)
2. **GitHub**: [Yoga_Poses-Dataset](https://github.com/Manoj-2702/Yoga_Poses-Dataset)
3. **Custom images**: Your own chair pose images

## 🎨 Integration with Web Interface

This project integrates with your existing web application:
- Use the trained model (`chair_pose_classifier_final.h5`) in your web interface
- Load the model in JavaScript using TensorFlow.js
- Apply real-time chair pose detection

## 📋 Troubleshooting

### Common Issues

1. **GPU Memory Error**: Reduce batch_size in the classifier
2. **Low Accuracy**: 
   - Increase dataset size
   - Add more data augmentation
   - Increase training epochs
3. **Model Not Found**: Run `chair_pose_classifier.py` first

### Dependencies Issues
If you encounter import errors:
```bash
pip install --upgrade tensorflow opencv-python scikit-learn matplotlib seaborn pandas
```

## 🏆 Model Performance Interpretation

### Understanding Your Metrics

- **High Accuracy + High Precision + Low Recall**: Model is very conservative, misses some chair poses
- **High Accuracy + Low Precision + High Recall**: Model detects most chair poses but has false positives
- **Balanced High Scores**: Optimal performance
- **F1 Score Close to Precision/Recall**: Good balance between false positives and false negatives

## 📞 Support

For issues or questions:
1. Check the console output for error messages
2. Ensure all dependencies are installed correctly
3. Verify dataset structure matches the expected format
4. Review the generated plots and metrics for insights

---

**Happy Training! 🧘‍♀️🤖**
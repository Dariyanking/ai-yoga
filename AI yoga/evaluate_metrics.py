import tensorflow as tf
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def load_and_evaluate_model(model_path, test_data_path, img_height=224, img_width=224, batch_size=32):
    """
    Load a trained model and evaluate it on test data
    Returns F1 score, Precision, Accuracy, and Recall
    """
    
    print("Loading trained model...")
    model = tf.keras.models.load_model(model_path)
    
    print("Preparing test data...")
    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    
    test_generator = test_datagen.flow_from_directory(
        test_data_path,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='binary',
        shuffle=False
    )
    
    print("Making predictions...")
    predictions = model.predict(test_generator, verbose=1)
    y_pred = (predictions > 0.5).astype(int).flatten()
    y_true = test_generator.classes
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='binary')
    recall = recall_score(y_true, y_pred, average='binary')
    f1 = f1_score(y_true, y_pred, average='binary')
    
    # Display results
    print("\\n" + "="*60)
    print("YOGA CHAIR POSE CLASSIFICATION EVALUATION")
    print("="*60)
    print(f"📊 ACCURACY:   {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"🎯 PRECISION:  {precision:.4f} ({precision*100:.2f}%)")
    print(f"🔍 RECALL:     {recall:.4f} ({recall*100:.2f}%)")
    print(f"⚖️  F1 SCORE:   {f1:.4f} ({f1*100:.2f}%)")
    print("="*60)
    
    # Create metrics summary
    metrics_summary = {
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
        'Value': [accuracy, precision, recall, f1],
        'Percentage': [f"{accuracy*100:.2f}%", f"{precision*100:.2f}%", 
                      f"{recall*100:.2f}%", f"{f1*100:.2f}%"]
    }
    
    metrics_df = pd.DataFrame(metrics_summary)
    print("\\nMetrics Summary:")
    print(metrics_df.to_string(index=False))
    
    # Save metrics to CSV
    metrics_data = {
        'accuracy': accuracy,
        'precision': precision, 
        'recall': recall,
        'f1_score': f1
    }
    
    pd.DataFrame([metrics_data]).to_csv('chair_pose_metrics.csv', index=False)
    print("\\n✅ Metrics saved to 'chair_pose_metrics.csv'")
    
    # Detailed classification report
    print("\\nDetailed Classification Report:")
    target_names = ['Not Chair Pose', 'Chair Pose']
    print(classification_report(y_true, y_pred, target_names=target_names))
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=target_names,
                yticklabels=target_names,
                cbar_kws={'label': 'Count'})
    
    plt.title('Confusion Matrix - Chair Pose vs Other Poses\\nYoga Classification Model', 
              fontsize=14, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    
    # Add text annotations for better understanding
    plt.text(0.5, -0.1, f'Total Test Samples: {len(y_true)}', 
             transform=plt.gca().transAxes, ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('chair_pose_confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("\\n📊 Confusion matrix saved as 'chair_pose_confusion_matrix.png'")
    plt.show()
    
    # Create metrics visualization
    plt.figure(figsize=(12, 6))
    
    # Bar plot of metrics
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    metrics_values = [accuracy, precision, recall, f1]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    bars = plt.bar(metrics_names, metrics_values, color=colors, alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar, value in zip(bars, metrics_values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.3f}\\n({value*100:.1f}%)', 
                ha='center', va='bottom', fontweight='bold')
    
    plt.title('Chair Pose Classification - Performance Metrics', 
              fontsize=14, fontweight='bold', pad=20)
    plt.ylabel('Score', fontsize=12)
    plt.ylim(0, 1.1)
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add horizontal reference lines
    plt.axhline(y=0.8, color='green', linestyle='--', alpha=0.5, label='Good (80%)')
    plt.axhline(y=0.9, color='blue', linestyle='--', alpha=0.5, label='Excellent (90%)')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('chair_pose_metrics_chart.png', dpi=300, bbox_inches='tight')
    print("📈 Metrics chart saved as 'chair_pose_metrics_chart.png'")
    plt.show()
    
    return metrics_data

def evaluate_predictions_array(y_true, y_pred):
    """
    Evaluate predictions given true labels and predicted labels
    """
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='binary')
    recall = recall_score(y_true, y_pred, average='binary')
    f1 = f1_score(y_true, y_pred, average='binary')
    
    print("\\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)
    print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"F1 Score:  {f1:.4f} ({f1*100:.2f}%)")
    print("="*50)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

def main():
    """Main evaluation function"""
    print("Chair Pose Classification - Metrics Evaluation")
    print("=" * 50)
    
    # Check if model exists
    model_path = 'chair_pose_classifier_final.h5'
    test_data_path = 'data/test'
    
    if os.path.exists(model_path) and os.path.exists(test_data_path):
        print(f"Found model: {model_path}")
        print(f"Found test data: {test_data_path}")
        
        # Evaluate the model
        metrics = load_and_evaluate_model(model_path, test_data_path)
        
        print("\\n🎉 Evaluation complete!")
        print("Files generated:")
        print("- chair_pose_metrics.csv")
        print("- chair_pose_confusion_matrix.png")
        print("- chair_pose_metrics_chart.png")
        
    else:
        print("❌ Model or test data not found!")
        print("Please ensure you have:")
        print("1. A trained model file: 'chair_pose_classifier_final.h5'")
        print("2. Test data directory: 'data/test'")
        print("\\nRun the training script first: python chair_pose_classifier.py")
        
        # Demonstrate with sample data
        print("\\nDemonstrating with sample predictions...")
        
        # Sample predictions (for demonstration)
        np.random.seed(42)
        y_true = np.array([0, 1, 1, 0, 1, 1, 0, 0, 1, 0] * 10)  # 100 samples
        y_pred = np.array([0, 1, 1, 0, 0, 1, 0, 1, 1, 0] * 10)  # Some errors
        
        sample_metrics = evaluate_predictions_array(y_true, y_pred)
        print("\\n(Note: This is sample data for demonstration)")

if __name__ == "__main__":
    main()
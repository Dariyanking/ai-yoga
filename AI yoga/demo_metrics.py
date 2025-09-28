"""
Demo script for Chair Pose Classification Metrics
Shows F1 Score, Precision, Accuracy, and Recall calculations
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report, confusion_matrix

def calculate_metrics_demo():
    """Demonstrate metrics calculation with sample data"""
    
    print("🧘 Chair Pose Classification - Metrics Demo")
    print("=" * 50)
    
    # Simulate realistic predictions for chair pose classification
    np.random.seed(42)
    
    # Create realistic test data (100 samples)
    # 40 actual chair poses, 60 other poses
    y_true = np.array([1] * 40 + [0] * 60)
    
    # Simulate model predictions with realistic performance
    # Model correctly identifies most chair poses but has some errors
    y_pred = y_true.copy()
    
    # Add some realistic errors:
    # - Miss 3 chair poses (False Negatives)
    y_pred[[5, 12, 25]] = 0  
    
    # - Incorrectly identify 4 other poses as chair poses (False Positives)  
    y_pred[[45, 52, 68, 71]] = 1
    
    # Calculate all metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    # Display results with explanations
    print("\\n📊 EVALUATION METRICS RESULTS")
    print("=" * 50)
    print(f"🎯 ACCURACY:   {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("   → Overall correctness: (Correct predictions) / (Total predictions)")
    
    print(f"\\n🔍 PRECISION:  {precision:.4f} ({precision*100:.2f}%)")  
    print("   → Chair pose detection quality: (True Chair Poses) / (All Chair Pose Predictions)")
    print("   → Higher = Fewer false alarms")
    
    print(f"\\n📈 RECALL:     {recall:.4f} ({recall*100:.2f}%)")
    print("   → Chair pose detection coverage: (True Chair Poses) / (All Actual Chair Poses)")
    print("   → Higher = Fewer missed chair poses")
    
    print(f"\\n⚖️  F1 SCORE:   {f1:.4f} ({f1*100:.2f}%)")
    print("   → Balanced measure: 2 × (Precision × Recall) / (Precision + Recall)")
    print("   → Higher = Better overall performance")
    
    # Confusion Matrix Analysis
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print("\\n🔢 CONFUSION MATRIX BREAKDOWN")
    print("=" * 50)
    print(f"True Negatives (TN):  {tn:2d} - Correctly identified other poses")
    print(f"False Positives (FP): {fp:2d} - Other poses wrongly identified as chair pose")
    print(f"False Negatives (FN): {fn:2d} - Chair poses missed by the model") 
    print(f"True Positives (TP):  {tp:2d} - Correctly identified chair poses")
    
    # Create detailed classification report
    print("\\n📋 DETAILED CLASSIFICATION REPORT")
    print("=" * 50)
    target_names = ['Other Poses', 'Chair Pose']
    print(classification_report(y_true, y_pred, target_names=target_names))
    
    # Visualizations
    create_visualizations(y_true, y_pred, accuracy, precision, recall, f1)
    
    # Save metrics to CSV
    metrics_data = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'true_positives': tp,
        'true_negatives': tn,
        'false_positives': fp,
        'false_negatives': fn
    }
    
    df = pd.DataFrame([metrics_data])
    df.to_csv('demo_chair_pose_metrics.csv', index=False)
    print("\\n💾 Metrics saved to 'demo_chair_pose_metrics.csv'")
    
    return metrics_data

def create_visualizations(y_true, y_pred, accuracy, precision, recall, f1):
    """Create visualizations for the metrics"""
    
    # Set up the plotting style
    plt.style.use('default')
    
    # Create a figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax1,
                xticklabels=['Other Poses', 'Chair Pose'],
                yticklabels=['Other Poses', 'Chair Pose'])
    ax1.set_title('Confusion Matrix\\nChair Pose vs Other Poses', fontweight='bold')
    ax1.set_xlabel('Predicted Label')
    ax1.set_ylabel('True Label')
    
    # 2. Metrics Bar Chart
    metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    metrics_values = [accuracy, precision, recall, f1]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    bars = ax2.bar(metrics_names, metrics_values, color=colors, alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar, value in zip(bars, metrics_values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.3f}\\n({value*100:.1f}%)', 
                ha='center', va='bottom', fontweight='bold')
    
    ax2.set_title('Performance Metrics', fontweight='bold')
    ax2.set_ylabel('Score')
    ax2.set_ylim(0, 1.1)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add reference lines
    ax2.axhline(y=0.8, color='green', linestyle='--', alpha=0.5, label='Good (80%)')
    ax2.axhline(y=0.9, color='blue', linestyle='--', alpha=0.5, label='Excellent (90%)')
    ax2.legend()
    
    # 3. Prediction Distribution
    unique, counts = np.unique(y_pred, return_counts=True)
    ax3.pie(counts, labels=['Other Poses', 'Chair Pose'], autopct='%1.1f%%', 
            colors=['lightcoral', 'lightblue'], startangle=90)
    ax3.set_title('Model Predictions Distribution', fontweight='bold')
    
    # 4. Performance Interpretation
    ax4.axis('off')
    interpretation_text = f\"\"\"
📊 PERFORMANCE INTERPRETATION

✅ ACCURACY: {accuracy:.1%}
   Overall correctness of all predictions
   
🎯 PRECISION: {precision:.1%}  
   Of all chair pose predictions, {precision:.1%} were correct
   
🔍 RECALL: {recall:.1%}
   Of all actual chair poses, {recall:.1%} were detected
   
⚖️ F1 SCORE: {f1:.1%}
   Balanced measure combining precision & recall

📈 MODEL QUALITY:
   {'Excellent' if f1 > 0.9 else 'Good' if f1 > 0.8 else 'Moderate' if f1 > 0.7 else 'Needs Improvement'}
   
🎯 RECOMMENDATIONS:
   - {'Great performance!' if f1 > 0.9 else 'Consider more training data' if f1 < 0.8 else 'Good balance of metrics'}
    \"\"\"
    
    ax4.text(0.05, 0.95, interpretation_text, transform=ax4.transAxes, 
             fontsize=10, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('demo_chair_pose_analysis.png', dpi=300, bbox_inches='tight')
    print("\\n📊 Visualization saved as 'demo_chair_pose_analysis.png'")
    plt.show()

def explain_metrics():
    """Provide detailed explanations of the metrics"""
    
    print("\\n📚 UNDERSTANDING THE METRICS")
    print("=" * 60)
    
    explanations = {
        "ACCURACY": {
            "definition": "Overall correctness of the model",
            "formula": "(TP + TN) / (TP + TN + FP + FN)",
            "interpretation": "Higher is better. Shows how often the model is correct overall.",
            "when_to_use": "When classes are balanced and all errors are equally important"
        },
        
        "PRECISION": {
            "definition": "Quality of positive predictions (chair pose detections)",
            "formula": "TP / (TP + FP)", 
            "interpretation": "Higher is better. Reduces false alarms.",
            "when_to_use": "When false positives are costly (wrongly detecting chair pose)"
        },
        
        "RECALL": {
            "definition": "Completeness of positive predictions (finding all chair poses)",
            "formula": "TP / (TP + FN)",
            "interpretation": "Higher is better. Reduces missed detections.",
            "when_to_use": "When false negatives are costly (missing actual chair poses)"
        },
        
        "F1 SCORE": {
            "definition": "Harmonic mean of precision and recall",
            "formula": "2 × (Precision × Recall) / (Precision + Recall)",
            "interpretation": "Higher is better. Balanced measure when you care about both precision and recall.",
            "when_to_use": "When you need a single metric that balances precision and recall"
        }
    }
    
    for metric, info in explanations.items():
        print(f"\\n🎯 {metric}")
        print(f"   Definition: {info['definition']}")
        print(f"   Formula: {info['formula']}")
        print(f"   Interpretation: {info['interpretation']}")
        print(f"   When to use: {info['when_to_use']}")

if __name__ == "__main__":
    print("Starting Chair Pose Classification Metrics Demo...\\n")
    
    # Run the demo
    metrics = calculate_metrics_demo()
    
    # Provide explanations
    explain_metrics()
    
    # Summary
    print("\\n" + "=" * 60)
    print("🎉 DEMO COMPLETED!")
    print("=" * 60)
    print("Files created:")
    print("- demo_chair_pose_metrics.csv (metrics data)")
    print("- demo_chair_pose_analysis.png (visualizations)")
    print("\\nThis demo shows how your actual model will be evaluated.")
    print("The real training will use your yoga pose images and provide")
    print("similar detailed metrics for chair pose classification!")
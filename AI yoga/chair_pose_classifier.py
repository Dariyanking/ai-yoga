import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score, accuracy_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from pathlib import Path
import cv2
from PIL import Image

class ChairPoseClassifier:
    def __init__(self, img_height=224, img_width=224, batch_size=32):
        self.img_height = img_height
        self.img_width = img_width
        self.batch_size = batch_size
        self.model = None
        self.history = None
        
    def create_model(self):
        """Create CNN model for chair pose classification"""
        model = models.Sequential([
            # First Convolutional Block
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_height, self.img_width, 3)),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, 2),
            layers.Dropout(0.25),
            
            # Second Convolutional Block
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, 2),
            layers.Dropout(0.25),
            
            # Third Convolutional Block
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, 2),
            layers.Dropout(0.25),
            
            # Fourth Convolutional Block
            layers.Conv2D(256, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, 2),
            layers.Dropout(0.25),
            
            # Flatten and Dense layers
            layers.Flatten(),
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            # Output layer (binary classification)
            layers.Dense(1, activation='sigmoid')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def prepare_data_generators(self, train_dir, validation_dir):
        """Prepare data generators with augmentation"""
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            fill_mode='nearest'
        )
        
        validation_datagen = ImageDataGenerator(rescale=1./255)
        
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='binary',  # binary classification
            shuffle=True
        )
        
        validation_generator = validation_datagen.flow_from_directory(
            validation_dir,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='binary',
            shuffle=False
        )
        
        return train_generator, validation_generator
    
    def train_model(self, train_generator, validation_generator, epochs=50):
        """Train the model with callbacks"""
        # Define callbacks
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
        
        model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
            'best_chair_pose_model.h5',
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
        
        # Train the model
        self.history = self.model.fit(
            train_generator,
            epochs=epochs,
            validation_data=validation_generator,
            callbacks=[early_stopping, reduce_lr, model_checkpoint]
        )
        
        return self.history
    
    def evaluate_model(self, test_generator):
        """Evaluate model and calculate all metrics"""
        # Get predictions
        predictions = self.model.predict(test_generator)
        y_pred = (predictions > 0.5).astype(int).flatten()
        y_true = test_generator.classes
        
        # Calculate metrics
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='binary')
        recall = recall_score(y_true, y_pred, average='binary')
        f1 = f1_score(y_true, y_pred, average='binary')
        
        # Print results
        print("\n" + "="*50)
        print("CHAIR POSE CLASSIFICATION RESULTS")
        print("="*50)
        print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
        print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
        print(f"F1 Score:  {f1:.4f} ({f1*100:.2f}%)")
        print("="*50)
        
        # Detailed classification report
        print("\nDetailed Classification Report:")
        print(classification_report(y_true, y_pred, target_names=['Not Chair Pose', 'Chair Pose']))
        
        # Confusion Matrix
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Not Chair Pose', 'Chair Pose'],
                   yticklabels=['Not Chair Pose', 'Chair Pose'])
        plt.title('Confusion Matrix - Chair Pose Classification')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            print("No training history available. Train the model first.")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy', marker='o')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy', marker='s')
        ax1.set_title('Model Accuracy Over Epochs')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Plot loss
        ax2.plot(self.history.history['loss'], label='Training Loss', marker='o')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss', marker='s')
        ax2.set_title('Model Loss Over Epochs')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
        plt.show()

def create_sample_dataset():
    """Create sample dataset structure for demonstration"""
    # Create directory structure
    dirs = [
        'data/train/chair_pose',
        'data/train/other_poses',
        'data/validation/chair_pose', 
        'data/validation/other_poses',
        'data/test/chair_pose',
        'data/test/other_poses'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    print("Sample dataset structure created!")
    print("Please add your chair pose images to:")
    print("- data/train/chair_pose/")
    print("- data/validation/chair_pose/")
    print("- data/test/chair_pose/")
    print("\nAnd other yoga poses to:")
    print("- data/train/other_poses/")
    print("- data/validation/other_poses/")
    print("- data/test/other_poses/")

def main():
    # Create sample dataset structure if it doesn't exist
    if not os.path.exists('data'):
        print("Creating sample dataset structure...")
        create_sample_dataset()
        print("\nPlease organize your yoga pose images in the created directories and run again.")
        return
    
    # Initialize classifier
    classifier = ChairPoseClassifier()
    
    # Create model
    print("Creating CNN model...")
    model = classifier.create_model()
    print(model.summary())
    
    # Check if data directories exist and have images
    train_dir = 'data/train'
    validation_dir = 'data/validation'
    test_dir = 'data/test'
    
    if not all(os.path.exists(d) for d in [train_dir, validation_dir, test_dir]):
        print("Error: Please ensure data directories exist with proper structure.")
        print("Run create_sample_dataset() first.")
        return
    
    # Prepare data generators
    print("Preparing data generators...")
    train_generator, validation_generator = classifier.prepare_data_generators(
        train_dir, validation_dir
    )
    
    # Train model
    print("Starting training...")
    history = classifier.train_model(train_generator, validation_generator, epochs=30)
    
    # Plot training history
    classifier.plot_training_history()
    
    # Prepare test generator
    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(classifier.img_height, classifier.img_width),
        batch_size=classifier.batch_size,
        class_mode='binary',
        shuffle=False
    )
    
    # Evaluate model
    print("Evaluating model...")
    metrics = classifier.evaluate_model(test_generator)
    
    # Save metrics to file
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv('evaluation_metrics.csv', index=False)
    print("\nMetrics saved to 'evaluation_metrics.csv'")
    
    # Save model
    classifier.model.save('chair_pose_classifier_final.h5')
    print("Model saved as 'chair_pose_classifier_final.h5'")

if __name__ == "__main__":
    main()
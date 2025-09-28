import os
import zipfile
import shutil
from pathlib import Path
import requests
import cv2
import numpy as np
from PIL import Image
import pandas as pd

class DatasetPreparation:
    def __init__(self):
        self.base_dir = Path("./data")
        self.raw_dir = self.base_dir / "raw"
        self.processed_dir = self.base_dir / "processed"
        
    def setup_directories(self):
        """Create necessary directories"""
        dirs = [
            "data/raw/kaggle",
            "data/raw/github", 
            "data/train/chair_pose",
            "data/train/other_poses",
            "data/validation/chair_pose",
            "data/validation/other_poses", 
            "data/test/chair_pose",
            "data/test/other_poses"
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            
        print("Directory structure created successfully!")
        
    def download_kaggle_dataset(self):
        """Download dataset from Kaggle"""
        print("To download from Kaggle, you need:")
        print("1. Install kaggle: pip install kaggle")
        print("2. Setup Kaggle API credentials")
        print("3. Run: kaggle datasets download -d shrutisaxena/yoga-pose-image-classification-dataset")
        print("\nAfter download, extract the zip file to data/raw/kaggle/")
        
    def download_github_repo(self):
        """Clone GitHub repository"""
        print("To download from GitHub:")
        print("1. Run: git clone https://github.com/Manoj-2702/Yoga_Poses-Dataset.git")
        print("2. Move contents to data/raw/github/")
        
    def extract_chair_poses(self, source_dir):
        """Extract chair pose images from the dataset"""
        chair_pose_count = 0
        other_pose_count = 0
        
        # Look for chair pose images (usually named with 'chair' or similar)
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    file_path = os.path.join(root, file)
                    
                    # Check if it's a chair pose based on filename or directory
                    is_chair_pose = any(keyword in file.lower() or keyword in root.lower() 
                                      for keyword in ['chair', 'utkatasana'])
                    
                    try:
                        # Load and validate image
                        img = cv2.imread(file_path)
                        if img is not None:
                            # Resize image to standard size
                            img_resized = cv2.resize(img, (224, 224))
                            
                            if is_chair_pose:
                                # This is a chair pose
                                target_path = f"data/train/chair_pose/chair_{chair_pose_count}.jpg"
                                cv2.imwrite(target_path, img_resized)
                                chair_pose_count += 1
                            else:
                                # This is another pose
                                target_path = f"data/train/other_poses/other_{other_pose_count}.jpg"
                                cv2.imwrite(target_path, img_resized)
                                other_pose_count += 1
                                
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
                        
        print(f"Extracted {chair_pose_count} chair pose images")
        print(f"Extracted {other_pose_count} other pose images")
        
    def split_data(self):
        """Split data into train/validation/test sets"""
        import random
        
        # Split chair poses
        chair_files = os.listdir("data/train/chair_pose")
        random.shuffle(chair_files)
        
        chair_train = chair_files[:int(0.7 * len(chair_files))]
        chair_val = chair_files[int(0.7 * len(chair_files)):int(0.85 * len(chair_files))]
        chair_test = chair_files[int(0.85 * len(chair_files)):]
        
        # Move validation files
        for file in chair_val:
            shutil.move(f"data/train/chair_pose/{file}", f"data/validation/chair_pose/{file}")
            
        # Move test files  
        for file in chair_test:
            shutil.move(f"data/train/chair_pose/{file}", f"data/test/chair_pose/{file}")
            
        # Split other poses
        other_files = os.listdir("data/train/other_poses")
        random.shuffle(other_files)
        
        other_train = other_files[:int(0.7 * len(other_files))]
        other_val = other_files[int(0.7 * len(other_files)):int(0.85 * len(other_files))]
        other_test = other_files[int(0.85 * len(other_files)):]
        
        # Move validation files
        for file in other_val:
            shutil.move(f"data/train/other_poses/{file}", f"data/validation/other_poses/{file}")
            
        # Move test files
        for file in other_test:
            shutil.move(f"data/train/other_poses/{file}", f"data/test/other_poses/{file}")
            
        print("Data split completed!")
        print(f"Training: {len(chair_train)} chair poses, {len(other_train)} other poses")
        print(f"Validation: {len(chair_val)} chair poses, {len(other_val)} other poses") 
        print(f"Test: {len(chair_test)} chair poses, {len(other_test)} other poses")

def create_sample_images():
    """Create some sample synthetic images for testing"""
    print("Creating sample synthetic images for demonstration...")
    
    # Create sample chair pose images (simple rectangles to simulate poses)
    for i in range(50):
        # Create a simple synthetic image
        img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # Add some geometric shapes to simulate a pose
        cv2.rectangle(img, (50, 50), (174, 174), (0, 255, 0), 3)
        cv2.circle(img, (112, 112), 30, (255, 0, 0), -1)
        
        cv2.imwrite(f"data/train/chair_pose/synthetic_chair_{i}.jpg", img)
        
    # Create sample other pose images
    for i in range(50):
        img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        # Different pattern for other poses
        cv2.ellipse(img, (112, 112), (80, 40), 0, 0, 360, (0, 0, 255), -1)
        
        cv2.imwrite(f"data/train/other_poses/synthetic_other_{i}.jpg", img)
        
    # Create validation and test samples
    for i in range(10):
        # Validation chair poses
        img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        cv2.rectangle(img, (60, 60), (164, 164), (0, 255, 0), 3)
        cv2.imwrite(f"data/validation/chair_pose/val_chair_{i}.jpg", img)
        
        # Validation other poses
        img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        cv2.ellipse(img, (112, 112), (70, 50), 45, 0, 360, (0, 0, 255), -1)
        cv2.imwrite(f"data/validation/other_poses/val_other_{i}.jpg", img)
        
        # Test chair poses
        img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        cv2.rectangle(img, (40, 40), (184, 184), (0, 255, 0), 3)
        cv2.imwrite(f"data/test/chair_pose/test_chair_{i}.jpg", img)
        
        # Test other poses  
        img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        cv2.ellipse(img, (112, 112), (90, 30), 90, 0, 360, (0, 0, 255), -1)
        cv2.imwrite(f"data/test/other_poses/test_other_{i}.jpg", img)
        
    print("Sample synthetic dataset created!")

def main():
    prep = DatasetPreparation()
    
    print("Setting up directories...")
    prep.setup_directories()
    
    print("\n" + "="*60)
    print("DATASET PREPARATION OPTIONS")
    print("="*60)
    print("1. If you have yoga pose images ready:")
    print("   - Place chair pose images in: data/raw/chair_poses/")
    print("   - Place other pose images in: data/raw/other_poses/")
    print("   - Then run the extract_chair_poses() method")
    print()
    print("2. To download from online sources:")
    prep.download_kaggle_dataset()
    print()
    prep.download_github_repo()
    print()
    print("3. For quick testing with synthetic data:")
    print("   - Run create_sample_images() to generate synthetic poses")
    print("="*60)
    
    # Ask user what they want to do
    choice = input("\nChoose option (1/2/3) or press Enter to create synthetic data for testing: ").strip()
    
    if choice == "1":
        print("Please organize your images in the specified directories and run extract_chair_poses()")
    elif choice == "2":
        print("Please follow the download instructions above")
    else:
        print("Creating synthetic dataset for testing...")
        create_sample_images()
        print("\nDataset preparation complete!")
        print("You can now run: python chair_pose_classifier.py")

if __name__ == "__main__":
    main()
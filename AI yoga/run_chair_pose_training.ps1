# Chair Pose Classification Training Script
# PowerShell script to run the complete training and evaluation pipeline

Write-Host "🧘 Chair Pose Classification - Training Pipeline" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Function to check if Python is available
function Test-Python {
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python") {
            Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "❌ Python not found or not accessible" -ForegroundColor Red
        Write-Host "Please install Python from https://python.org or Microsoft Store" -ForegroundColor Yellow
        return $false
    }
    return $false
}

# Function to install requirements
function Install-Requirements {
    Write-Host "`n📦 Installing required packages..." -ForegroundColor Yellow
    try {
        python -m pip install -r requirements.txt
        Write-Host "✅ Requirements installed successfully" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to install requirements" -ForegroundColor Red
        return $false
    }
}

# Function to prepare dataset
function Prepare-Dataset {
    Write-Host "`n📊 Preparing dataset..." -ForegroundColor Yellow
    
    # Check if data directories exist and have content
    $trainChairDir = "data\train\chair_pose"
    $trainOtherDir = "data\train\other_poses"
    
    if ((Test-Path $trainChairDir) -and (Test-Path $trainOtherDir)) {
        $chairCount = (Get-ChildItem $trainChairDir -Filter *.jpg).Count
        $otherCount = (Get-ChildItem $trainOtherDir -Filter *.jpg).Count
        
        if ($chairCount -gt 0 -and $otherCount -gt 0) {
            Write-Host "✅ Found existing dataset:" -ForegroundColor Green
            Write-Host "   - Chair poses: $chairCount images" -ForegroundColor White
            Write-Host "   - Other poses: $otherCount images" -ForegroundColor White
            return $true
        }
    }
    
    Write-Host "⚠️  No existing dataset found. Creating synthetic data for demonstration..." -ForegroundColor Yellow
    
    try {
        python prepare_dataset.py
        Write-Host "✅ Dataset preparation completed" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to prepare dataset" -ForegroundColor Red
        return $false
    }
}

# Function to train model
function Train-Model {
    Write-Host "`n🤖 Training chair pose classification model..." -ForegroundColor Yellow
    Write-Host "This may take several minutes depending on your hardware..." -ForegroundColor Gray
    
    try {
        python chair_pose_classifier.py
        Write-Host "✅ Model training completed" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Model training failed" -ForegroundColor Red
        return $false
    }
}

# Function to evaluate model
function Evaluate-Model {
    Write-Host "`n📈 Evaluating model and calculating metrics..." -ForegroundColor Yellow
    
    try {
        python evaluate_metrics.py
        Write-Host "✅ Model evaluation completed" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Model evaluation failed" -ForegroundColor Red
        return $false
    }
}

# Main execution
Write-Host "`nStarting Chair Pose Classification Pipeline...`n" -ForegroundColor White

# Step 1: Check Python
if (-not (Test-Python)) {
    Write-Host "`n❌ Cannot proceed without Python. Please install Python and try again." -ForegroundColor Red
    Write-Host "Download from: https://python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Step 2: Install requirements
if (-not (Install-Requirements)) {
    Write-Host "`n❌ Cannot proceed without required packages." -ForegroundColor Red
    exit 1
}

# Step 3: Prepare dataset
if (-not (Prepare-Dataset)) {
    Write-Host "`n❌ Dataset preparation failed." -ForegroundColor Red
    exit 1
}

# Step 4: Train model
if (-not (Train-Model)) {
    Write-Host "`n❌ Model training failed." -ForegroundColor Red
    exit 1
}

# Step 5: Evaluate model
if (-not (Evaluate-Model)) {
    Write-Host "`n⚠️  Model evaluation failed, but training was successful." -ForegroundColor Yellow
}

# Summary
Write-Host "`n🎉 Pipeline completed successfully!" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

Write-Host "`nGenerated files:" -ForegroundColor White
Write-Host "- chair_pose_classifier_final.h5 (Trained model)" -ForegroundColor Gray
Write-Host "- chair_pose_metrics.csv (Evaluation metrics)" -ForegroundColor Gray
Write-Host "- chair_pose_confusion_matrix.png (Confusion matrix)" -ForegroundColor Gray
Write-Host "- chair_pose_metrics_chart.png (Metrics visualization)" -ForegroundColor Gray
Write-Host "- training_history.png (Training progress)" -ForegroundColor Gray

Write-Host "`n📊 Your F1 Score, Precision, Accuracy, and Recall are in:" -ForegroundColor Yellow
Write-Host "- chair_pose_metrics.csv" -ForegroundColor White
Write-Host "- Console output above" -ForegroundColor White

Write-Host "`n🎯 Next steps:" -ForegroundColor Cyan
Write-Host "- Review the metrics in chair_pose_metrics.csv" -ForegroundColor White
Write-Host "- Check the confusion matrix visualization" -ForegroundColor White
Write-Host "- Integrate the trained model with your web application" -ForegroundColor White

Read-Host "`nPress Enter to continue..."
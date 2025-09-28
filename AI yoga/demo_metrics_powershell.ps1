# Chair Pose Classification Metrics Demo (PowerShell Version)
# Demonstrates F1 Score, Precision, Accuracy, and Recall calculations

Write-Host "🧘 Chair Pose Classification - Metrics Demo" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Simulate realistic test data for chair pose classification
Write-Host "`n📊 SIMULATED TEST SCENARIO" -ForegroundColor Yellow
Write-Host "- Total test images: 100" -ForegroundColor White
Write-Host "- Actual chair poses: 40" -ForegroundColor White  
Write-Host "- Actual other poses: 60" -ForegroundColor White

# Define confusion matrix values (simulating realistic model performance)
$TruePositives = 37    # Chair poses correctly identified
$FalsePositives = 4    # Other poses wrongly identified as chair poses
$TrueNegatives = 56    # Other poses correctly identified
$FalseNegatives = 3    # Chair poses missed by model

Write-Host "`n🔢 CONFUSION MATRIX" -ForegroundColor Yellow
Write-Host "                  PREDICTED" -ForegroundColor Gray
Write-Host "                Chair  Other" -ForegroundColor Gray
Write-Host "ACTUAL Chair     $TruePositives      $FalseNegatives" -ForegroundColor White
Write-Host "       Other     $FalsePositives     $TrueNegatives" -ForegroundColor White

# Calculate metrics
$Accuracy = ($TruePositives + $TrueNegatives) / ($TruePositives + $TrueNegatives + $FalsePositives + $FalseNegatives)
$Precision = $TruePositives / ($TruePositives + $FalsePositives)
$Recall = $TruePositives / ($TruePositives + $FalseNegatives)
$F1Score = 2 * ($Precision * $Recall) / ($Precision + $Recall)

# Display results with explanations
Write-Host "`n📊 EVALUATION METRICS RESULTS" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

Write-Host "🎯 ACCURACY:   $($Accuracy.ToString('F4')) ($($($Accuracy * 100).ToString('F2'))%%)" -ForegroundColor White
Write-Host "   → Overall correctness: (TP + TN) / Total = ($TruePositives + $TrueNegatives) / 100" -ForegroundColor Gray

Write-Host "`n🔍 PRECISION:  $($Precision.ToString('F4')) ($($($Precision * 100).ToString('F2'))%)" -ForegroundColor White
Write-Host "   → Chair pose detection quality: TP / (TP + FP) = $TruePositives / ($TruePositives + $FalsePositives)" -ForegroundColor Gray
Write-Host "   → Of all chair pose predictions, $($($Precision * 100).ToString('F1'))% were correct" -ForegroundColor Gray

Write-Host "`n📈 RECALL:     $($Recall.ToString('F4')) ($($($Recall * 100).ToString('F2'))%)" -ForegroundColor White
Write-Host "   → Chair pose detection coverage: TP / (TP + FN) = $TruePositives / ($TruePositives + $FalseNegatives)" -ForegroundColor Gray
Write-Host "   → Of all actual chair poses, $($($Recall * 100).ToString('F1'))% were detected" -ForegroundColor Gray

Write-Host "`n⚖️  F1 SCORE:   $($F1Score.ToString('F4')) ($($($F1Score * 100).ToString('F2'))%)" -ForegroundColor White
Write-Host "   → Balanced measure: 2 × (Precision × Recall) / (Precision + Recall)" -ForegroundColor Gray
Write-Host "   → Formula: 2 × ($($Precision.ToString('F3')) × $($Recall.ToString('F3'))) / ($($Precision.ToString('F3')) + $($Recall.ToString('F3')))" -ForegroundColor Gray

# Performance interpretation
Write-Host "`n🏆 PERFORMANCE INTERPRETATION" -ForegroundColor Magenta
Write-Host "=" * 50 -ForegroundColor Magenta

$QualityLevel = if ($F1Score -gt 0.9) { "Excellent" } elseif ($F1Score -gt 0.8) { "Good" } elseif ($F1Score -gt 0.7) { "Moderate" } else { "Needs Improvement" }
$QualityColor = if ($F1Score -gt 0.8) { "Green" } elseif ($F1Score -gt 0.7) { "Yellow" } else { "Red" }

Write-Host "Model Quality: $QualityLevel" -ForegroundColor $QualityColor

# Detailed breakdown
Write-Host "`n🔍 DETAILED BREAKDOWN" -ForegroundColor Yellow
Write-Host "True Positives (TP):  $TruePositives - Chair poses correctly identified" -ForegroundColor Green
Write-Host "True Negatives (TN):  $TrueNegatives - Other poses correctly identified" -ForegroundColor Green  
Write-Host "False Positives (FP): $FalsePositives - Other poses wrongly identified as chair pose" -ForegroundColor Red
Write-Host "False Negatives (FN): $FalseNegatives - Chair poses missed by the model" -ForegroundColor Red

# Create CSV data
$MetricsData = @{
    'Metric' = @('Accuracy', 'Precision', 'Recall', 'F1_Score')
    'Value' = @($Accuracy, $Precision, $Recall, $F1Score)
    'Percentage' = @("$($($Accuracy * 100).ToString('F2'))%", "$($($Precision * 100).ToString('F2'))%", "$($($Recall * 100).ToString('F2'))%", "$($($F1Score * 100).ToString('F2'))%")
    'Formula' = @(
        "(TP + TN) / Total",
        "TP / (TP + FP)", 
        "TP / (TP + FN)",
        "2 × (Precision × Recall) / (Precision + Recall)"
    )
}

# Save to CSV
$CsvContent = "Metric,Value,Percentage,Formula`n"
for ($i = 0; $i -lt $MetricsData.Metric.Length; $i++) {
    $CsvContent += "$($MetricsData.Metric[$i]),$($MetricsData.Value[$i].ToString('F4')),$($MetricsData.Percentage[$i]),$($MetricsData.Formula[$i])`n"
}

$CsvContent | Out-File -FilePath "demo_chair_pose_metrics.csv" -Encoding UTF8
Write-Host "`n💾 Metrics saved to 'demo_chair_pose_metrics.csv'" -ForegroundColor Green

# Explain what each metric means in practical terms
Write-Host "`n📚 PRACTICAL INTERPRETATION" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

Write-Host "`n🎯 What does ACCURACY mean?" -ForegroundColor White
Write-Host "   - Out of 100 test images, the model got $($($Accuracy * 100).ToString('F0')) correct" -ForegroundColor Gray
Write-Host "   - This includes both chair poses and other poses" -ForegroundColor Gray

Write-Host "`n🔍 What does PRECISION mean?" -ForegroundColor White
Write-Host "   - When the model says 'chair pose', it's right $($($Precision * 100).ToString('F0'))% of the time" -ForegroundColor Gray
Write-Host "   - Low precision = many false alarms" -ForegroundColor Gray

Write-Host "`n📈 What does RECALL mean?" -ForegroundColor White
Write-Host "   - The model finds $($($Recall * 100).ToString('F0'))% of all actual chair poses" -ForegroundColor Gray
Write-Host "   - Low recall = missing many chair poses" -ForegroundColor Gray

Write-Host "`n⚖️ What does F1 SCORE mean?" -ForegroundColor White
Write-Host "   - Balanced score combining precision and recall" -ForegroundColor Gray
Write-Host "   - Single metric to judge overall performance" -ForegroundColor Gray

# Show training recommendations
Write-Host "`n🚀 TRAINING RECOMMENDATIONS" -ForegroundColor Yellow
Write-Host "=" * 50 -ForegroundColor Yellow

if ($F1Score -gt 0.9) {
    Write-Host "✅ Excellent performance! Model is ready for production." -ForegroundColor Green
} elseif ($F1Score -gt 0.8) {
    Write-Host "✅ Good performance! Consider minor improvements." -ForegroundColor Green
} elseif ($F1Score -gt 0.7) {
    Write-Host "⚠️  Moderate performance. Consider:" -ForegroundColor Yellow
    Write-Host "   - Adding more training data" -ForegroundColor Gray
    Write-Host "   - Improving data quality" -ForegroundColor Gray
    Write-Host "   - Adjusting model architecture" -ForegroundColor Gray
} else {
    Write-Host "❌ Needs improvement. Consider:" -ForegroundColor Red
    Write-Host "   - Collecting more diverse training data" -ForegroundColor Gray
    Write-Host "   - Using data augmentation techniques" -ForegroundColor Gray
    Write-Host "   - Trying different model architectures" -ForegroundColor Gray
}

Write-Host "`n🎉 DEMO COMPLETED!" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green
Write-Host "This demo shows how your actual model will be evaluated." -ForegroundColor White
Write-Host "When you train with real yoga pose images, you'll get similar" -ForegroundColor White
Write-Host "detailed metrics for chair pose classification!" -ForegroundColor White

Write-Host "`n📋 Files created:" -ForegroundColor Cyan
Write-Host "- demo_chair_pose_metrics.csv (detailed metrics)" -ForegroundColor Gray

Write-Host "`n🔄 Next Steps:" -ForegroundColor Cyan  
Write-Host "1. Install Python: https://python.org/downloads/" -ForegroundColor Gray
Write-Host "2. Run: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "3. Execute: python chair_pose_classifier.py" -ForegroundColor Gray
Write-Host "4. Get real metrics: python evaluate_metrics.py" -ForegroundColor Gray

Read-Host "`nPress Enter to continue..."
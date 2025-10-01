# Models Directory

This directory contains trained models and model-related files for the SIH PS1 Cybersecurity Threat Detector.

## Structure

```
models/
├── README.md                    # This file
├── checkpoints/                 # Model checkpoints during training
├── trained/                     # Final trained models
│   ├── text_classifier.pkl     # Text classification model
│   ├── url_classifier.pkl      # URL classification model
│   └── ensemble_model.pkl      # Combined ensemble model
├── configs/                     # Model configuration files
│   ├── text_model_config.json  # Text model parameters
│   └── url_model_config.json   # URL model parameters
└── metrics/                     # Model performance metrics
    ├── training_history.json   # Training history
    └── evaluation_results.json # Evaluation metrics
```

## Model Types

### 1. Text Classification Model
- **Purpose**: Detect phishing in text content
- **Algorithm**: Random Forest / LSTM
- **Features**: TF-IDF, N-grams, Custom features
- **Performance**: Target >85% accuracy

### 2. URL Classification Model
- **Purpose**: Analyze URL safety
- **Algorithm**: Feature-based classifier
- **Features**: Domain analysis, Pattern matching
- **Performance**: Target >80% accuracy

### 3. Ensemble Model
- **Purpose**: Combine text and URL analysis
- **Algorithm**: Weighted voting
- **Features**: Combined predictions
- **Performance**: Target >90% accuracy

## Usage

```python
import pickle
from pathlib import Path

# Load trained model
model_path = Path("models/trained/text_classifier.pkl")
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Make predictions
prediction = model.predict(features)
```

## Training

Models are trained using the notebooks in the `notebooks/` directory:

1. `threat_analysis_experiments.ipynb` - Data exploration and feature engineering
2. `model_training.ipynb` - Model training and evaluation
3. `model_comparison.ipynb` - Compare different algorithms

## Model Versioning

- Use semantic versioning (v1.0.0, v1.1.0, etc.)
- Save models with version tags
- Keep training logs and metrics for each version

## Performance Targets

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Text  | >85%     | >80%      | >85%   | >82%     |
| URL   | >80%     | >75%      | >80%   | >77%     |
| Ensemble | >90%  | >85%      | >90%   | >87%     |

## Deployment

Models are loaded by the Flask application in `backend/app.py` for real-time inference.

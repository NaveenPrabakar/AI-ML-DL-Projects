# Titanic Survival Prediction

A machine learning project that predicts passenger survival on the Titanic using various classification algorithms and feature engineering techniques.

## Overview

This project analyzes the famous Titanic dataset to predict passenger survival based on features like age, sex, passenger class, fare, and family relationships. The analysis includes data preprocessing, feature engineering, multiple machine learning models, and comprehensive evaluation.

## Dataset

The project uses the Titanic dataset from Kaggle, which contains:
- **Training set**: 891 passengers with survival outcomes
- **Test set**: 418 passengers without survival outcomes (for predictions)

### Key Features
- `PassengerId`: Unique identifier for each passenger
- `Survived`: Target variable (0 = No, 1 = Yes)
- `Pclass`: Passenger class (1st, 2nd, 3rd)
- `Name`: Passenger name
- `Sex`: Gender
- `Age`: Age in years
- `SibSp`: Number of siblings/spouses aboard
- `Parch`: Number of parents/children aboard
- `Ticket`: Ticket number
- `Fare`: Passenger fare
- `Cabin`: Cabin number
- `Embarked`: Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)

## Data Preprocessing

### Missing Value Handling
- **Age**: Filled with median age
- **Embarked**: Filled with most frequent value (mode)
- **Fare**: Filled with median fare
- **Cabin**: Dropped due to excessive missing values (>75%)

### Categorical Encoding
- **Sex**: Male = 0, Female = 1
- **Embarked**: C = 0, Q = 1, S = 2
- **Title**: Extracted from names and encoded using LabelEncoder

### Feature Engineering

#### Created Features
1. **FamilySize**: `SibSp + Parch + 1`
2. **IsAlone**: Binary indicator for solo travelers
3. **Age Groups**: Categorized age into life stages (Child, Teen, Young Adult, etc.)
4. **Fare Groups**: Quartile-based fare categories
5. **Title**: Extracted titles from names (Mr, Mrs, Miss, Master, Rare)
6. **Age*Pclass**: Interaction feature between age and passenger class

#### Dropped Features
- `Name`, `Ticket`, `PassengerId`: Non-predictive identifiers
- `Cabin`: Too many missing values

## Machine Learning Models

### 1. Random Forest Classifier
- **Base Model**: 100 estimators, achieved ~82% accuracy
- **Optimized Model**: 200 estimators with tuned hyperparameters
  - `max_depth=10`
  - `min_samples_leaf=2`
  - `min_samples_split=2`

### 2. Logistic Regression
- Simple baseline model for comparison
- Achieved competitive accuracy for interpretability

### 3. XGBoost Classifier (Final Model)
- **Hyperparameters**:
  - `n_estimators=300`
  - `max_depth=7`
  - `learning_rate=0.05`
  - `subsample=0.8`
  - `colsample_bytree=0.8`
  - `gamma=1`
  - `min_child_weight=2`

## Feature Selection

Used SHAP (SHapley Additive exPlanations) for interpretable feature importance:
- Selected top 8 most important features
- Provides explainable AI insights into model decisions
- Helps identify which features contribute most to survival predictions

## Model Evaluation

### Cross-Validation
- 5-fold cross-validation for robust accuracy estimation
- Prevents overfitting and provides confidence intervals

### Performance Metrics
- **Accuracy**: Primary metric for model comparison
- **Final Model Accuracy**: ~84% on validation set
- **Cross-validated Accuracy**: Consistent performance across folds

## Visualizations

The project includes several exploratory data analysis visualizations:

1. **Survival Distribution**: Shows class imbalance in target variable
2. **Age Distribution**: Histogram with KDE overlay
3. **Fare Distribution**: Right-skewed distribution analysis
4. **Embarked vs Survival**: Categorical relationship analysis

## Installation & Usage

### Requirements
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
```

### Running the Project
1. Download the Titanic dataset from Kaggle
2. Update file paths in the notebook
3. Run all cells sequentially
4. The final model will generate `submission.csv` for Kaggle submission

## Results

- **Best Model**: XGBoost Classifier
- **Validation Accuracy**: ~84%
- **Cross-validation Score**: Consistent performance
- **Key Insights**: 
  - Gender was the strongest predictor
  - Passenger class and fare were important socioeconomic indicators
  - Family size and age showed complex relationships with survival

## Future Improvements

The author identified several areas for enhancement:

1. **Advanced Preprocessing**:
   - One-hot encoding for categorical variables
   - More sophisticated missing value imputation

2. **Model Optimization**:
   - Hyperparameter tuning with Grid/Random Search
   - Ensemble methods combining multiple models

3. **Feature Engineering**:
   - More domain-specific features
   - Polynomial features and interactions

4. **Validation**:
   - Stratified cross-validation
   - Learning curves analysis

## Project Structure

```
titanic-survival-prediction/
├── naveen-prabakar-titanics.ipynb    # Main analysis notebook
├── train.csv                         # Training dataset
├── test.csv                          # Test dataset
├── submission.csv                    # Final predictions
└── README.md                         # This file
```

## Author

Naveen Prabakar - Data Science Student

## Acknowledgments

- Kaggle for providing the Titanic dataset
- Professor recommendations for XGBoost implementation
- Previous DS 201 coursework experience
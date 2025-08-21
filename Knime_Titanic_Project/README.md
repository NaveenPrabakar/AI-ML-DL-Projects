# KNIME Machine Learning Pipeline

A comprehensive machine learning workflow built in KNIME Analytics Platform for data preprocessing, model training, and evaluation using multiple algorithms including Logistic Regression, Random Forest, and Support Vector Machine (SVM).

## Overview

This project demonstrates a complete machine learning pipeline using KNIME's visual workflow interface. The workflow includes data ingestion, preprocessing, feature engineering, model training with multiple algorithms, and comprehensive model evaluation and comparison.

## Workflow Architecture

### 1. Data Input and Exploration
- **CSV Reader**: Loads the training dataset
- **Data Visualization**: 
  - Histogram of Pages for data distribution analysis
  - Age Bar Chart for demographic insights
  - Line Plot of Age vs Fare for correlation analysis

### 2. Data Preprocessing Pipeline

#### Missing Value Treatment
- **Missing Value**: Identifies missing data points
- **One to Many**: Handles data splitting for parallel processing
- **Math Formula**: Custom calculations for feature derivation
- **Column Filter**: Selects relevant features
- **Number to String** & **Normalizer**: Data type conversion and feature scaling

#### Feature Engineering
- **Applied Feature Engineering**: Custom feature creation and transformation
- **Dropped columns**: Removes irrelevant features (PassengerId, etc.)
- **Normalized Age and Fare**: Scales continuous variables for better model performance
- **Better scaling purposes**: Ensures all features are on similar scales

### 3. Data Splitting and Partitioning
- **Partitioning**: Splits data into training (80%) and testing (20%) sets
- **80:20 split**: Standard practice for model validation
- **25% test**: Additional validation split for robust evaluation

## Machine Learning Models

### 1. Logistic Regression
- **Logistic Regression Learner**: Trains binary classification model
- **Logistic Regression Predictor**: Generates predictions
- **Scorer**: Evaluates model performance
- Best for interpretable linear relationships

### 2. K-Nearest Neighbors (KNN)
- **K Nearest Neighbor**: Instance-based learning algorithm
- **Scorer**: Performance evaluation
- Good for non-linear patterns and local relationships

### 3. Random Forest
- **Random Forest Learner**: Ensemble method with decision trees
- **Random Forest Predictor**: Prediction generation
- **Scorer**: Model evaluation
- **Best Model**: Identified as highest performing algorithm
- Excellent for handling mixed data types and feature interactions

### 4. Support Vector Machine (SVM)
- **SVM Learner**: Trains support vector classifier
- **SVM Predictor**: Generates predictions
- **SVM Score**: Performance metrics
- Effective for high-dimensional data and complex boundaries

## Model Evaluation and Comparison

### Performance Metrics
- **Scorer Nodes**: Calculate accuracy, precision, recall, and F1-score
- **Model Comparison**: Side-by-side evaluation of all algorithms
- **Best Model Selection**: Random Forest identified as optimal performer

### Visualization and Reporting
- **Concatenate**: Combines results from multiple models
- **Table View**: Displays comprehensive results
- **Accuracy Comparison**: "ADG everything together" for final assessment

### Output Generation
- **Column Renamer**: Standardizes output format
- **CSV Writer**: Exports final predictions
- **Write out the submission file**: Creates competition-ready output

## Key Features

### Data Quality Assurance
- Comprehensive missing value handling
- Feature scaling and normalization
- Data type optimization

### Feature Engineering
- Custom mathematical transformations
- Feature selection based on relevance
- Scaling for optimal model performance

### Model Robustness
- Multiple algorithm comparison
- Cross-validation through data splitting
- Performance metric standardization

### Automated Pipeline
- End-to-end workflow automation
- Reproducible results
- Easy parameter modification

## Technical Implementation

### KNIME Workflow Components
1. **Data Input**: CSV Reader nodes for dataset ingestion
2. **Preprocessing**: Missing value treatment, normalization, feature engineering
3. **Model Training**: Multiple ML algorithm implementations
4. **Evaluation**: Comprehensive scoring and comparison framework
5. **Output**: Prediction export and submission file generation

### Workflow Benefits
- **Visual Programming**: No coding required
- **Modular Design**: Easy component modification
- **Scalable Architecture**: Can handle larger datasets
- **Reproducible Results**: Consistent execution across runs

## Results and Performance

### Model Rankings
1. **Random Forest**: Best overall performance
2. **Logistic Regression**: Good baseline with interpretability
3. **SVM**: Strong performance on complex patterns
4. **KNN**: Effective for local pattern recognition

### Key Insights
- Feature engineering significantly improved model performance
- Ensemble methods (Random Forest) outperformed single algorithms
- Proper data preprocessing was crucial for optimal results
- Model comparison revealed algorithm-specific strengths

## Usage Instructions

### Prerequisites
- KNIME Analytics Platform (version 4.0+)
- Sufficient memory for dataset processing
- Input dataset in CSV format

### Running the Workflow
1. Open KNIME Analytics Platform
2. Import the workflow file (.knwf)
3. Configure CSV Reader with your dataset path
4. Execute workflow sequentially or run all nodes
5. Check results in Table View and Scorer nodes
6. Export predictions using CSV Writer

### Customization Options
- **Algorithm Parameters**: Adjust hyperparameters in learner nodes
- **Data Splitting**: Modify partition ratios
- **Feature Engineering**: Add custom Math Formula nodes
- **Evaluation Metrics**: Configure different scoring methods

## File Structure

```
knime-ml-pipeline/
├── workflow.knwf                 # Main KNIME workflow file
├── data/
│   ├── train.csv                # Training dataset
│   └── test.csv                 # Test dataset
├── output/
│   ├── predictions.csv          # Model predictions
│   └── model_comparison.csv     # Performance metrics
└── README.md                    # This file
```

## Performance Metrics

### Evaluation Criteria
- **Accuracy**: Overall prediction correctness
- **Precision**: True positive rate
- **Recall**: Sensitivity measure
- **F1-Score**: Harmonic mean of precision and recall
- **Cross-validation**: Robust performance estimation

### Model Comparison Results
- Comprehensive scoring across all algorithms
- Statistical significance testing
- Performance consistency across validation sets

## Future Enhancements

### Potential Improvements
1. **Hyperparameter Optimization**: Grid search for optimal parameters
2. **Feature Selection**: Automated feature importance analysis
3. **Ensemble Methods**: Combine multiple models for better performance
4. **Deep Learning**: Integration with neural network nodes
5. **Real-time Scoring**: Deploy models for live predictions

### Advanced Analytics
- **Model Interpretability**: SHAP values integration
- **Bias Detection**: Fairness analysis across demographic groups
- **A/B Testing**: Statistical comparison framework
- **Time Series**: Temporal pattern analysis capabilities

## Technical Requirements

### System Specifications
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 500MB for workflow and temporary files
- **OS**: Windows, macOS, or Linux
- **Java**: Version 11 or higher

### KNIME Extensions
- **Analytics Platform**: Core functionality
- **Machine Learning**: ML algorithm implementations
- **Statistics**: Advanced statistical functions
- **Visualization**: Enhanced plotting capabilities

## Contributing

This workflow serves as a template for machine learning projects in KNIME. Contributions for improvements, additional algorithms, or enhanced visualizations are welcome.

## License

This project is provided as an educational resource for learning KNIME and machine learning workflows.

## Acknowledgments

- KNIME Analytics Platform for providing the visual programming environment
- Open-source machine learning community for algorithm implementations
- Educational institutions for promoting hands-on learning approaches
# Housing Price Prediction 🏠
### KNIME Machine Learning Project
**Team Members**: Naveen, Greg, Riza  
**Achievement**: 🥉 **3rd Place Winner** in Class Competition

---

## 🎯 Project Overview

A comprehensive machine learning project that predicts housing prices using advanced feature engineering, multiple algorithms, and hyperparameter optimization in KNIME Analytics Platform. This regression analysis achieved a Kaggle score of **0.19** and earned 3rd place recognition in class.

## 📊 Dataset Overview

### Data Characteristics
- **Data Types**: Mixed dataset containing both numerical and categorical features
- **Target Variable**: Sale Price (continuous) - **Regression Problem**
- **Challenge**: Training and test sets had different data types for some columns
- **Data Quality**: Significant missing values across multiple columns

### Key Data Insights
- **Housing Era**: Most houses built between **1960-2010**
- **Market Segment**: Higher-end housing market bias due to modern construction
- **Geographic Distribution**: Uneven neighborhood representation
- **Price Patterns**: Strong correlation between living area and price up to ~4000 sq ft

## 🔍 Exploratory Data Analysis

### Temporal Analysis
- **Construction Period**: Concentration of houses from 1960-2010
- **Market Implications**: Dataset skewed toward modern, higher-value properties
- **Potential Bias**: Limited representation of older housing stock

### Spatial Analysis
- **Ground Living Area vs Price**: Strong positive correlation with high variability
- **Sweet Spot**: Most properties clustered around 1000-2000 sq ft range
- **Prediction Challenge**: High variability beyond 4000 sq ft area

### Neighborhood Analysis
- **Distribution**: Generally even sale price distribution across neighborhoods
- **Data Imbalance**: Some neighborhoods (e.g., N Ames) severely underrepresented
- **Box Plot Insights**: Consistent median prices with varying quartile ranges

## 🛠️ Data Preprocessing Pipeline

### Missing Value Treatment
```
Strategy by Data Type:
├── Numerical Columns → Median Imputation
├── Categorical Columns → Mode Imputation
└── High Missing Rate → Column Removal
```

### Data Cleaning Steps
1. **Missing Value Imputation**:
   - Numerical features: Filled with median values
   - Categorical features: Filled with mode (most frequent value)

2. **Column Elimination**:
   - Dropped high-missing columns: `Alley`, `MiscValue`, etc.
   - Removed features with >50% missing data

3. **Encoding Process**:
   - Applied Label Encoding to categorical variables
   - Dropped original string columns post-encoding
   - Ensured consistent data types across train/test sets

## ⚙️ Feature Engineering

### Correlation Analysis
**Top Correlations with Sale Price:**
- **Overall Quality**: 0.79 (strongest predictor)
- **Ground Living Area**: 0.781 (size matters)
- **1st Floor Square Feet**: 0.6 (foundation importance)

### Custom Feature Creation
1. **HouseAge**: `Current Year - Year Built`
2. **YearsSinceRemodel**: `Current Year - Remodel Date`
3. **Total Bathrooms**: `Full Bathrooms + 0.5 × Half Bathrooms`
4. **Living Area Ratio**: `Ground Living Area / Total Lot Area`

### Data Transformation
- **Log Transformation**: Applied to skewed variables for normal distribution
- **Outlier Handling**: Log scaling helped manage extreme values
- **Distribution Normalization**: Improved model performance and convergence

## 🤖 Machine Learning Implementation

### Data Partitioning
- **Training Set**: 80% of data
- **Testing Set**: 20% of data
- **Validation Strategy**: Holdout method with random sampling

### Model Portfolio

#### 1. Linear Regression 📈
- **Type**: Simple linear model
- **Advantages**: Interpretable, fast training
- **Use Case**: Baseline model and final selection

#### 2. Random Forest 🌲
- **Type**: Ensemble method with decision trees
- **Advantages**: Handles non-linearity, feature interactions
- **Configuration**: Optimized with 1,000 estimators

#### 3. Gradient Boosting 🚀
- **Type**: Sequential ensemble method
- **Advantages**: High accuracy, handles complex patterns
- **Configuration**: 1,000 models with tuned tree depth

#### 4. Additional Models (Cross-validation)
- **Simple Tree**: Baseline comparison (worst performer)
- **Tree Ensemble**: Performance comparable to Random Forest

### Hyperparameter Optimization

#### Key Optimizations
- **Number of Estimators**: Increased to 1,000 for ensemble methods
- **Tree Depth**: Systematically tested various depth levels
- **Performance Impact**: Higher model counts significantly improved accuracy

#### Optimization Results
- **Finding**: More estimators → Higher accuracy
- **Trade-off**: Computational cost vs performance gain
- **Sweet Spot**: 1,000 estimators provided optimal balance

## 📈 Results & Performance

### Model Comparison: Before vs After Optimization

#### Performance Metrics (R² Score)
| Model | Before Optimization | After Optimization | Improvement |
|-------|-------------------|-------------------|------------|
| **Linear Regression** | Baseline | **Best Overall** | ✅ Winner |
| **Gradient Boosting** | Good | Excellent | 📈 Significant |
| **Random Forest** | Good | Very Good | 📈 Moderate |

### Final Model Selection
**🏆 Winner: Linear Regression**
- **Rationale**: Best overall attributes across evaluation metrics
- **Performance**: Consistent and reliable predictions
- **Interpretability**: Easy to understand and explain
- **Robustness**: Stable performance across different data subsets

### Competition Results
- **Kaggle Score**: **0.19** 🎯
- **Class Ranking**: **3rd Place** 🥉
- **Achievement**: Top-tier performance among student submissions

## 🔧 Technical Implementation

### KNIME Workflow Architecture
```
Data Input → Preprocessing → Feature Engineering → Model Training → Evaluation
     ↓             ↓              ↓                ↓              ↓
CSV Reader → Missing Values → Correlation → ML Algorithms → Numeric Scorer
           → Encoding      → New Features → Hypertuning  → Comparison
           → Cleaning      → Transform    → Validation   → Selection
```

### Workflow Components
1. **Data Ingestion**: CSV Reader nodes
2. **Preprocessing**: Missing value nodes, encoders
3. **Feature Engineering**: Math Formula, Column operations
4. **Model Training**: Learner nodes for each algorithm
5. **Evaluation**: Numeric Scorer, model comparison
6. **Output**: Predictions and performance metrics

## 💡 Key Insights & Learnings

### Data Science Insights
1. **Feature Engineering Impact**: Custom features significantly improved performance
2. **Model Selection**: Sometimes simpler models (Linear Regression) outperform complex ones
3. **Data Quality**: Proper preprocessing is crucial for model success
4. **Hyperparameter Tuning**: Systematic optimization pays dividends

### Domain Knowledge
1. **Housing Market**: Overall quality is the strongest price predictor
2. **Size Matters**: Living area strongly correlates with price
3. **Age Factor**: House age and remodeling history affect valuation
4. **Location**: Neighborhood differences require careful handling

### Technical Learnings
1. **KNIME Proficiency**: Advanced workflow design and optimization
2. **Ensemble Methods**: Understanding when and how to use different algorithms
3. **Feature Engineering**: Creating meaningful derived variables
4. **Model Evaluation**: Comprehensive comparison methodologies

## 🚀 Usage Instructions

### Prerequisites
- KNIME Analytics Platform 4.0+
- Housing dataset (train.csv, test.csv)
- Minimum 8GB RAM recommended

### Running the Project
1. **Setup**: Import KNIME workflow file
2. **Data**: Configure CSV Reader paths
3. **Execute**: Run complete workflow or step-by-step
4. **Results**: Check Numeric Scorer outputs
5. **Export**: Generate final predictions

### Customization Options
- **Feature Engineering**: Add new derived features
- **Hyperparameters**: Adjust model parameters
- **Algorithms**: Try additional ML methods
- **Validation**: Implement cross-validation

## 📁 Project Structure

```
housing-prediction-knime/
├── workflow.knwf              # Main KNIME workflow
├── data/
│   ├── train.csv             # Training dataset
│   ├── test.csv              # Test dataset
│   └── sample_submission.csv # Submission format
├── results/
│   ├── predictions.csv       # Final predictions
│   ├── model_scores.csv      # Performance metrics
│   └── feature_importance.csv # Feature analysis
├── presentation/
│   └── Housing-Presentation.pdf # Project presentation
└── README.md                 # This documentation
```

## 🏆 Awards & Recognition

### Class Competition Results
- **🥉 3rd Place** out of all student teams
- **Kaggle Score**: 0.19 (competitive performance)
- **Recognition**: Outstanding feature engineering and model selection

### What Made This Project Stand Out
1. **Comprehensive EDA**: Thorough data exploration and visualization
2. **Strategic Feature Engineering**: Data-driven feature creation
3. **Model Diversity**: Systematic comparison of multiple algorithms
4. **Optimization**: Rigorous hyperparameter tuning
5. **Clear Documentation**: Well-structured presentation and analysis

## 🔮 Future Enhancements

### Advanced Techniques
1. **Ensemble Stacking**: Combine multiple models for better predictions
2. **Cross-Validation**: Implement k-fold validation
3. **Feature Selection**: Automated feature importance ranking
4. **Neural Networks**: Deep learning approaches
5. **Time Series**: Incorporate temporal market trends

### Data Improvements
1. **External Data**: Economic indicators, market trends
2. **Geospatial Features**: Location-based variables
3. **Image Analysis**: Property photos for additional insights
4. **Real-time Data**: Current market conditions

## 👥 Team Contributions

### Collaborative Excellence
- **Naveen**: Feature engineering and model optimization
- **Greg**: Data preprocessing and visualization
- **Riza**: Model evaluation and presentation

### Teamwork Success Factors
- **Clear Division**: Each member owned specific components
- **Regular Communication**: Consistent progress updates
- **Peer Review**: Cross-validation of approaches
- **Shared Learning**: Knowledge transfer across team

## 📚 References & Resources

### Tools & Technologies
- KNIME Analytics Platform
- Kaggle Housing Dataset
- Statistical and ML algorithms

### Learning Resources
- KNIME Documentation and Tutorials
- Machine Learning Best Practices
- Feature Engineering Techniques
- Model Evaluation Methodologies

---

## 🎉 Conclusion

This housing price prediction project demonstrates the power of systematic data science methodology using KNIME's visual programming environment. Through careful data exploration, strategic feature engineering, and comprehensive model evaluation, we achieved competitive performance and earned 3rd place recognition.

The project showcases not just technical proficiency, but also the importance of domain knowledge, teamwork, and clear communication in successful data science projects.

**Final Achievement: Kaggle Score of 0.19 and 3rd Place Class Recognition** 🏆
# BizLens v2.0.0

**Integrated Analytics Platform — Descriptive, Diagnostic & Predictive Analytics with Sample vs Population Distinction**

[![PyPI version](https://img.shields.io/pypi/v/bizlens)](https://pypi.org/project/bizlens/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

---

## 🎯 What is BizLens?

BizLens is a **comprehensive analytics platform** for business and educational use, featuring:

- **Descriptive Analytics**: What happened? (statistics, distributions, visualizations)
- **Diagnostic Analytics**: Why did it happen? (correlations, hypothesis testing, assumptions)
- **Predictive Analytics**: What will happen? (regression, forecasting, confidence intervals)
- **Sample vs Population**: Explicit distinction throughout (n-1 vs n denominator)

Designed for **High School → Undergraduate → Postgraduate** students and professionals.

---

## ✨ Key Features

### 📊 Descriptive Analytics
- Central tendency: Mean, Median, Mode
- Dispersion: Range, Variance, Standard Deviation, IQR
- Distribution analysis: Skewness, Kurtosis
- 9+ visualization types (histogram, boxplot, violin, density, heatmap, etc.)
- Professional color schemes (Academic, Pastel, Vibrant)

### 🔍 Diagnostic Analytics
- Hypothesis testing (t-tests, ANOVA, chi-square)
- Correlation analysis (Pearson, Spearman)
- Assumption checking (normality, linearity, homoscedasticity)
- Segment analysis and comparisons
- Effect size and statistical significance

### 🔮 Predictive Analytics
- Linear regression (simple & multiple)
- Time series forecasting with seasonality
- Logistic regression (binary classification)
- Confidence intervals & uncertainty quantification
- Cross-validation and model evaluation
- Diagnostic plots (residuals, Q-Q plots)

### 📚 Educational Excellence
- Sample vs population distinction in all calculations
- Mathematical notation and formulas
- Real datasets with proper citations (Iris, Titanic, Gapminder, World Bank)
- Jupyter notebook templates (12-section standardized structure)
- Python fundamentals integrated throughout
- Skill-level progression (Basics → Intermediate → Advanced)

### 🎓 Real Data Integration
- Built-in sample datasets with citations
- World Bank API integration (with caching)
- Dataset metadata and quality reports
- Reproducibility and provenance tracking

---

## 🚀 Quick Start

### Installation

```bash
pip install bizlens==2.0.0
```

### Basic Example

```python
import bizlens as bl
import pandas as pd

# Load data
data = bl.load_dataset('iris')

# Describe (Sample-level statistics)
stats = bl.describe(data['sepal_length'], calculation_level='sample')
print(stats)

# Diagnose (Hypothesis test)
t_stat, p_value = bl.test.compare_groups(
    data[data['species']=='setosa']['sepal_length'],
    data[data['species']=='versicolor']['sepal_length']
)

# Predict (Linear regression)
prediction = bl.predict.regression.simple(
    x=data['sepal_length'],
    y=data['petal_length'],
    confidence_interval=0.95
)
```

---

## 📚 Learning Pathways

### For Business Analytics
- Sales forecasting with seasonal decomposition
- Customer segmentation and profiling
- Marketing effectiveness analysis
- Revenue prediction and ROI estimation

### For Data Science
- Statistical foundations
- Hypothesis testing workflows
- Regression model development
- Time series analysis and forecasting

### For Academic Research
- Rigorous statistical methods
- Publication-ready visualizations
- Assumption validation
- Effect size and confidence intervals

---

## 🎯 Sample vs Population

A core pedagogical principle throughout BizLens:

```python
# Sample (your dataset)
sample_stats = bl.describe(data, calculation_level='sample')  # Uses n-1

# Population (all possible values)
pop_stats = bl.describe(data, calculation_level='population')  # Uses n

# Compare both
bl.compare_sample_population(data)
```

---

## 🔧 API Overview

### Descriptive Analytics
```python
bl.describe(data)                    # Comprehensive statistics
bl.visualize.histogram(data)         # 9+ visualization types
bl.datasets.load_dataset('iris')     # Real datasets with citations
```

### Diagnostic Analytics
```python
bl.test.hypothesis(data1, data2)     # Hypothesis testing
bl.correlation.pearson(data)         # Correlations
bl.assumptions.normality(data)       # Assumption checking
```

### Predictive Analytics
```python
bl.predict.regression.simple(x, y)   # Simple linear regression
bl.predict.forecast(timeseries)      # Time series forecasting
bl.predict.classify.logistic(X, y)   # Logistic regression
```

---

## 📖 Documentation & Examples

- **Quick Start**: 15 minutes to first analysis
- **Notebooks**: 12-section templates for all use cases
- **API Reference**: Complete function documentation
- **Roadmap**: v2.1+ will add ML foundations (decision trees, random forests, clustering)

---

## 🛣️ Roadmap

**v2.0.0** (Current) - Integrated Analytics Platform
- ✅ Descriptive, diagnostic & predictive analytics
- ✅ Sample vs population distinction
- ✅ Real data integration
- ✅ Educational focus

**v2.1** (Q3 2026) - ML Foundations
- Classification (decision trees, random forests, naive bayes)
- Clustering (K-means, hierarchical, DBSCAN)
- Dimensionality reduction (PCA, feature selection)
- AutoML basics

**v2.2** (Q4 2026) - Advanced ML
- Ensemble methods (XGBoost, LightGBM, stacking)
- Advanced time series (ARIMA, SARIMA, Prophet)
- Anomaly detection (Isolation Forest, LOF)
- Explainability (SHAP, LIME)

**v3.0** (2027) - Deep Learning
- Neural networks (MLPs, CNNs, RNNs)
- Transfer learning
- Reinforcement learning
- Foundation model integration

---

## 📦 Requirements

- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.21.0
- scipy >= 1.7.0
- matplotlib >= 3.3.0
- seaborn >= 0.11.0

Optional:
- polars >= 0.14.0 (for performance)
- plotly >= 5.0.0 (for interactive plots)

---

## 📄 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

**Sudhanshu Singh**
- Email: cc9n8y8tqc@privaterelay.appleid.com
- GitHub: https://github.com/solutiongate-learn/bizlens

## 🤝 Contributing

Contributions welcome! Please see CONTRIBUTING.md for guidelines.

## 📝 Citation

```bibtex
@software{bizlens2026,
  title={BizLens: Integrated Analytics Platform},
  author={Singh, Sudhanshu},
  year={2026},
  url={https://github.com/solutiongate-learn/bizlens}
}
```

---

**BizLens v2.0.0** - Making analytics accessible, rigorous, and educational.

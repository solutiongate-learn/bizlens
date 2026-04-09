# 📓 BizLens v2.2.15 — Interactive Google Colab Notebooks

All notebooks below can be opened directly in **Google Colab** with one click. No installation needed!

---

## 🚀 Quick Start (3 Steps)

1. **Click any "Open in Colab" link below**
2. **Run the setup cell** (installs BizLens automatically)
3. **Start learning!** (Colab includes free GPU/TPU)

---

## 📚 Notebook Library

### 🔄 Process Mining (NEW in v2.2.15!)

| Notebook | Open in Colab | Topics |
|----------|:-------------:|--------|
| **Process_Mining_Foundations** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/Process_Mining_Foundations.ipynb) | Petri nets, causal nets, Alpha algorithm, conformance checking |
| **New_Process_Mining** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Process_Mining.ipynb) | Transition matrices, timelines, Sankey diagrams, bottleneck analysis |
| **New2_Process_Mining** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New2_Process_Mining.ipynb) | Variants, rework detection, resource analysis, concurrency |

### 📊 Core Analytics

| Notebook | Open in Colab | Topics |
|----------|:-------------:|--------|
| **Quick_Start** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Quick_Start_bizlens.ipynb) | Introduction to BizLens functions and workflow |
| **Descriptive_Analytics** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Descriptive_Analytics.ipynb) | Summary statistics, distributions, crosstabs, percentiles |

### 📈 Statistical Inference

| Notebook | Open in Colab | Topics |
|----------|:-------------:|--------|
| **Statistical_Inference** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Statistica_Inference.ipynb) | Hypothesis testing, confidence intervals, t-tests, ANOVA |
| **Chi_Square_Test** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_ChiSquareTest.ipynb) | Chi-square tests, categorical data analysis |

### 🎯 Unsupervised Learning

| Notebook | Open in Colab | Topics |
|----------|:-------------:|--------|
| **PCA_Clustering** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_PCA_Clustering.ipynb) | PCA dimensionality reduction, K-means, elbow method |
| **Probability_Distribution_Simulation** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Probability_Distribution_Simulation.ipynb) | Distributions, probability, Monte Carlo simulation |

### 📉 Supervised Learning — Regression

| Notebook | Open in Colab | Topics |
|----------|:-------------:|--------|
| **Linear_Multiple_Regression** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Linear_Multiple_Linear_Regression.ipynb) | Simple & multiple linear regression, R², residual analysis |

### ✅ Supervised Learning — Classification

| Notebook | Open in Colab | Topics |
|----------|:-------------:|--------|
| **Logistic_Regression** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Logistics_Regression.ipynb) | Logistic regression, confusion matrix, ROC curves, AUC |
| **Decision_Trees_Random_Forests** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Decision_Trees_Random_Forests.ipynb) | Decision trees, random forests, feature importance |

### 🔬 Advanced Topics

| Notebook | Open in Colab | Topics |
|----------|:-------------:|--------|
| **Conjoint_Analysis** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Conjoint_Analysis.ipynb) | Preference modeling, trade-off analysis, attribute importance |
| **Q_Learning** | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Q_Learning.ipynb) | Reinforcement learning, Q-learning agent training |

---

## ✨ What's New in v2.2.15

### 🎯 Process Mining Enhancements
- ✅ **Petri Net Generation** — Discover formal process models
- ✅ **Causal Net Discovery** — Extract activity relationships
- ✅ **Alpha Algorithm** — Automated process discovery
- ✅ **Workflow Net Validation** — Check process well-formedness
- ✅ **Conformance Checking** — Token replay fitness analysis

### 🐛 Bug Fixes
- Fixed `bl.describe()` — quality module import
- Fixed `process_mining.transition_matrix()` — variable unpacking
- Fixed `process_mining.timeline_visualization()` — timedelta serialization
- Fixed `tables.summary_statistics()` — integer column names
- Fixed pandas boolean dtype → statsmodels compatibility

### 🎨 Formatting
- Beautiful matplotlib theme applied to all charts
- Professional color palettes and typography
- Improved table rendering with Rich library

---

## 🖥️ Environment Comparison

| Feature | Local Jupyter | Google Colab |
|---------|:-------------:|:------------:|
| No installation needed | ✗ | ✓ |
| Free GPU/TPU | ✗ | ✓ |
| Cloud storage integration | ✗ | ✓ (Drive) |
| Real-time collaboration | ✗ | ✓ |
| Persistent storage | Local | Drive |
| Interactive plots | ✓ | ✓ |
| Animations | ✓ | ✓ |

**Recommendation:** Start in Colab, graduate to local Jupyter for production work.

---

## 📦 Installation (Local)

```bash
pip install bizlens
```

### Full Features
```bash
pip install "bizlens[full]"  # Includes all extras
```

---

## 📖 Documentation

- **PyPI**: https://pypi.org/project/bizlens/
- **GitHub**: https://github.com/solutiongate-learn/bizlens
- **Author**: Sudhanshu Singh

---

**Version:** 2.2.15  
**Last Updated:** April 2026  
**License:** MIT

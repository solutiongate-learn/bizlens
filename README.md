# BizLens 📊

**Business analytics, statistical inference, and process mining — all in one package**

BizLens is a Python library for business analysts, data scientists, educators, and students. It delivers professional statistical analysis, beautiful Rich tables, and built-in support for business process mining — all with a single `pip install`.

---

## 🚀 Open in Google Colab — No Installation Needed

Click any link to launch a notebook instantly in your browser:

### Core Analytics

| Notebook | Colab Link | What You'll Learn |
|----------|-----------|-------------------|
| **Quick Start** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Quick_Start_bizlens.ipynb) | Overview, frequency tables, outlier detection |
| **Descriptive Analytics** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Descriptive_Analytics.ipynb) | Frequency, percentile, contingency, data profile |
| **Statistical Inference** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Statistica_Inference.ipynb) | Confidence intervals, t-tests, ANOVA, correlation |
| **Chi-Square & Association** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_ChiSquareTest.ipynb) | Chi-square, contingency tables, Cramér's V |
| **Probability & Distributions** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Probability_Distribution_Simulation.ipynb) | Distribution fitting, simulation, sampling |

### Machine Learning

| Notebook | Colab Link | What You'll Learn |
|----------|-----------|-------------------|
| **Linear & Multiple Regression** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Linear_Multiple_Linear_Regression.ipynb) | OLS regression, diagnostics, predictions |
| **Logistic Regression** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Logistics_Regression.ipynb) | Binary classification, ROC, confusion matrix |
| **Decision Trees & Random Forests** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Decision_Trees_Random_Forests.ipynb) | Tree models, feature importance, ensembles |
| **PCA & Clustering** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_PCA_Clustering.ipynb) | Dimensionality reduction, K-Means, DBSCAN |
| **Conjoint Analysis** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Conjoint_Analysis.ipynb) | Preference modeling, attribute utilities |
| **Q-Learning** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Q_Learning.ipynb) | Reinforcement learning basics, Q-table |

### Process Mining

| Notebook | Colab Link | What You'll Learn |
|----------|-----------|-------------------|
| **Process Mining** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New_Process_Mining.ipynb) | Case metrics, bottlenecks, variants, resources |
| **Process Mining (Advanced)** | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/New2_Process_Mining.ipynb) | BizLens + optional pm4py integration |

> All notebooks auto-install BizLens on first run — just click the Colab badge and run the first cell.

---

## 💾 Installation

```bash
pip install bizlens
```

```bash
# With process mining extras (pm4py)
pip install bizlens[process-mining]
```

```bash
# Latest from source
git clone https://github.com/solutiongate-learn/bizlens.git
cd bizlens && pip install -e .
```

---

## 📦 Modules at a Glance

| Module | Key Functions |
|--------|--------------|
| `bl.tables` | `frequency_table`, `percentile_table`, `contingency_table`, `summary_statistics` |
| `bl.diagnostic` | `detect_outliers`, `normality_test`, `correlation_analysis`, `missing_value_analysis` |
| `bl.inference` | `confidence_interval`, `two_sample_ttest`, `anova_test`, `paired_ttest`, `correlation_test` |
| `bl.process_mining` | `case_metrics`, `variant_discovery`, `bottleneck_analysis`, `resource_analysis` |
| `bl.quality` | `data_profile`, `completeness_report`, `consistency_check` |
| `bl.describe()` | Smart all-in-one data exploration |

---

## 💡 Quick Examples

```python
import bizlens as bl
import pandas as pd

# Load a built-in teaching dataset (returns pandas DataFrame)
df = bl.load_dataset('titanic')   # or 'tips', 'iris', 'penguins', 'diamonds', 'mpg'

# Frequency distribution
bl.tables.frequency_table(df['sex'])

# Summary statistics
bl.tables.summary_statistics(df[['age', 'fare']])

# Contingency table with chi-square test
table, stats = bl.tables.contingency_table(df, 'sex', 'survived')
print(f"Chi² = {stats['chi2']:.3f}, p = {stats['p_value']:.4f}, Cramér's V = {stats['cramers_v']:.3f}")

# Data quality profile
bl.quality.data_profile(df)

# Confidence interval
import numpy as np
bl.inference.confidence_interval(df['age'].dropna(), confidence=0.95)

# Two-sample t-test
bl.inference.two_sample_ttest(df[df['sex']=='male']['fare'], df[df['sex']=='female']['fare'])
```

### Process Mining

```python
# Load a built-in event log (returns pandas DataFrame)
event_log = bl.generate_hr_onboarding_event_log()

bl.process_mining.case_metrics(event_log)
bl.process_mining.bottleneck_analysis(event_log)
bl.process_mining.variant_discovery(event_log)
bl.process_mining.resource_analysis(event_log, resource_col='resource')
```

### Polars Users

```python
# BizLens also accepts polars DataFrames
import polars as pl
df_pl = pl.from_pandas(bl.load_dataset('titanic'))
bl.tables.frequency_table(df_pl['sex'])     # works transparently
bl.quality.data_profile(df_pl)              # works transparently
```

---

## 🔄 Supported Environments

| Environment | Status |
|------------|--------|
| Google Colab | ✅ Recommended |
| Jupyter Notebook / JupyterLab | ✅ Full |
| VS Code (Jupyter extension) | ✅ Full |
| Terminal / scripts | ✅ Full |

---

## 📊 Version

- **Current**: 2.2.13
- **Python**: 3.9+
- **License**: MIT

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/solutiongate-learn/bizlens/issues)
- **Discussions**: [GitHub Discussions](https://github.com/solutiongate-learn/bizlens/discussions)
- **PyPI**: [pypi.org/project/bizlens](https://pypi.org/project/bizlens/)

---

**Made with ❤️ for business analysts, data scientists, and students**

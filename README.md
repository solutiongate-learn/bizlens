# BizLens 📊

**Fast descriptive analytics for business + real process mining event logs**

BizLens is a Python library for business analysts, data scientists, educators, and students. It provides professional statistical analysis, beautiful visualizations, and special support for business process mining.

---

## 🚀 Quick Start - Try in Google Colab Now!

No installation needed. Click any link below to start learning immediately:

### 📚 Interactive Tutorials (5-20 minutes each)

| Tutorial | Duration | What You'll Learn |
|----------|----------|-------------------|
| [**Quick Start**](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/01_Quick_Start_Colab.ipynb) | 5 min | Overview, data quality, diagnostics |
| [**Descriptive Analytics**](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/02_Descriptive_Analytics_Colab.ipynb) | 15 min | Tables, distributions, quality checks |
| [**Process Mining**](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/03_Process_Mining_Colab.ipynb) | 15 min | Event logs, workflows, bottlenecks |
| [**Statistical Inference**](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/04_Statistical_Inference_Colab.ipynb) | 20 min | Hypothesis testing, ANOVA, correlation |

**All notebooks auto-install BizLens - just run the first cell!**

---

## 💾 Installation

### Standard Installation
```bash
pip install bizlens
```

### With Specific Version
```bash
pip install bizlens==2.2.11
```

### For Development
```bash
git clone https://github.com/solutiongate-learn/bizlens.git
cd bizlens
pip install -e .
```

---

## 📦 What's Included

### 6 Core Modules

| Module | Purpose | Key Functions |
|--------|---------|---|
| **tables** | Statistical tables & distributions | frequency_table, percentile_table, contingency_table, summary_statistics |
| **diagnostic** | Data quality & outlier detection | detect_outliers, normality_test, correlation_analysis, missing_value_analysis |
| **inference** | Hypothesis testing & confidence intervals | confidence_interval, two_sample_ttest, anova_test, correlation_test |
| **process_mining** | Business process analysis | case_metrics, variant_discovery, bottleneck_analysis, rework_detection |
| **quality** | Data quality scoring | data_profile, completeness_report, consistency_check |
| **core** | Main describe() function | Smart data exploration with Pandas/Polars |

---

## 🎯 Use Cases

- **Business Analytics**: Analyze customer data, sales metrics, process efficiency
- **Education**: Teach descriptive statistics, hypothesis testing, process analysis
- **Data Science**: Quick exploratory analysis with publication-ready tables
- **Quality Assurance**: Detect outliers, assess data completeness, find anomalies
- **Process Improvement**: Identify bottlenecks, discover process variants, measure efficiency

---

## 💡 Example Usage

### Quick Data Exploration
```python
import bizlens as bz
import pandas as pd

# Load your data
df = pd.read_csv('data.csv')

# Smart analysis with one function
bz.describe(df)
```

### Create Statistical Tables
```python
# Frequency distribution
freq = bz.tables.frequency_table(df, 'category')

# Summary statistics
stats = bz.tables.summary_statistics(df[['sales', 'profit']])

# Percentile analysis
percentiles = bz.tables.percentile_table(df[['age']])
```

### Analyze Business Processes
```python
# Detect event logs automatically
metrics = bz.process_mining.case_metrics(event_log)
bottlenecks = bz.process_mining.bottleneck_analysis(event_log)
variants = bz.process_mining.variant_discovery(event_log)
```

### Run Statistical Tests
```python
# Confidence intervals
ci = bz.inference.confidence_interval(data, confidence=0.95)

# Hypothesis testing
result = bz.inference.two_sample_ttest(group1, group2)

# ANOVA for multiple groups
anova = bz.inference.anova_test(df, group_col='category', value_col='metric')
```

### Assess Data Quality
```python
# Overall quality score (0-100)
quality = bz.quality.data_profile(df)

# Detailed completeness report
completeness = bz.quality.completeness_report(df)

# Outlier detection
outliers = bz.diagnostic.detect_outliers(df[['column']], method='iqr')
```

---

## 📖 Documentation

- **API Reference**: Each function has detailed docstrings
- **Examples**: See `/examples/` directory for Python scripts
- **Notebooks**: Run interactive Colab tutorials (links above)
- **Source**: Full source code in `/src/bizlens/`

---

## ✨ Key Features

✅ **Pandas & Polars compatible** - Works with both DataFrames
✅ **Auto-install dependencies** - All notebooks handle setup automatically
✅ **Publication-ready output** - Professional tables and visualizations
✅ **Educational focus** - Clear explanations in every function
✅ **Sample datasets included** - Learn without external data
✅ **Process mining support** - Analyze event logs automatically
✅ **Statistical rigor** - Proper hypothesis testing with effect sizes
✅ **Data quality tools** - Comprehensive profiling and diagnostics

---

## 🔄 Supported Environments

| Environment | Status | Notes |
|------------|--------|-------|
| **Google Colab** | ✅ Full | Recommended for quick learning |
| **Jupyter Notebook** | ✅ Full | Local installation required |
| **JupyterLab** | ✅ Full | Modern notebook interface |
| **VS Code** | ✅ Full | With Jupyter extension |
| **Terminal/CLI** | ✅ Full | Standard Python environments |

---

## 📊 Version Info

- **Current Version**: 2.2.11
- **Python**: 3.8+
- **Status**: Production ready
- **License**: MIT

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

---

## 📞 Support

- **Issues**: Report bugs on [GitHub Issues](https://github.com/solutiongate-learn/bizlens/issues)
- **Questions**: Ask in [GitHub Discussions](https://github.com/solutiongate-learn/bizlens/discussions)
- **Feedback**: We'd love to hear how you're using BizLens!

---

## 📋 Getting Started Checklist

- [ ] Install: `pip install bizlens`
- [ ] Try Colab: Click any tutorial link above
- [ ] Explore examples: Check `/examples/` directory
- [ ] Read docstrings: `help(bz.tables.frequency_table)`
- [ ] Build something: Apply to your own data!

---

**Made with ❤️ for business analysts, data scientists, and students**

[GitHub](https://github.com/solutiongate-learn/bizlens) • [PyPI](https://pypi.org/project/bizlens/) • [MIT License](LICENSE)

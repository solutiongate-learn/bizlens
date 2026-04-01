# BizLens 📊

**Fast business descriptive analytics — Polars-first, beautiful charts, and normality comparison**

BizLens is a Python analytics library designed for business analysts, teachers, and students. It provides:

- **⚡ Zero-copy performance** with Polars (10-100x faster than Pandas)
- **📈 Instant descriptive statistics** with Mean, Median, Mode, Skewness, IQR
- **📉 Beautiful visualizations** with Matplotlib & Seaborn
- **🔬 Normality comparison** — see how your data deviates from normal distribution
- **🎓 Educational-friendly** — Interactive demos for learning analytics concepts
- **🌍 Framework-agnostic** with Narwhals (works with Polars, Pandas, Dask, etc.)

---

## Quick Start

### Installation

```bash
pip install bizlens
```

### Basic Usage

```python
import bizlens as bl
import polars as pl

# Create or load data
df = pl.read_csv("sales_data.csv")

# Instant analysis
bl.describe(df, plots=True, norm_compare=True)
```

### Interactive Demo

```python
import bizlens as bl

# Generate realistic business dataset
demo_data = bl.create_interactive_demo()

# Analyze with visualizations
bl.describe(demo_data, plots=True)
```

### For Teachers & Students

```python
import bizlens as bl

# Load pre-built sample data
data = bl.load_sample_business_data()

# Analyze and save plots as PNG files
bl.describe(data, plots=True, save_plots=True)
```

---

## Why BizLens?

### The Problem
Business analysts often assume revenue is "normally distributed," but it's usually **log-normal (skewed)**. Standard averages mislead managers.

### The Solution
BizLens shows **side-by-side comparisons**:
- Left: Your actual data distribution
- Right: How it compares to a standard normal curve

This teaches the "why" behind skewed data in a visually intuitive way.

---

## Features

### 📊 Core Analytics

```python
bl.describe(df, plots=True, bins=30, norm_compare=True)
```

Returns:
- **Shape**: Dataset dimensions
- **Numeric Stats**: Mean, Median, Mode, Std Dev, Range, IQR, Skewness
- **Missing Values**: Count of NaN per column
- **Visualizations**: Distribution + Normality plots (optional)

### 💾 Export Support

```python
# Save analysis to CSV or Excel
bl.describe(df, export="output.csv")
bl.describe(df, export="output.xlsx")
```

### 🖼️ Chart Control

```python
# Display plots in Jupyter/interactive mode
bl.describe(df, plots=True, save_plots=False)

# Save plots as PNG files (great for reports)
bl.describe(df, plots=True, save_plots=True)
```

---

## Advanced Usage

### Using the BizDesc Class

```python
from bizlens import BizDesc

# Initialize with file path or DataFrame
bd = BizDesc("data.csv")

# Get detailed results
results = bd.summary(
    include_plots=True,
    bins=50,
    norm_compare=True,
    export="analysis.csv"
)

print(results['numeric_stats'])
```

### Working with Different Data Sources

```python
import polars as pl
import pandas as pd
import narwhals as nw

# Polars (zero-copy)
df_pl = pl.read_csv("data.csv")
bl.describe(df_pl)

# Pandas
df_pd = pd.read_csv("data.csv")
bl.describe(df_pd)

# From file path
bl.describe("data.csv")  # Auto-detects CSV
bl.describe("data.xlsx")  # Auto-detects Excel
bl.describe("data.parquet")  # Auto-detects Parquet
```

---

## API Reference

### `bizlens.describe()`

```python
bl.describe(
    data,              # DataFrame or file path
    plots=False,       # Generate visualizations
    export=None,       # Export to file
    bins=30,           # Histogram bins
    norm_compare=True, # Compare to standard normal
    save_plots=False   # Save PNG instead of display
)
```

### `bizlens.BizDesc`

```python
from bizlens import BizDesc

bd = BizDesc(data)
result = bd.summary(include_plots=True)
```

### `bizlens.create_interactive_demo()`

Generates sample business dataset with:
- Transaction IDs
- Geographic regions (East, West, North, South)
- Revenue (exponential/skewed distribution)
- Customer satisfaction scores (normal distribution)
- Units sold (Poisson distribution)
- Priority levels (categorical)

### `bizlens.load_sample_business_data()`

Pre-loaded sample dataset (500 rows) for quick demos and testing.

---

## Why Polars + Narwhals?

| Feature | Pandas | Polars | BizLens |
|---------|--------|--------|---------|
| Speed (1M rows) | 1x (baseline) | 10-100x | ⚡ 10-100x |
| Memory | High | Low | Low |
| Null handling | ⚠️ Complex | ✅ Simple | ✅ Simple |
| Type safety | Weak | Strong | Strong |
| Framework support | Just Pandas | Polars/Dask | **All** (Narwhals) |

---

## Installation from Source

```bash
git clone https://github.com/yourusername/bizlens.git
cd bizlens
pip install -e ".[all]"
```

---

## Requirements

- Python 3.9+
- polars >= 0.18.0
- narwhals >= 0.8.0
- pandas >= 1.5.0
- numpy >= 1.23.0
- scipy >= 1.9.0
- matplotlib >= 3.6.0
- seaborn >= 0.12.0
- rich >= 13.0.0

---

## Testing

```bash
# Install with test dependencies
pip install -e ".[all]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=bizlens tests/
```

---

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

MIT License © 2026 Sudhanshu Singh

---

## Acknowledgments

Built with:
- **Polars** for blazing-fast data processing
- **Narwhals** for dataframe interoperability
- **Rich** for beautiful terminal output
- **SciPy** for statistical functions
- **Matplotlib & Seaborn** for visualization

---

## Support

For questions, issues, or feature requests:
- 🐛 [GitHub Issues](https://github.com/yourusername/bizlens/issues)
- 📧 Email: cc9n8y8tqc@privaterelay.appleid.com

---

**Happy analyzing! 📊**

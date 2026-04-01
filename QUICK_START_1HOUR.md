# BizLens v0.6.0 — Quick Start (5 Minutes to First Plot) ⏱️

## 🚀 Launch in 1 Hour

This guide gets you from zero to fully functional educational analytics in 60 minutes.

---

## ⚡ The 5-Minute Path

### Step 1: Install Dependencies (2 minutes)
```bash
pip install polars pandas narwhals numpy scipy matplotlib seaborn jupyter
```

### Step 2: Open Jupyter (1 minute)
```bash
jupyter notebook DEMO_NOTEBOOK.ipynb
```

### Step 3: Run All Cells (2 minutes)
Click "Cell → Run All" or press `Ctrl+A` then `Shift+Enter`

**You now have:**
- ✅ Descriptive statistics
- ✅ 6 different visualizations
- ✅ Outlier detection
- ✅ Normality testing
- ✅ Correlation analysis
- ✅ Grouped comparisons

---

## 📊 What's Included in v0.6.0

### Core Functions

**1. Load Educational Data**
```python
import bizlens as bl

# Load datasets designed for teaching
df = bl.load_dataset('school_cafeteria')      # Spending data
df = bl.load_dataset('test_scores')            # Academic performance
```

**2. Get Descriptive Statistics**
```python
bd = bl.BizDesc(df)
stats = bd.describe(include_plots=True)

# Output:
# - Mean, Median, Mode
# - Std Dev, IQR
# - Min, Max, Quartiles
# - Skewness, Kurtosis
```

**3. Visualize with Different Plot Types**
```python
bd.visualize('column_name', plot_type='histogram')
bd.visualize('column_name', plot_type='boxplot')
bd.visualize('column_name', plot_type='violin')
bd.visualize('column_name', plot_type='density')
```

**4. Detect Outliers (IQR Method)**
```python
outliers = bd.outliers()
# Shows: count, percentage, valid range for each column
```

**5. Test for Normality (Shapiro-Wilk)**
```python
normality = bd.normality_test()
# Shows: p-value, interpretation (Normal? Yes/No)
```

**6. Analyze Correlations (Pearson)**
```python
corr_matrix = bd.correlations()
# Shows: heatmap + correlation table
```

---

## 📚 Supported Education Levels

### ✅ High School (AP Statistics)
- Descriptive statistics
- Distribution analysis
- Outlier detection
- Simple correlations

### ✅ Undergraduate Year 1-2
- Hypothesis testing preparation
- Normality testing
- Group comparisons
- Correlation analysis

### ✅ Undergraduate Year 3-4
- Multivariate analysis
- Outlier handling
- Residual analysis setup

### ✅ Postgraduate
- Complex datasets
- Multiple distributions
- Real-world data patterns

---

## 🧮 Formulas Used (Transparent Calculations)

All calculations show the exact formula used:

```
MEAN:           μ = (Σ x) / n
MEDIAN:         50th percentile (sort and take middle)
STD DEV:        σ = √(Σ(x - μ)² / (n-1))
SKEWNESS:       γ = (3(μ - median)) / σ
IQR:            Q3 - Q1
OUTLIERS:       Values outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
CORRELATION:    r = Σ((x - μₓ)(y - μᵧ)) / √(Σ(x - μₓ)² × Σ(y - μᵧ)²)
NORMALITY:      Shapiro-Wilk test (p-value interpretation)
```

Every calculation is documented in the output.

---

## 📦 Dependency Libraries Explained

### **Core Dependencies**

| Library | Purpose | Why Needed |
|---------|---------|-----------|
| **polars** | Fast data processing | 10-100x faster than pandas for large datasets |
| **pandas** | Data manipulation | Standard in data science, Excel/CSV support |
| **narwhals** | Bridge framework | Lets you use both Polars & Pandas seamlessly |
| **numpy** | Numerical computing | Powers all statistical calculations |
| **scipy** | Statistics functions | Shapiro-Wilk test, distribution analysis |
| **matplotlib** | Plotting | Core visualization library |
| **seaborn** | Statistical plots | Better-looking plots on top of matplotlib |

### **Why This Stack?**

```
Traditional (Slow):              Modern (Fast):
Pandas only                       Polars + Narwhals
  ↓ Slow                            ↓ Fast
Memory issues at scale           Zero-copy operations
  ↓                               ↓
Not optimized                    Optimized for education
```

---

## 🎯 Example: Analyzing School Spending in 30 Seconds

```python
# 1. Import and load
import bizlens as bl
df = bl.load_dataset('school_cafeteria')

# 2. Analyze
bd = bl.BizDesc(df)
stats = bd.describe(plots=True)

# 3. Detect outliers
outliers = bd.outliers()

# 4. Test normality
normality = bd.normality_test()

# 5. Find correlations
corr = bd.correlations()

# DONE! You've analyzed 200 data points with 5 lines of code.
```

---

## 🔍 What Each Visualization Shows

### Histogram (Distribution)
- **Shows**: How many students spend each amount
- **Look for**: Shape, peaks, outliers
- **Interpretation**: Skewed = most students spend little, few spend lots

### Boxplot (Quartiles)
- **Shows**: Q1, Median, Q3, outliers
- **Look for**: Outliers (dots), whisker length
- **Interpretation**: Long whisker = wider range of spending

### Violin Plot (Density)
- **Shows**: Full distribution shape
- **Look for**: Multiple peaks (bimodal?), width at different values
- **Interpretation**: Wide = more students, narrow = fewer students

### Heatmap (Correlations)
- **Shows**: Relationship between all numeric columns
- **Look for**: Dark colors (strong correlation), light colors (weak)
- **Interpretation**: Red = positive, Blue = negative correlation

---

## 📖 Sample Analysis Walkthrough

### Question: "Do students who spend more on lunch have higher satisfaction?"

```python
# Step 1: Load data
df = bl.load_dataset('school_cafeteria')
bd = bl.BizDesc(df)

# Step 2: Check spending distribution
bd.visualize('spending', plot_type='histogram')
# Result: Right-skewed (most spend $4-6, few spend $15+)

# Step 3: Check satisfaction distribution
bd.visualize('satisfaction', plot_type='histogram')
# Result: Normal-ish, centered around 6.5

# Step 4: Check correlation
corr = bd.correlations()
# Result: Shows spending vs satisfaction correlation

# Step 5: Visual analysis
bd.visualize both, create scatter plot
# Result: Some high spenders are satisfied, but not all

# Conclusion: Moderate positive correlation, but other factors matter!
```

---

## ⚠️ Important: Correlation ≠ Causation

Just because spending correlates with satisfaction doesn't mean:
- Spending CAUSES satisfaction
- Satisfaction causes more spending
- The relationship is straightforward

**Could be**:
- Both caused by something else (pocket money amount?)
- Confounding variables (lunch type?)
- Just coincidence

**Always ask**: What else could explain this pattern?

---

## 🚀 Launch Checklist (60 Minutes)

### Minute 0-5: Setup
- [ ] Install dependencies: `pip install -r requirements_v0_6_0.txt`
- [ ] Verify installation: `python -c "import polars; print('✅')""`

### Minute 5-15: Explore Data
- [ ] Open DEMO_NOTEBOOK.ipynb
- [ ] Load school_cafeteria dataset
- [ ] View first 5 rows

### Minute 15-30: Statistics
- [ ] Run describe() function
- [ ] Review statistics output
- [ ] Understand formulas (reference guide above)

### Minute 30-45: Visualizations
- [ ] Create histogram
- [ ] Create boxplot
- [ ] Create violin plot
- [ ] Create correlation heatmap

### Minute 45-55: Analysis
- [ ] Detect outliers
- [ ] Test normality
- [ ] Analyze by groups

### Minute 55-60: Documentation
- [ ] Screenshot results
- [ ] Write 2-3 key findings
- [ ] Save notebook

### Minute 60: Launch! 🎉

---

## 📞 Quick Troubleshooting

### "Import Error: No module named 'polars'"
```bash
pip install polars
```

### "Plots not showing in Jupyter"
```python
%matplotlib inline  # Add this to first cell
```

### "Dataset not found"
```python
# Verify datasets are in correct path
bl.load_dataset('school_cafeteria')  # Case-sensitive!
```

### "Memory error with large datasets"
- Good news: Polars handles it! Just load normally
- If still slow: Use `n_rows` parameter to sample

---

## 📚 What's in DEMO_NOTEBOOK.ipynb

**8 Complete Sections:**

1. Setup & import
2. Load educational dataset
3. Descriptive statistics with formulas
4. Interactive visualizations (4 types)
5. Outlier detection
6. Normality testing
7. Correlation analysis
8. Group comparisons
9. Custom analysis & summary

**Each section includes:**
- Code ready to run
- Formula explanation
- Interpretation guide
- Discussion questions

---

## 🎓 Use in Your Classroom

### High School (AP Statistics)
1. Load `school_cafeteria` dataset
2. Show section 2-3 (statistics + visualizations)
3. Ask students: "Is this distribution normal?"
4. Run normality test
5. Discuss why real data isn't always normal

### Undergraduate (Intro Stats)
1. Start with test_scores
2. Group analysis by subject
3. Compare distributions
4. Test for normality
5. Analyze correlations between subjects

### Postgraduate (Advanced Stats)
1. Load test_scores
2. Multi-level analysis by subject and student
3. Advanced outlier detection
4. Bayesian interpretation of p-values
5. Causal inference discussion

---

## ✨ Why BizLens v0.6.0 is Different

| Feature | BizLens | Others |
|---------|---------|--------|
| **Formulas shown** | ✅ Explicit | ❌ Hidden |
| **Educational datasets** | ✅ 2 included | ❌ Have to find own |
| **Polars-native** | ✅ Fast | ❌ Slow (pandas) |
| **One-liner API** | ✅ bl.describe(df) | ❌ 20+ functions |
| **Interactive plots** | ✅ Multiple types | ⚠️ Limited |
| **Copyright-safe data** | ✅ Synthetic | ❌ Real/licensed |
| **Textbook alignment** | ✅ AP Stats, ISLR | ❌ Generic |

---

## 📞 Support

**Questions?**
1. Check DEMO_NOTEBOOK.ipynb (has examples)
2. Read formula section above
3. Run code yourself and experiment
4. Modify values to see how output changes

**Interactive Learning:**
- Change bin size: `bd.visualize('spending', plot_type='histogram', bins=50)`
- Try different columns: `bd.visualize('satisfaction', ...)`
- Load different dataset: `bl.load_dataset('test_scores')`

---

## 🎯 Your Next 60 Minutes

**Go from zero to running analysis platform:**

```
0:00 - Install dependencies
5:00 - Open notebook
15:00 - Load data
20:00 - Run statistics
30:00 - Create visualizations
45:00 - Detect patterns
55:00 - Document findings
60:00 - LAUNCH! 🚀
```

**Time to first plot: < 5 minutes**

---

**Ready? Let's go! 📊**

```bash
# Copy-paste this to get started:
pip install -r requirements_v0_6_0.txt
jupyter notebook DEMO_NOTEBOOK.ipynb
```

Then run all cells and explore! 🎉

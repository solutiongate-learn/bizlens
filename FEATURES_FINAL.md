# BizLens v0.6.0 ENHANCED — Final Complete Feature Guide 📊

## What's New in the Final Version

This is the **most comprehensive educational analytics platform** with advanced distribution visualization and integrated sample datasets.

---

## 🎯 PART 1: DISTRIBUTION VISUALIZATION (NEW!)

### What You See on Enhanced Histograms

Every histogram now shows:

1. **Distribution Type Annotation** (top right, red box)
   - **SYMMETRIC (Normal-like)**: Bell curve shape, Mean ≈ Median
   - **RIGHT-SKEWED (Positive tail)**: Long tail to the right, Mean > Median
   - **LEFT-SKEWED (Negative tail)**: Long tail to the left, Mean < Median
   - **Skewness Value**: Numerical measure of asymmetry

2. **Statistical Lines**
   - **Orange dashed line**: Mean (arithmetic average)
   - **Green solid line**: Median (middle value)
   - **Red dotted line**: Mode (most frequent value, if applicable)

3. **Statistics Box** (top left, white background)
   - **Range**: [Min, Max] values
   - **Range Width**: Max - Min
   - **Standard Deviation (σ)**: Measure of spread

### Example Interpretation

```
SPENDING DATA HISTOGRAM:
- Mean = 6.22, Median = 4.80
- Mean > Median → RIGHT-SKEWED
- Orange line is to the right of green line
- Histogram shows more values on left side
- Skewness = 0.79 (moderate right skew)

INTERPRETATION:
✓ Most students spend $3-5 (left side peak)
✓ Few students spend $20+ (long tail to right)
✓ MEDIAN ($4.80) better represents "typical" student
✓ Mean pulled higher by outlier spenders
```

### When Each Distribution Type Occurs

**SYMMETRIC Distributions:**
- Height measurements (bell curve)
- Test scores (normally distributed)
- IQ scores (standardized)
- Satisfaction ratings (centered)

**RIGHT-SKEWED Distributions:**
- Income/salaries (many low earners, few high earners)
- Spending (many small purchases, few large ones)
- Website page loads (many quick, few slow)
- Waiting times (most short, some very long)

**LEFT-SKEWED Distributions:**
- Age at retirement (many late, few early)
- Test scores on easy exams (many high, few low)
- Exam performance with curve (compressed at high end)

---

## 📊 PART 2: VARIANCE & STANDARD DEVIATION COVERAGE

### What is Variance?

**Variance (σ²):**
```
Formula: σ² = Σ(x - μ)² / (n - 1)

What it means:
- Average squared deviation from mean
- Measures how spread out data is
- Large variance = Data spread out
- Small variance = Data clustered together
```

### What is Standard Deviation?

**Standard Deviation (σ):**
```
Formula: σ = √variance

What it means:
- Square root of variance (easier to interpret)
- Same units as original data
- One standard deviation from mean covers ~68% of data
```

### The 68-95-99.7 Rule

For normally distributed data:

```
68% of data within ±1σ (one standard deviation)
95% of data within ±2σ (two standard deviations)
99.7% of data within ±3σ (three standard deviations)

Example with Satisfaction (μ=6.5, σ=1.5):
± 1σ: [5.0, 8.0]   → 68% of students here
± 2σ: [3.5, 9.5]   → 95% of students here
± 3σ: [2.0, 11.0]  → 99.7% of students here (essentially all)
```

### Where You See It in BizLens

1. **Central Tendency Output**
   ```
   Std Dev (σ)  :    5.43  (Spread around mean)
   ```

2. **Histogram Statistics Box**
   ```
   Std Dev: 5.43
   ```

3. **Complete Descriptive Analysis**
   ```
   Std Dev column shows σ for each numeric column
   ```

---

## 📚 PART 3: INTEGRATED SAMPLE DATASETS

### Available Datasets (15+ Built-in Options)

#### SEABORN DATASETS

**iris** (150 samples)
- Classic iris flowers dataset
- 4 numeric features, 1 categorical (species)
- Perfect for: Classification, multivariate analysis
- Education Level: High School, Undergraduate Year 1

**tips** (244 observations)
- Restaurant tips data with categorical variables
- Features: Total bill, tip, sex, day, time, party size
- Perfect for: Categorical comparison, correlation
- Education Level: High School, Undergraduate Year 1

**titanic** (891 records)
- Titanic passenger data with survival information
- Large dataset with missing values
- Perfect for: Missing data handling, correlation, binary outcomes
- Education Level: Undergraduate Year 1-2

**penguins** (344 observations)
- Palmer Penguins dataset with species info
- Features: Species, island, measurements, body mass
- Perfect for: Species comparison, multivariate analysis
- Education Level: Undergraduate Year 1-2

**diamonds** (53,940 records)
- Diamond prices and characteristics
- Large real-world dataset
- Perfect for: Correlation, regression, multivariate
- Education Level: Undergraduate Year 2-3

**flights** (144 records)
- Airline passenger data (1949-1960)
- Time series data
- Perfect for: Time series, trend analysis, seasonality
- Education Level: Undergraduate Year 2+

**mpg** (398 cars)
- Auto MPG dataset with multiple features
- Features: MPG, cylinders, displacement, horsepower, weight
- Perfect for: Regression, correlation, categorical analysis
- Education Level: Undergraduate Year 1-2

**planets** (1,000+ records)
- Exoplanet discovery data
- Advanced dataset with many features
- Perfect for: Distribution analysis, outlier detection
- Education Level: Undergraduate Year 2+

**exercise** (180 observations)
- Exercise physiology data
- Features: Athlete info, pulse, oxygen uptake, duration
- Perfect for: Categorical analysis, correlation
- Education Level: Undergraduate Year 1-2

#### SKLEARN DATASETS

**digits** (1,797 samples)
- Handwritten digits (0-9) dataset
- 64 features (8×8 pixel images)
- Perfect for: Image classification, multivariate
- Education Level: Undergraduate Year 3+

**wine** (178 samples)
- Wine classification dataset
- 13 numeric features
- Perfect for: Classification, multivariate analysis
- Education Level: Undergraduate Year 1-2

**breast_cancer** (569 samples)
- Cancer diagnosis dataset
- 30 numeric features, binary outcome
- Perfect for: Medical classification, feature importance
- Education Level: Postgraduate

#### SCIPY GENERATED DATASETS

**student_t** (500 samples)
- Student's t-distribution with heavy tails
- Perfect for: Understanding distribution shapes
- Education Level: Undergraduate Year 2+

**normal_dist** (500 samples)
- Standard normal distribution
- Perfect for: Understanding normal distribution
- Education Level: High School, Undergraduate Year 1

**exponential_dist** (500 samples)
- Exponential distribution (right-skewed)
- Perfect for: Understanding skewed distributions
- Education Level: Undergraduate Year 2+

### How to Use Sample Datasets

#### 1. List All Available Datasets

```python
import bizlens as bl

# See all available datasets
df = bl.list_sample_datasets()
```

Output shows:
- Dataset name
- Source (seaborn, sklearn, scipy)
- Size (rows × columns)
- Education level
- Brief description

#### 2. Get Detailed Info About a Dataset

```python
# Detailed information about specific dataset
bl.dataset_info('iris')
```

Shows:
- Complete description
- Education level and use cases
- Key concepts covered
- Features list
- All metadata

#### 3. Load a Dataset

```python
# Load external sample dataset
df_iris = bl.load_dataset('iris')

# Load built-in educational dataset
df_school = bl.load_dataset('school_cafeteria')
df_scores = bl.load_dataset('test_scores')
```

#### 4. Analyze Immediately

```python
# Create analyzer
bd = bl.BizDesc(df_iris, color_scheme='academic')

# Get central tendency
cent_tend = bd.central_tendency()

# Visualize
bd.visualize('sepal_length', plot_type='histogram')

# Compare groups
bd.compare_categorical('species', 'sepal_length')

# Check correlations
bd.correlations()
```

---

## 🎨 ENHANCED VISUALIZATION FEATURES

### Value Labels on Bar Charts

```
NEW FEATURE: Value labels on top of each bar

Before:
     │ ████
     │ ███
     │ ██

After:
  8  │ ████
  5  │ ███   ← Numbers show exact counts
  3  │ ██
```

### Distribution Type Annotations

```
NEW FEATURE: Visible annotation of distribution type

RED BOX (top right):
┌─────────────────────────────┐
│ Distribution: RIGHT-SKEWED  │
│ Skewness: 0.789            │
└─────────────────────────────┘
```

### Statistics Information Box

```
NEW FEATURE: Key statistics displayed on plot

WHITE BOX (top left):
┌────────────────────────────┐
│ Range: [3.50, 25.00]       │
│ Range Width: 21.50         │
│ Std Dev: 5.43              │
└────────────────────────────┘
```

### Color Schemes (3 Professional Options)

**ACADEMIC** (Professional, Formal)
- Colors: Deep Blue, Purple, Orange, Green, Red
- Use: Reports, research papers, formal settings
- Tone: Serious, traditional, trustworthy

**PASTEL** (Educational, Friendly)
- Colors: Light Blue, Light Pink, Mauve, Cyan, Light Red
- Use: Student work, educational materials
- Tone: Approachable, warm, inviting

**VIBRANT** (Modern, Eye-Catching)
- Colors: Red, Teal, Yellow, Mint, Dark Red
- Use: Presentations, posters, social media
- Tone: Bold, contemporary, energetic

---

## 📈 9 VISUALIZATION TYPES

### Complete Reference

| Visualization | Best For | Key Features |
|---|---|---|
| **Histogram** | Distribution shape | Mean/median/mode lines, distribution annotation |
| **Boxplot** | Quartiles, outliers | Q1, Median, Q3, whiskers, outlier dots |
| **Violin** | Density distribution | Full distribution shape, smooth curve |
| **Density** | Smooth curve | Probability distribution, comparison |
| **Bar** | Categorical counts | Value labels on bars, color per category |
| **Pie** | Proportions | Percentages, part-to-whole |
| **Line** | Trends | Progression, filled area, pattern detection |
| **Categorical Compare** | Group comparison | Boxplot + bar chart side-by-side |
| **Heatmap** | Correlations | Color-coded relationships, coefficients |

---

## 🎓 EDUCATIONAL ALIGNMENT

### High School (AP Statistics)
- ✅ Central tendency (mean, median, mode)
- ✅ Distribution shapes
- ✅ Outlier detection
- ✅ Histograms and boxplots
- ✅ Real-world data exploration

**Recommended Datasets:** school_cafeteria, tips, iris

### Undergraduate Year 1
- ✅ All above +
- ✅ Variance and standard deviation
- ✅ Quartiles and IQR
- ✅ Correlation analysis
- ✅ Multiple visualization types

**Recommended Datasets:** tips, iris, test_scores, mpg

### Undergraduate Year 2-3
- ✅ All above +
- ✅ Distribution testing (normality)
- ✅ Multivariate analysis
- ✅ Group comparisons
- ✅ Statistical relationships

**Recommended Datasets:** diamonds, flights, penguins, titanic

### Postgraduate
- ✅ All above +
- ✅ Complex data analysis
- ✅ Research methodology
- ✅ Publication-ready visualizations
- ✅ Feature importance analysis

**Recommended Datasets:** breast_cancer, all datasets

---

## 🚀 QUICK START

### Installation
```bash
pip install -r requirements_v0_6_0.txt
```

### Basic Usage
```python
import bizlens as bl

# Load data
df = bl.load_dataset('iris')

# Create analyzer
bd = bl.BizDesc(df, color_scheme='academic')

# Central tendency
cent_tend = bd.central_tendency()

# Visualize distribution
bd.visualize('sepal_length', plot_type='histogram')

# All in one
stats = bd.describe(include_plots=True)
```

### Explore Datasets
```python
# List available datasets
bl.list_sample_datasets()

# Get info about specific dataset
bl.dataset_info('tips')

# Load and analyze
df_tips = bl.load_dataset('tips')
bd_tips = bl.BizDesc(df_tips)
bd_tips.central_tendency()
```

---

## 📋 Complete API Reference

### Core Functions

**load_dataset(name)**
- Load any sample dataset or built-in dataset
- Returns: DataFrame

**list_sample_datasets()**
- Show all available datasets with descriptions
- Returns: DataFrame with dataset information

**dataset_info(name)**
- Print detailed information about a dataset
- Includes: Description, education level, concepts, features

### BizDesc Methods

**central_tendency()**
- Mean, Median, Mode, Range, Std Dev, Skewness
- Includes distribution type identification

**describe(include_plots=True)**
- Complete statistical summary
- Includes central tendency + histograms

**visualize(column, plot_type)**
- 9 visualization types with enhanced formatting
- Options: histogram, boxplot, violin, density, bar, pie, line, scatter, heatmap

**compare_categorical(cat_column, numeric_column)**
- Compare groups with boxplot + bar chart
- Includes value labels

**correlations(method='pearson')**
- Heatmap with correlation coefficients
- Shows relationships between all numeric columns

**outliers(method='iqr')**
- Detect and visualize outliers
- Shows IQR bounds and outlier percentage

**normality_test()**
- Shapiro-Wilk test for normality
- Returns p-value and interpretation

---

## ✨ Summary: Complete Feature List

✅ **Central Tendency Statistics**
- Mean, Median, Mode with interpretation
- Range and Range Width
- Standard Deviation and Variance
- Skewness with distribution type

✅ **Distribution Visualization**
- Distribution type annotation (Symmetric/Skewed)
- Visual indicators on histogram
- Statistics information box

✅ **9 Visualization Types**
- Each with enhanced formatting and value labels
- Professional color schemes
- Bold titles and axis labels
- Grid lines and legends

✅ **Integrated Sample Datasets**
- 15+ datasets from Seaborn, Sklearn, Scipy
- Educational metadata
- Easy discovery with descriptions
- One-liner loading

✅ **Statistical Analysis**
- Outlier detection (IQR method)
- Normality testing (Shapiro-Wilk)
- Correlation analysis (Pearson)
- Group comparisons

✅ **Professional Presentation**
- 3 color schemes (Academic, Pastel, Vibrant)
- Value labels on charts
- Enhanced formatting
- Publication-ready output

---

## 🎯 Perfect For

- **Teachers**: Built-in lesson materials, datasets, visualizations
- **Students**: Learning statistics with real data, immediate visual feedback
- **Researchers**: Quick data exploration, publication-ready figures
- **Self-Learners**: Complete toolkit with documentation and examples

---

## 📊 Example Workflow

```python
import bizlens as bl

# 1. Explore available datasets
bl.list_sample_datasets()

# 2. Load dataset
df = bl.load_dataset('iris')

# 3. Create analyzer with chosen color scheme
bd = bl.BizDesc(df, color_scheme='academic')

# 4. Get comprehensive statistics
cent_tend = bd.central_tendency()

# 5. Visualize multiple ways
bd.visualize('sepal_length', plot_type='histogram')  # Distribution
bd.visualize('sepal_length', plot_type='boxplot')    # Outliers
bd.compare_categorical('species', 'sepal_length')    # Groups
bd.correlations()                                      # Relationships

# 6. Detect anomalies
outliers = bd.outliers()

# 7. Test for normality
normality = bd.normality_test()

# COMPLETE ANALYSIS IN 10 LINES OF CODE! 🚀
```

---

**BizLens v0.6.0 ENHANCED**
*Educational Analytics Platform for Every Level*

*Created: March 31, 2026*
*Status: READY FOR PRODUCTION USE*

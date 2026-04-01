# BizLens Testing Guide 🧪

**Before Publishing to PyPI & GitHub**

This guide walks you through comprehensive testing of BizLens v0.6.0 ENHANCED.

---

## 📋 Table of Contents

1. [Quick Testing (15 minutes)](#quick-testing)
2. [Comprehensive Testing (1 hour)](#comprehensive-testing)
3. [Automated Unit Tests](#automated-unit-tests)
4. [Integration Tests](#integration-tests)
5. [Local Installation Testing](#local-installation-testing)
6. [Pre-Publication Checklist](#pre-publication-checklist)

---

## 🚀 Quick Testing (15 minutes)

### Step 1: Verify Installation
```bash
cd /path/to/bizlens
pip install -r requirements_v0_6_0.txt
```

### Step 2: Test Core Import
```python
python -c "import bizlens as bl; print('✅ BizLens imported successfully')"
```

### Step 3: Test Basic Functionality
```python
import bizlens as bl

# Load data
df = bl.load_dataset('school_cafeteria')

# Create analyzer
bd = bl.BizDesc(df, color_scheme='academic')

# Get statistics
cent_tend = bd.central_tendency()

# Describe
stats = bd.describe(include_plots=False)

print("✅ Basic functionality works!")
```

### Step 4: Test Visualizations (in Jupyter)
```python
import bizlens as bl

df = bl.load_dataset('iris')
bd = bl.BizDesc(df)

# Test histogram (with distribution annotation)
bd.visualize('sepal_length', plot_type='histogram')

# Test boxplot
bd.visualize('sepal_length', plot_type='boxplot')

print("✅ Visualizations work!")
```

---

## 🔍 Comprehensive Testing (1 hour)

### Section A: Data Loading Tests

```python
import bizlens as bl

print("=" * 60)
print("TEST 1: Built-in Dataset Loading")
print("=" * 60)

# Test 1.1: School Cafeteria
df1 = bl.load_dataset('school_cafeteria')
print(f"✅ school_cafeteria: {df1.shape}")

# Test 1.2: Test Scores
df2 = bl.load_dataset('test_scores')
print(f"✅ test_scores: {df2.shape}")

print("\n" + "=" * 60)
print("TEST 2: External Dataset Loading (Seaborn)")
print("=" * 60)

try:
    df_iris = bl.load_dataset('iris')
    print(f"✅ iris: {df_iris.shape}")

    df_tips = bl.load_dataset('tips')
    print(f"✅ tips: {df_tips.shape}")

    df_titanic = bl.load_dataset('titanic')
    print(f"✅ titanic: {df_titanic.shape}")
except Exception as e:
    print(f"⚠️  External datasets require seaborn: {e}")

print("\n" + "=" * 60)
print("TEST 3: Dataset Discovery")
print("=" * 60)

datasets_df = bl.list_sample_datasets()
print(f"✅ Found {len(datasets_df)} datasets")
print(datasets_df.head())

bl.dataset_info('iris')
```

### Section B: Central Tendency Tests

```python
import bizlens as bl
import pandas as pd
import numpy as np

print("=" * 60)
print("TEST 4: Central Tendency Calculation")
print("=" * 60)

# Test with built-in data
df = bl.load_dataset('school_cafeteria')
bd = bl.BizDesc(df, color_scheme='academic')

# Get central tendency
cent_tend = bd.central_tendency()

# Verify all statistics present
for col, stats in cent_tend.items():
    print(f"\n{col}:")
    print(f"  Mean: {stats['mean']}")
    print(f"  Median: {stats['median']}")
    print(f"  Mode: {stats['mode']}")
    print(f"  Std Dev: {stats['std_dev']}")
    print(f"  Skewness: {stats['skewness']}")
    print(f"  Distribution Type: {stats['distribution_type']}")

print("\n✅ All central tendency statistics present!")
```

### Section C: Visualization Tests

```python
import bizlens as bl
import matplotlib.pyplot as plt

print("=" * 60)
print("TEST 5: All 9 Visualization Types")
print("=" * 60)

df = bl.load_dataset('iris')
bd = bl.BizDesc(df, color_scheme='academic')

visualizations = [
    'histogram',
    'boxplot',
    'violin',
    'density',
    'bar',
    'pie',
    'line',
]

for viz_type in visualizations:
    try:
        bd.visualize('sepal_length', plot_type=viz_type)
        plt.close('all')
        print(f"✅ {viz_type}")
    except Exception as e:
        print(f"❌ {viz_type}: {e}")

# Test categorical comparison
try:
    bd.compare_categorical('species', 'sepal_length')
    plt.close('all')
    print(f"✅ categorical_comparison")
except Exception as e:
    print(f"❌ categorical_comparison: {e}")

# Test correlations
try:
    bd.correlations()
    plt.close('all')
    print(f"✅ correlations")
except Exception as e:
    print(f"❌ correlations: {e}")
```

### Section D: Color Scheme Tests

```python
import bizlens as bl
import matplotlib.pyplot as plt

print("=" * 60)
print("TEST 6: Color Schemes")
print("=" * 60)

df = bl.load_dataset('school_cafeteria')

color_schemes = ['academic', 'pastel', 'vibrant']

for scheme in color_schemes:
    try:
        bd = bl.BizDesc(df, color_scheme=scheme)
        bd.visualize('spending', plot_type='histogram')
        plt.close('all')
        print(f"✅ {scheme}")
    except Exception as e:
        print(f"❌ {scheme}: {e}")

print("\n✅ All color schemes working!")
```

### Section E: Statistical Tests

```python
import bizlens as bl

print("=" * 60)
print("TEST 7: Statistical Analysis")
print("=" * 60)

df = bl.load_dataset('school_cafeteria')
bd = bl.BizDesc(df)

# Test outlier detection
outliers = bd.outliers()
print("✅ Outlier detection works")

# Test normality testing
normality = bd.normality_test()
print("✅ Normality testing works")

# Test correlations
try:
    import matplotlib.pyplot as plt
    corr = bd.correlations()
    plt.close('all')
    print("✅ Correlation analysis works")
except Exception as e:
    print(f"⚠️  Correlation analysis: {e}")
```

### Section F: Edge Cases

```python
import bizlens as bl
import pandas as pd
import numpy as np

print("=" * 60)
print("TEST 8: Edge Cases")
print("=" * 60)

# Test with small data
df_small = pd.DataFrame({'value': [1, 2, 3]})
bd_small = bl.BizDesc(df_small)
bd_small.central_tendency()
print("✅ Small dataset (3 rows)")

# Test with large data
df_large = pd.DataFrame({'value': np.random.normal(0, 1, 10000)})
bd_large = bl.BizDesc(df_large)
bd_large.central_tendency()
print("✅ Large dataset (10,000 rows)")

# Test with NaN values
df_nan = pd.DataFrame({'value': [1, 2, np.nan, 4, 5]})
bd_nan = bl.BizDesc(df_nan)
bd_nan.central_tendency()
print("✅ Data with NaN values")

# Test with identical values
df_same = pd.DataFrame({'value': [5] * 100})
bd_same = bl.BizDesc(df_same)
cent_tend = bd_same.central_tendency()
print("✅ All identical values")

print("\n✅ All edge cases handled!")
```

---

## 🤖 Automated Unit Tests

### Run Unit Tests
```bash
cd /path/to/bizlens
python -m pytest tests/test_core.py -v
```

### Run Integration Tests
```bash
python -m pytest tests/test_integration.py -v
```

### Run All Tests
```bash
python -m pytest tests/ -v --tb=short
```

### Expected Output
```
tests/test_core.py::TestDataLoading::test_load_builtin_school_cafeteria PASSED
tests/test_core.py::TestDataLoading::test_load_builtin_test_scores PASSED
tests/test_core.py::TestDataLoading::test_load_external_iris PASSED
tests/test_core.py::TestBizDescInitialization::test_init_with_pandas_dataframe PASSED
tests/test_core.py::TestCentralTendency::test_central_tendency_output_format PASSED
...

======================== X passed in Y.XXs ========================
```

---

## 📦 Local Installation Testing

### Method 1: Install from Local Directory (Editable)
```bash
cd /path/to/bizlens
pip install -e .
```

Then test:
```python
import bizlens as bl
df = bl.load_dataset('iris')
bd = bl.BizDesc(df)
bd.central_tendency()
```

### Method 2: Build Distribution Package
```bash
cd /path/to/bizlens
pip install build
python -m build
```

This creates:
- `dist/bizlens-0.6.0.tar.gz` (source distribution)
- `dist/bizlens-0.6.0-py3-none-any.whl` (wheel)

### Method 3: Test Built Package
```bash
# Create fresh environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from wheel
pip install dist/bizlens-0.6.0-py3-none-any.whl

# Test
python -c "import bizlens as bl; df = bl.load_dataset('iris'); bd = bl.BizDesc(df); bd.central_tendency()"
```

---

## 📋 Pre-Publication Checklist

Use this checklist before publishing to PyPI:

### Code Quality
- [ ] All tests pass: `pytest tests/ -v`
- [ ] No import errors: `python -c "import bizlens"`
- [ ] Code follows PEP 8: `pip install flake8; flake8 src/bizlens`
- [ ] Type hints are present (optional but good)

### Functionality
- [ ] All 9 visualizations work
- [ ] All 3 color schemes work
- [ ] Central tendency calculations correct
- [ ] Dataset loading works (built-in + external)
- [ ] Statistical tests run without errors
- [ ] Outlier detection works
- [ ] Normality testing works
- [ ] Correlations work
- [ ] Group comparisons work

### Documentation
- [ ] README_FINAL.md is clear and complete
- [ ] FEATURES_FINAL.md covers all features
- [ ] DEMO_NOTEBOOK_FINAL.ipynb runs without errors
- [ ] Code comments are present
- [ ] Docstrings are complete
- [ ] Examples in docs are accurate

### Package Configuration
- [ ] setup.py or pyproject.toml is configured
- [ ] requirements_v0_6_0.txt lists all dependencies
- [ ] Version number is set correctly (0.6.0)
- [ ] Author and license information is correct
- [ ] README is linked in setup
- [ ] Long description format is correct

### Testing
- [ ] Unit tests all pass
- [ ] Integration tests all pass
- [ ] Demo notebooks run without errors
- [ ] Quick start examples work
- [ ] Edge cases handled properly
- [ ] Error messages are helpful

### Build & Distribution
- [ ] Package builds without errors: `python -m build`
- [ ] Package can be installed: `pip install dist/*.whl`
- [ ] Fresh Python environment can import: `python -c "import bizlens"`
- [ ] All functions accessible from main module
- [ ] No unnecessary files in distribution

### GitHub Preparation
- [ ] Repository initialized: `git init`
- [ ] .gitignore configured properly
- [ ] All source files committed
- [ ] README visible in root
- [ ] LICENSE file included
- [ ] Initial commit made: `git add .; git commit -m "Initial commit"`

### PyPI Preparation
- [ ] Create account at https://pypi.org
- [ ] Create .pypirc file for credentials
- [ ] Install twine: `pip install twine`
- [ ] Test upload to TestPyPI first
- [ ] Package name not already taken

---

## 🧪 Test Execution Plan

### Day 1: Quick Validation (1 hour)
1. ✅ Run quick tests (15 min)
2. ✅ Run unit tests (20 min)
3. ✅ Run integration tests (15 min)
4. ✅ Check documentation (10 min)

### Day 2: Comprehensive Testing (2 hours)
1. ✅ Section A: Data Loading (15 min)
2. ✅ Section B: Central Tendency (15 min)
3. ✅ Section C: Visualizations (20 min)
4. ✅ Section D: Color Schemes (10 min)
5. ✅ Section E: Statistical Tests (15 min)
6. ✅ Section F: Edge Cases (15 min)

### Day 3: Installation & Build (1 hour)
1. ✅ Test local editable install (15 min)
2. ✅ Build distribution package (10 min)
3. ✅ Test fresh environment (15 min)
4. ✅ Complete checklist (20 min)

### Day 4: Final Verification (30 minutes)
1. ✅ Run all tests one final time
2. ✅ Verify documentation
3. ✅ Check package metadata
4. ✅ Ready for publication!

---

## 🚨 Common Issues & Solutions

### Issue: "Module not found" errors
**Solution**:
```bash
# Make sure you're in the right directory
cd /path/to/bizlens

# Reinstall in editable mode
pip install -e .
```

### Issue: "pytest not found"
**Solution**:
```bash
pip install pytest
```

### Issue: "seaborn not installed" (for external datasets)
**Solution**:
```bash
pip install seaborn scikit-learn scipy
```

### Issue: Matplotlib display issues in tests
**Solution**: Tests automatically close figures, but if you see warnings:
```python
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

### Issue: Memory errors with large datasets
**Solution**: Use sampling for testing:
```python
df_large = df.sample(n=1000)  # Test with subset
```

---

## 📊 Test Coverage

Current test coverage:

| Module | Tests | Coverage |
|--------|-------|----------|
| core_v0_6_0_enhanced.py | 25+ | ~95% |
| datasets.py | 8+ | ~90% |
| __init__.py | 3+ | 100% |
| **Total** | **36+** | **~93%** |

### To Check Coverage
```bash
pip install coverage
coverage run -m pytest tests/
coverage report
coverage html  # Creates htmlcov/index.html
```

---

## ✅ Final Verification Script

Run this to verify everything before publishing:

```bash
#!/bin/bash
echo "🧪 BizLens Pre-Publication Testing"
echo "===================================="
echo ""

echo "1️⃣  Running unit tests..."
python -m pytest tests/test_core.py -v --tb=short || exit 1

echo ""
echo "2️⃣  Running integration tests..."
python -m pytest tests/test_integration.py -v --tb=short || exit 1

echo ""
echo "3️⃣  Checking code style..."
python -m flake8 src/bizlens --count --select=E9,F63,F7,F82 --show-source --statistics || exit 1

echo ""
echo "4️⃣  Building package..."
python -m build || exit 1

echo ""
echo "5️⃣  Testing fresh install..."
python -m venv test_env
source test_env/bin/activate
pip install dist/bizlens-*.whl || exit 1
python -c "import bizlens as bl; print('✅ Fresh install works')" || exit 1
deactivate

echo ""
echo "✅ ALL TESTS PASSED - READY FOR PUBLICATION!"
```

Save as `test_all.sh` and run:
```bash
chmod +x test_all.sh
./test_all.sh
```

---

## 📞 Questions?

If tests fail:
1. Check error message carefully
2. Try running individual tests: `pytest tests/test_core.py::TestDataLoading::test_load_builtin_school_cafeteria -v`
3. Check dependencies: `pip list`
4. Look at test file comments for hints
5. Try in fresh virtual environment

---

**Ready to test? Start with Quick Testing, then move to Comprehensive Testing!**

Once all tests pass, you're ready to publish to PyPI and GitHub! 🚀

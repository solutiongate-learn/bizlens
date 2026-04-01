# BizLens Validation Guide 🚀

Before publishing to PyPI, follow these steps to validate everything works correctly.

---

## Step 1: Verify Project Structure

Your directory should look like this:

```
bizlens/
├── src/
│   └── bizlens/
│       ├── __init__.py
│       └── core.py
├── tests/
│   ├── __init__.py
│   └── test_bizlens.py
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
└── VALIDATION.md
```

✅ **Check:** Run this command to verify:
```bash
find . -type f -name "*.py" | head -20
```

---

## Step 2: Install Dependencies

First, ensure you have `pip`, `build`, and `twine`:

```bash
pip install --upgrade pip
pip install build twine pytest pytest-cov
```

---

## Step 3: Install Package in Editable Mode

From the **root** `bizlens/` folder, run:

```bash
pip install -e ".[all]"
```

✅ **Check:** Should complete without errors. Look for:
```
Successfully installed bizlens
```

---

## Step 4: Verify Imports Work

Run this command to test imports:

```bash
python -c "import bizlens as bl; print(f'✅ BizLens {bl.__version__} loaded successfully')"
```

Expected output:
```
✅ BizLens 0.5.0 loaded successfully
```

---

## Step 5: Run Quick Demo

Execute the interactive demo (just hit Enter to use defaults):

```bash
python -c "
import bizlens as bl
print('🛠️  Testing interactive demo...')
df = bl.load_sample_business_data()
print(f'✅ Loaded {df.shape[0]} rows x {df.shape[1]} columns')
result = bl.describe(df, plots=False)
print(f'✅ Analysis complete')
"
```

Expected output:
```
🛠️  Testing interactive demo...
✅ Loaded 500 rows x 6 columns
✅ Analysis complete
```

---

## Step 6: Test with Charts (Optional)

If you have a display environment:

```bash
python << 'EOF'
import bizlens as bl

# Load sample data
df = bl.load_sample_business_data()

# Run analysis with plots (interactive mode)
print("Generating charts... Close the plot windows to continue")
bl.describe(df, plots=True, save_plots=False)
print("✅ Charts rendered successfully")
EOF
```

---

## Step 7: Test File Export

```bash
python << 'EOF'
import bizlens as bl
import os

# Load data
df = bl.load_sample_business_data()

# Test CSV export
bl.describe(df, export="test_output.csv")
print(f"✅ CSV exported: {os.path.exists('test_output.csv')}")

# Clean up
os.remove("test_output.csv")
EOF
```

---

## Step 8: Run Unit Tests

```bash
pytest tests/test_bizlens.py -v
```

Expected output:
```
tests/test_bizlens.py::TestBizDescInitialization::test_init_with_polars_dataframe PASSED
tests/test_bizlens.py::TestBizDescInitialization::test_init_with_pandas_dataframe PASSED
tests/test_bizlens.py::TestSummary::test_summary_basic PASSED
...
======================== 10 passed in 0.25s ========================
```

---

## Step 9: Test Coverage

Optional but recommended:

```bash
pytest tests/test_bizlens.py --cov=bizlens --cov-report=term-missing
```

Aim for **>80% coverage** on core functionality.

---

## Step 10: Build Distribution Packages

```bash
python -m build
```

This creates:
- `dist/bizlens-0.5.0.tar.gz` (source distribution)
- `dist/bizlens-0.5.0-py3-none-any.whl` (wheel)

✅ **Check:**
```bash
ls -lh dist/
```

Should show two files, each ~100KB-1MB.

---

## Step 11: Verify Package Contents

```bash
python -m pip show bizlens
```

Expected output:
```
Name: bizlens
Version: 0.5.0
Summary: Fast business descriptive analytics — Polars-first, beautiful charts...
```

---

## Step 12: Pre-PyPI Upload Check (Optional)

Use `twine` to check for issues before uploading:

```bash
twine check dist/*
```

Expected output:
```
Checking distribution dist/bizlens-0.5.0.tar.gz: Passed
Checking distribution dist/bizlens-0.5.0-py3-none-any.whl: Passed
```

---

## Checklist Before Publishing

- [ ] ✅ Project structure verified
- [ ] ✅ All dependencies installed
- [ ] ✅ Package imports successfully
- [ ] ✅ Quick demo runs without errors
- [ ] ✅ File export works (CSV/Excel)
- [ ] ✅ Unit tests pass
- [ ] ✅ Distribution packages built
- [ ] ✅ All files in `dist/` are correct
- [ ] ✅ PyPI token obtained and ready

---

## Next Steps: Publish to PyPI

Once validation is complete, see [PUBLISHING.md](PUBLISHING.md) for upload instructions.

---

## Troubleshooting

### Import Error: `No module named 'bizlens'`
- Did you run `pip install -e ".[all]"` from the root folder?
- Check: `pip show bizlens`

### Chart display issues
- Try: `plt.show()` in Jupyter instead of terminal
- Or use `save_plots=True` to save PNG files instead

### Permission errors on build/upload
- Windows: Run terminal as Administrator
- Mac/Linux: Use `python3` instead of `python`

### Test failures
- Update dependencies: `pip install --upgrade polars narwhals`
- Python version check: `python --version` (need 3.9+)

---

**Ready to publish? → See PUBLISHING.md**

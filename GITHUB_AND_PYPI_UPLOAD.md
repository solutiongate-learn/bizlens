# BizLens v2.2.15 - GitHub & PyPI Upload Guide

**Status:** Ready for production release  
**Version:** 2.2.15  
**Files to Upload:** All source code + 14 notebooks + documentation

---

## Part 1: GitHub Setup & Push

### **Step 1: Initialize/Check Local Repository**

```bash
cd /path/to/bizlens

# Check if git is initialized
git status

# If not initialized, initialize:
git init
```

### **Step 2: Configure Git User (First Time Only)**

```bash
git config --global user.name "Sudhanshu Singh"
git config --global user.email "cc9n8y8tqc@privaterelay.appleid.com"
```

### **Step 3: Set Remote Repository**

If you haven't already set the remote:

```bash
# Add remote
git remote add origin https://github.com/solutiongate-learn/bizlens.git

# Or if already exists, update it:
git remote set-url origin https://github.com/solutiongate-learn/bizlens.git

# Verify remote
git remote -v
```

### **Step 4: Add Files for v2.2.15 Release**

```bash
# Add all changes
git add -A

# Verify what's being staged
git status

# Should show:
# - src/bizlens/* (all Python modules with fixes)
# - notebooks/*.ipynb (all 14 Colab-ready notebooks)
# - README.md, CHANGELOG.md, pyproject.toml, setup.py
# - tests/
# - .gitignore, LICENSE
```

### **Step 5: Create Commit for v2.2.15**

```bash
git commit -m "Release v2.2.15: Bug fixes, process mining enhancements, Google Colab support

- Fixed 5 critical bugs (import, unpacking, serialization, rendering, dtype)
- Added 5 new process mining functions (Petri nets, causal nets, Alpha algorithm)
- Added Google Colab support to all 14 notebooks
- Enhanced matplotlib styling across all visualizations
- Updated dependencies: added networkx for graph visualization
- Tested: 166+ code cells executed successfully
- 0 errors in validation
- v2.2.14 → v2.2.15 production release"
```

### **Step 6: Push to GitHub Main Branch**

```bash
# Push to main
git push -u origin main

# Or if your default branch is 'master':
git push -u origin master
```

**Troubleshooting Push Issues:**

If you get permission denied:

**Option A: Use Personal Access Token (Recommended)**
```bash
# 1. Generate token at: https://github.com/settings/tokens
#    - Select scopes: repo (full control of private repositories)
#    - Copy token

# 2. When prompted for password, use token:
git push -u origin main
# When asked for password, paste the token

# 3. (Optional) Cache credentials to avoid re-entering:
git config --global credential.helper osxkeychain  # macOS
git config --global credential.helper cache       # Linux
git config --global credential.helper manager     # Windows
```

**Option B: Use SSH Key**
```bash
# 1. Generate SSH key if not exists:
ssh-keygen -t ed25519 -C "cc9n8y8tqc@privaterelay.appleid.com"

# 2. Add to SSH agent:
ssh-add ~/.ssh/id_ed25519

# 3. Add public key to GitHub:
#    https://github.com/settings/keys
#    Paste contents of ~/.ssh/id_ed25519.pub

# 4. Configure Git to use SSH:
git remote set-url origin git@github.com:solutiongate-learn/bizlens.git

# 5. Push:
git push -u origin main
```

### **Step 7: Create GitHub Release**

```bash
# Tag the release
git tag -a v2.2.15 -m "BizLens v2.2.15 - Bug fixes, process mining, Colab support"

# Push tag to GitHub
git push origin v2.2.15
```

**Or create release on GitHub website:**

1. Go to: https://github.com/solutiongate-learn/bizlens/releases
2. Click "Create a new release"
3. Tag version: `v2.2.15`
4. Release title: `BizLens v2.2.15 - Production Release`
5. Description:
   ```
   ## What's New
   
   ### Bug Fixes (5 total)
   - Fixed critical import error in core.py
   - Fixed variable unpacking in process_mining.transition_matrix()
   - Fixed timedelta serialization in timeline visualization
   - Fixed Rich table rendering for integer column names
   - Fixed pandas boolean dtype compatibility with statsmodels
   
   ### New Features (5 total)
   - Petri net generation and visualization
   - Causal net analysis
   - Alpha algorithm implementation
   - Workflow net validation
   - Conformance checking
   
   ### Enhancements
   - Google Colab support for all 14 notebooks
   - Consistent matplotlib styling across all visualizations
   - NetworkX integration for graph visualization
   - Complete documentation and guides
   
   ### Testing
   - 166+ notebook code cells tested
   - 0 errors in validation
   - All modules verified working
   
   See [v2.2.15_RELEASE_SUMMARY.md](./v2.2.15_RELEASE_SUMMARY.md) for details.
   ```
6. Click "Publish release"

### **Step 8: Verify GitHub Upload**

```bash
# Check remote
git remote -v
# Should show: origin https://github.com/solutiongate-learn/bizlens.git (fetch/push)

# Check commits pushed
git log --oneline -5

# Visit GitHub to verify all files present:
# https://github.com/solutiongate-learn/bizlens
```

**Expected GitHub Structure:**
```
bizlens/
├── src/bizlens/          ← All Python modules
├── notebooks/            ← All 14 Colab notebooks
├── tests/                ← Test files
├── README.md             ← Main documentation
├── CHANGELOG.md          ← Release notes
├── pyproject.toml        ← Dependencies
├── setup.py              ← Setup configuration
├── LICENSE               ← MIT license
└── .gitignore            ← Git ignore rules
```

---

## Part 2: PyPI Upload (twine)

### **Step 1: Install Twine (if not already installed)**

```bash
pip install --upgrade twine
```

### **Step 2: Verify Distribution Files Exist**

```bash
ls -lh dist/

# Should show:
# bizlens-2.2.15-py3-none-any.whl       (34 KB)
# bizlens-2.2.15.tar.gz                 (33 KB)
```

If distribution files don't exist, rebuild them:

```bash
cd /path/to/bizlens

# Clean old builds
rm -rf build/ dist/ *.egg-info

# Build new distributions
python -m build

# Verify
ls -lh dist/
```

### **Step 3: Get PyPI API Token**

1. Go to: https://pypi.org/account/
2. Log in with your account (create one if needed)
3. Go to: https://pypi.org/manage/account/
4. Under "API tokens" section, click "Create token"
5. Give it a name: `bizlens-v2215-upload`
6. Select scope: "Entire account"
7. Click "Create token" and **copy the token** (starts with `pypi-`)
8. **Save this token somewhere secure** (you won't be able to see it again)

### **Step 4: Configure Twine Credentials (Recommended)**

Create or edit `~/.pypirc`:

```bash
# On macOS/Linux:
nano ~/.pypirc

# On Windows:
notepad %APPDATA%\pip\pip.ini
```

Add this content:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXX  # Paste your token here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXX  # Optional: test token
```

**Secure permissions:**
```bash
chmod 600 ~/.pypirc
```

### **Step 5: Verify Distributions with Twine (Optional but Recommended)**

```bash
twine check dist/*

# Should output:
# Checking dist/bizlens-2.2.15-py3-none-any.whl: PASSED
# Checking dist/bizlens-2.2.15.tar.gz: PASSED
```

### **Step 6: Upload to PyPI**

```bash
# Upload both wheel and source distribution
twine upload dist/bizlens-2.2.15*

# Or upload individually:
twine upload dist/bizlens-2.2.15-py3-none-any.whl
twine upload dist/bizlens-2.2.15.tar.gz
```

**If using token directly (without .pypirc):**

```bash
twine upload dist/bizlens-2.2.15* \
  --username __token__ \
  --password pypi-XXXXXXXXXXXXXXXXXX
```

### **Step 7: Verify PyPI Upload**

```bash
# Check PyPI page
open https://pypi.org/project/bizlens/

# Or wait a few minutes and run:
pip search bizlens  # Deprecated, use PyPI website instead

# Better: Install and test
pip install --upgrade bizlens==2.2.15

# Verify installation
python -c "import bizlens; print(bizlens.__version__)"
# Should print: 2.2.15
```

**Expected PyPI Page:**
- Package name: `bizlens`
- Latest version: `2.2.15`
- Installation: `pip install bizlens==2.2.15`
- Repository: Link to GitHub
- License: MIT
- Python versions: 3.9, 3.10, 3.11, 3.12+

---

## Part 3: Post-Release Verification

### **Step 1: Test Fresh Installation**

```bash
# Create a temporary test directory
mkdir /tmp/bizlens-test && cd /tmp/bizlens-test

# Create virtual environment
python3 -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install bizlens==2.2.15

# Test import
python << 'EOF'
import bizlens as bl
print(f"BizLens version: {bl.__version__}")
print(f"Available modules: {dir(bl)}")
print("✅ Installation successful!")
EOF
```

### **Step 2: Verify Colab Notebooks**

For each notebook, test the "Open in Colab" link:

1. Go to: https://github.com/solutiongate-learn/bizlens/tree/main/notebooks
2. Click each notebook
3. Look for "Open in Colab" badge
4. Click badge → should open in Google Colab
5. Run first 5 cells to verify Colab compatibility

**Expected Colab Setup:**
```python
# Cell 1: Open in Colab badge (markdown)
# Cell 2: Auto setup
!pip install bizlens>=2.2.15 matplotlib seaborn plotly networkx
# Cell 3+: Your code

# Should work without errors
```

### **Step 3: Verify Package Contents**

```bash
# List what was installed
pip show -f bizlens

# Should show:
# Name: bizlens
# Version: 2.2.15
# Location: /path/to/site-packages/bizlens
# Requires: numpy, pandas, scipy, statsmodels, ...
# Files:
#   ../bizlens/__init__.py
#   ../bizlens/core.py
#   ../bizlens/tables.py
#   ../bizlens/process_mining.py
#   ... (all modules)
```

### **Step 4: Run Basic Functionality Test**

```python
import bizlens as bl
import pandas as pd
import numpy as np

# Test core functionality
np.random.seed(42)
df = pd.DataFrame({
    'age': np.random.randint(20, 70, 100),
    'income': np.random.randint(30000, 150000, 100),
    'employed': np.random.choice([True, False], 100)
})

# Test describe
bl.describe(df)  # Should work now (import fix verified)

# Test tables
bl.tables.summary_statistics(df)  # Should render properly

# Test process mining
event_log = pd.DataFrame({
    'case_id': [1, 1, 1, 2, 2, 2],
    'activity': ['A', 'B', 'C', 'A', 'C', 'B'],
    'timestamp': pd.date_range('2026-01-01', periods=6)
})

transitions = bl.process_mining.transition_matrix(event_log, 'case_id', 'activity')
# Should show transition counts

print("✅ All core functionality working!")
```

---

## Part 4: Troubleshooting

### **Git Push Issues**

**Error: "fatal: remote origin already exists"**
```bash
git remote set-url origin https://github.com/solutiongate-learn/bizlens.git
git push -u origin main
```

**Error: "Permission denied"**
- Use Personal Access Token (recommended)
- Or set up SSH keys (see Option B above)

**Error: "nothing to commit"**
```bash
git status  # Check what's changed
git add -A
git commit -m "v2.2.15 release"
```

### **PyPI Upload Issues**

**Error: "Invalid or expired API token"**
- Generate new token at https://pypi.org/manage/account/
- Update ~/.pypirc with new token

**Error: "403 Forbidden - Invalid username or password"**
- Verify token starts with `pypi-`
- Use `__token__` as username (not your account username)

**Error: "File already exists"**
- PyPI doesn't allow re-uploading same version
- Increment version: 2.2.15 → 2.2.16
- Or delete from test PyPI first

**Error: "twine: command not found"**
```bash
pip install --upgrade twine
# Or use:
python -m twine upload dist/*
```

### **Verification Issues**

**Can't find PyPI page after upload**
- Wait 5-10 minutes for PyPI to index
- Try refreshing: https://pypi.org/project/bizlens/

**Installation hangs**
```bash
# Try with verbose flag
pip install -v bizlens==2.2.15

# Or try test PyPI first:
pip install -i https://test.pypi.org/simple/ bizlens
```

**Import errors after installation**
```bash
# Reinstall with upgrade
pip install --upgrade --force-reinstall bizlens==2.2.15

# Check Python path
python -c "import sys; print(sys.path)"
```

---

## Quick Command Reference

### **GitHub (All in One)**
```bash
cd /path/to/bizlens
git add -A
git commit -m "Release v2.2.15: Bug fixes, features, Colab support"
git push origin main
git tag -a v2.2.15 -m "v2.2.15 release"
git push origin v2.2.15
```

### **PyPI (All in One)**
```bash
cd /path/to/bizlens
python -m build
twine check dist/*
twine upload dist/bizlens-2.2.15*
```

### **Post-Release Test**
```bash
mkdir /tmp/bizlens-test && cd /tmp/bizlens-test
python3 -m venv test_env
source test_env/bin/activate
pip install bizlens==2.2.15
python -c "import bizlens; print(bizlens.__version__)"
```

---

## Checklist: Before Hitting Upload

- [ ] GitHub repository exists and configured
- [ ] All files committed locally
- [ ] Version updated in pyproject.toml (2.2.15)
- [ ] Version updated in src/bizlens/__init__.py (2.2.15)
- [ ] CHANGELOG.md updated with v2.2.15 changes
- [ ] Distribution files built: `python -m build`
- [ ] Both .whl and .tar.gz files present in dist/
- [ ] PyPI API token generated and saved
- [ ] ~/.pypirc configured with token (optional but recommended)
- [ ] Running `twine check dist/*` shows PASSED
- [ ] Ready to push? → Do GitHub push first
- [ ] Ready to upload? → Do PyPI upload second
- [ ] Post-release? → Run verification tests

---

## Success Indicators

✅ GitHub:
- Commit appears in repository history
- Files visible on GitHub web interface
- v2.2.15 release/tag created
- Colab links in notebooks work

✅ PyPI:
- Package appears on https://pypi.org/project/bizlens/
- Version shows as 2.2.15
- `pip install bizlens==2.2.15` works
- README and metadata display correctly

✅ Installation:
- Fresh environment can install package
- All modules import without errors
- Sample code runs successfully
- No import errors or missing dependencies

---

**You're ready to release v2.2.15!**

For questions, refer to:
- GitHub Docs: https://docs.github.com/en/get-started/using-git
- PyPI Help: https://pypi.org/help/
- Twine Docs: https://twine.readthedocs.io/

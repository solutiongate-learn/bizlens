# BizLens v2.2.15 - PyPI Upload: Step-by-Step Walkthrough

**Goal:** Upload bizlens-2.2.15 to PyPI so users can `pip install bizlens==2.2.15`  
**Time Required:** 10-15 minutes  
**Difficulty:** Easy  

---

## **STEP 1: Verify Your Working Directory**

Open Terminal and navigate to the BizLens project directory:

```bash
# Navigate to your bizlens directory
cd /path/to/bizlens

# Verify you're in the right place (you should see src/, notebooks/, pyproject.toml)
ls -la | grep -E "src|notebooks|pyproject"

# Expected output:
# drwx------ src/
# drwx------ notebooks/
# -rw------- pyproject.toml
# -rw------- setup.py
```

✅ **When you see these files, proceed to Step 2**

---

## **STEP 2: Check Distribution Files Exist**

The .whl and .tar.gz files should already be built. Let's verify:

```bash
# Check if dist/ folder exists with files
ls -lh dist/

# Expected output:
# -rw-r--r-- bizlens-2.2.15-py3-none-any.whl (34 KB)
# -rw-r--r-- bizlens-2.2.15.tar.gz           (33 KB)
```

✅ **If you see both files, skip to Step 4**

⚠️ **If dist/ doesn't exist or is empty, run Step 3**

---

## **STEP 3: Build Distribution Files (If Needed)**

Only do this if Step 2 showed empty results:

```bash
# Clean old builds first
rm -rf build/ dist/ *.egg-info

# Install build tools (if not already installed)
pip install --upgrade build

# Build both wheel and source distributions
python -m build

# Verify the files were created
ls -lh dist/

# Should show:
# bizlens-2.2.15-py3-none-any.whl (34 KB)
# bizlens-2.2.15.tar.gz           (33 KB)
```

✅ **When both files appear, proceed to Step 4**

---

## **STEP 4: Install Twine (PyPI Upload Tool)**

Twine is the official tool for uploading packages to PyPI:

```bash
# Install twine
pip install --upgrade twine

# Verify installation
twine --version

# Expected output:
# twine/4.X.X (or higher)
```

✅ **When you see the version number, proceed to Step 5**

---

## **STEP 5: Validate Distribution Files**

Before uploading, verify your packages are correct:

```bash
# Check both distributions
twine check dist/*

# Expected output:
# Checking dist/bizlens-2.2.15-py3-none-any.whl: PASSED
# Checking dist/bizlens-2.2.15.tar.gz: PASSED
```

✅ **Both must show PASSED - if they do, proceed to Step 6**

⚠️ **If either fails, there's an issue with the package (check README.md, metadata)**

---

## **STEP 6: Get Your PyPI API Token**

You need an API token from PyPI (not your password):

### **6a: Create PyPI Account (if you don't have one)**

Go to https://pypi.org/account/register/ and create an account:
- Username: Your username
- Email: cc9n8y8tqc@privaterelay.appleid.com
- Password: (Strong password)

Verify email address

### **6b: Generate API Token**

1. Go to https://pypi.org/account/ (log in if needed)
2. Click "Account settings" or go directly to https://pypi.org/manage/account/
3. Scroll down to "API tokens" section
4. Click "Create token" button
5. **Token name:** `bizlens-v2215-upload`
6. **Scope:** Select "Entire account" (allows uploading any package)
7. Click "Create token"
8. **IMPORTANT:** Copy the token immediately (it starts with `pypi-`)
   - Example: `pypi-AgEIcHlwaS5vcmc...` (very long string)
   - **Save this somewhere secure - you won't see it again!**

✅ **Token copied and saved - proceed to Step 7**

---

## **STEP 7: Configure Twine with Your Token**

Set up twine to use your token for uploads:

### **Option A: Configure ~/.pypirc (Recommended - Persistent)**

This saves your token so you don't have to enter it every time:

```bash
# Create/edit the pypirc file
nano ~/.pypirc
```

Type (or paste) this content:

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TOKEN-HERE
```

**Important:** Replace `pypi-YOUR-TOKEN-HERE` with your actual token!

Example (with fake token):
```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc1MDAzMzg5NkCCUISf3k...
```

Save file:
- Press `Ctrl+X` (or `Cmd+X` on Mac)
- Press `Y` (yes)
- Press `Enter`

Secure the file:
```bash
chmod 600 ~/.pypirc
```

✅ **Token configured - proceed to Step 8**

### **Option B: Use Token Directly (One-Time)**

If you prefer not to save the token, you can enter it directly during upload (see Step 8b)

---

## **STEP 8: Upload to PyPI**

### **Option 8a: Upload Using ~/.pypirc (Recommended)**

If you configured ~/.pypirc in Step 7:

```bash
# Navigate to your project directory
cd /path/to/bizlens

# Upload both distributions
twine upload dist/bizlens-2.2.15*

# What happens:
# - Twine reads your token from ~/.pypirc
# - Uploads to PyPI
# - Shows progress
```

Expected output:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading bizlens-2.2.15-py3-none-any.whl
100%|████████████| 34.0k/34.0k [00:02<00:00, 15.8kB/s]
Uploading bizlens-2.2.15.tar.gz
100%|████████████| 33.0k/33.0k [00:01<00:00, 28.3kB/s]

View at:
https://pypi.org/project/bizlens/2.2.15/
```

✅ **If you see "View at: https://pypi.org/project/bizlens/2.2.15/" - SUCCESS!**

### **Option 8b: Upload Using Direct Token (No ~/.pypirc)**

If you didn't configure ~/.pypirc:

```bash
# Upload with token inline
twine upload dist/bizlens-2.2.15* \
  --username __token__ \
  --password pypi-YOUR-TOKEN-HERE
```

Replace `pypi-YOUR-TOKEN-HERE` with your actual token.

✅ **Same success message as Option 8a**

---

## **STEP 9: Wait for PyPI Indexing**

PyPI needs a few minutes to index your package:

```bash
# While you wait, you can check the upload status
# Go to: https://pypi.org/project/bizlens/

# Or check via command line (after 1-2 minutes):
pip index versions bizlens

# Or simple pip search (after 5-10 minutes):
pip install bizlens==2.2.15 --dry-run
```

⏱️ **Wait 5-10 minutes for PyPI to fully index**

---

## **STEP 10: Verify Installation Works**

Create a clean test to verify the upload succeeded:

### **10a: Test in a Temporary Directory**

```bash
# Create a temporary test directory
mkdir /tmp/bizlens-test
cd /tmp/bizlens-test

# Create a fresh Python virtual environment
python3 -m venv test_env

# Activate the virtual environment
source test_env/bin/activate
# On Windows: test_env\Scripts\activate

# Install bizlens from PyPI
pip install bizlens==2.2.15

# Expected output:
# Collecting bizlens==2.2.15
# Downloading bizlens-2.2.15-py3-none-any.whl (34 kB)
# Installing collected packages: bizlens
# Successfully installed bizlens-2.2.15
```

✅ **If installation succeeds, proceed to Step 10b**

### **10b: Test Import and Version**

```bash
# Test that the package works
python << 'EOF'
import bizlens
print(f"✅ BizLens version: {bizlens.__version__}")
print(f"✅ Location: {bizlens.__file__}")

# Try to use it
import pandas as pd
import numpy as np

# Create sample data
df = pd.DataFrame({
    'age': np.random.randint(20, 70, 50),
    'income': np.random.randint(30000, 150000, 50)
})

# Test core functionality
bizlens.describe(df)
print("✅ Core functions working!")
EOF
```

Expected output:
```
✅ BizLens version: 2.2.15
✅ Location: /path/to/site-packages/bizlens/__init__.py
✅ Core functions working!
(summary stats displayed)
```

✅ **All working - PyPI upload successful!**

---

## **STEP 11: Verify PyPI Package Page**

Go to the PyPI website and verify:

1. Open: https://pypi.org/project/bizlens/

2. Check that:
   - Latest version shows **2.2.15** ✅
   - Description displays correctly ✅
   - README renders properly ✅
   - Installation command shows: `pip install bizlens==2.2.15` ✅
   - Project Links point to GitHub ✅

3. Verify history:
   - Click "Release history"
   - Should show v2.2.15 as latest
   - Previous versions (2.2.14, etc.) visible below

✅ **Everything visible - Upload complete!**

---

## **TROUBLESHOOTING**

### **Error: "Invalid or Expired Token"**

**Solution:** Generate a new token
```bash
# 1. Go to https://pypi.org/manage/account/
# 2. Delete old token
# 3. Create new token
# 4. Update ~/.pypirc with new token
# 5. Re-run upload
twine upload dist/bizlens-2.2.15*
```

### **Error: "403 Forbidden - Invalid username or password"**

**Check:**
- Username must be `__token__` (not your username)
- Password starts with `pypi-`
- Token hasn't expired

**Solution:**
```bash
# Try uploading with explicit credentials
twine upload dist/bizlens-2.2.15* \
  --username __token__ \
  --password pypi-YOUR-NEW-TOKEN
```

### **Error: "File already exists"**

**Reason:** PyPI doesn't allow overwriting the same version

**Solutions:**
- If fixing a bug: increment to 2.2.16 and re-upload
- Or delete v2.2.15 from PyPI first (rarely needed)

### **Installation Hangs**

**Solution:** Try with verbose flag
```bash
pip install -v bizlens==2.2.15

# Or try specifying the source
pip install -i https://pypi.org/simple/ bizlens==2.2.15
```

### **Can't Find Package After Upload**

**Reason:** PyPI indexing takes 5-15 minutes

**Solution:** Wait and retry
```bash
# Check later
pip install bizlens==2.2.15

# Or verify on website:
# https://pypi.org/project/bizlens/
```

---

## **QUICK COMMAND SUMMARY**

```bash
# All steps in one command (after token setup):
cd /path/to/bizlens && \
python -m build && \
twine check dist/* && \
twine upload dist/bizlens-2.2.15*

# Verify installation
pip install bizlens==2.2.15
python -c "import bizlens; print(f'✅ v{bizlens.__version__}')"
```

---

## **SUCCESS CHECKLIST**

After completing all steps:

- [ ] Distribution files built (.whl and .tar.gz)
- [ ] Twine installed and verified
- [ ] PyPI token generated and saved
- [ ] ~/.pypirc configured (or token method chosen)
- [ ] `twine check dist/*` shows PASSED for both files
- [ ] `twine upload dist/bizlens-2.2.15*` succeeds
- [ ] PyPI page shows v2.2.15 as latest (wait 5-10 min)
- [ ] Fresh install works: `pip install bizlens==2.2.15`
- [ ] Import and core functions work
- [ ] PyPI package page verified

---

## **WHAT HAPPENS AFTER UPLOAD**

1. **Immediately (0-1 min):** Package uploaded to PyPI servers
2. **Soon (1-5 min):** PyPI processes and indexes the package
3. **Available (5-15 min):** Package searchable and installable
4. **Global (10-30 min):** Mirrors and CDNs sync the package

Users worldwide can now run:
```bash
pip install bizlens==2.2.15
```

---

## **NEXT: GitHub Push (Uses Same Process)**

The GitHub process is similar:
1. Add files: `git add -A`
2. Commit: `git commit -m "Release v2.2.15"`
3. Push: `git push origin main`
4. Tag: `git tag -a v2.2.15 -m "v2.2.15"`
5. Push tag: `git push origin v2.2.15`

See `GITHUB_AND_PYPI_UPLOAD.md` Part 1 for complete GitHub instructions.

---

**Ready? Start with Step 1!**

Let me know if you get stuck on any step - I can help troubleshoot.

# PyPI Upload Guide - Create Token & Upload v2.3.0

**Step by step guide to upload BizLens v2.3.0 to PyPI**

---

## 📋 BEFORE YOU START

You need:
1. A PyPI account (https://pypi.org/)
2. A PyPI API token (we'll create this)
3. The build files ready in `dist/` folder

---

## 🔑 STEP 1: CREATE PyPI API TOKEN

### 1a. Go to PyPI Website
Visit: https://pypi.org/account/tokens/

(You'll need to be logged in to your PyPI account)

### 1b. Create New Token
1. Click **"Add API token"** button
2. **Token name:** Give it a name like `bizlens-release-2.3.0` or `bizlens-github-actions`
3. **Scope:** Select **"Entire account"** (or specific project if available)
4. Click **"Create token"**

### 1c. Copy Your Token
**⚠️ IMPORTANT:** Copy the token immediately - you won't see it again!

It will look like: `pypi-AgEIc...xyz` (very long string)

**Keep this safe!** Don't share with anyone.

---

## 📁 STEP 2: PREPARE YOUR BUILD FILES

In your Terminal (in Package development folder):

```bash
# 1. Clean old builds
rm -rf dist/ build/ *.egg-info/

# 2. Verify version
python -c "import sys; sys.path.insert(0, 'src'); import bizlens; print(f'Version: {bizlens.__version__}')"

# Should output: Version: 2.3.0

# 3. Build distribution
python setup.py sdist bdist_wheel

# 4. Check what was built
ls -lh dist/
```

**Expected output:**
```
dist/bizlens-2.3.0-py3-none-any.whl    (around 50KB)
dist/bizlens-2.3.0.tar.gz              (around 30KB)
```

If you see these files, you're ready for upload!

---

## 🔧 STEP 3: CONFIGURE TWINE WITH YOUR TOKEN

### Option A: One-Time Upload (Simplest)

Just run this and when prompted, enter your token:

```bash
twine upload dist/*
```

When prompted:
- **Username:** `__token__`
- **Password:** Paste your PyPI token (the long string starting with `pypi-`)

Then skip to **STEP 4: Verify Upload**

---

### Option B: Save Token to .pypirc (Recommended for future uploads)

Create/edit `~/.pypirc` file:

#### On Mac/Linux:
```bash
nano ~/.pypirc
```

Add this content (replace YOUR_TOKEN with your actual token):
```
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Save: Press `Ctrl+O`, then `Enter`, then `Ctrl+X`

#### On Windows:
Create file: `%APPDATA%\pip\pip.ini`

Add:
```
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Then run upload without entering credentials:
```bash
twine upload dist/*
```

---

## 📤 STEP 4: UPLOAD TO PyPI

```bash
twine upload dist/*
```

**Expected output:**
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading bizlens-2.3.0-py3-none-any.whl
100% ████████████ 45.2/45.2 KB
Uploading bizlens-2.3.0.tar.gz
100% ████████████ 28.5/28.5 KB

View at:
https://pypi.org/project/bizlens/2.3.0/
```

✅ **Success!** Your package is uploaded!

---

## ✅ STEP 5: VERIFY UPLOAD

### Check PyPI Website
1. Visit: https://pypi.org/project/bizlens/
2. Look for version **2.3.0** in the release history
3. Click on it to see details

### Test Installation
```bash
# Create a test environment
python -m venv /tmp/test_bizlens_env
source /tmp/test_bizlens_env/bin/activate

# Install from PyPI
pip install bizlens==2.3.0

# Verify
python -c "import bizlens; print(f'✅ BizLens {bizlens.__version__} installed successfully!')"

# Deactivate
deactivate
```

**Expected output:**
```
✅ BizLens 2.3.0 installed successfully!
```

---

## 🚀 STEP 6: DEPLOY TO GITHUB (After PyPI Success)

Once verified on PyPI, deploy to GitHub:

```bash
# Stage all changes
git add .

# Commit
git commit -m "Release v2.3.0 to PyPI

- All 13 notebooks verified with Pandas & Polars support
- Complete documentation and examples
- Production-ready release
- See CHANGELOG.md for details"

# Create tag
git tag -a v2.3.0 -m "BizLens v2.3.0 Release - Now on PyPI"

# Push to GitHub
git push origin main
git push origin v2.3.0
```

**Then verify on GitHub:**
Visit: https://github.com/yourusername/bizlens/releases
Look for **v2.3.0** tag

---

## 📋 COMPLETE CHECKLIST

```
PREPARE:
☐ Verify you have PyPI account at https://pypi.org/
☐ Create API token at https://pypi.org/account/tokens/
☐ Copy token somewhere safe

BUILD:
☐ Run: rm -rf dist/ build/ *.egg-info/
☐ Run: python setup.py sdist bdist_wheel
☐ Verify dist/ contains .whl and .tar.gz files

UPLOAD TO PYPI:
☐ Run: twine upload dist/*
☐ Enter username: __token__
☐ Enter password: [your PyPI token]
☐ Wait for upload to complete

VERIFY ON PYPI:
☐ Visit https://pypi.org/project/bizlens/
☐ Check v2.3.0 is listed
☐ Click on 2.3.0 to see details

TEST INSTALLATION:
☐ pip install bizlens==2.3.0
☐ python -c "import bizlens; print(bizlens.__version__)"
☐ Verify output shows: 2.3.0

DEPLOY TO GITHUB:
☐ git add .
☐ git commit -m "Release v2.3.0"
☐ git tag -a v2.3.0 -m "Release message"
☐ git push origin main v2.3.0
☐ Verify on GitHub releases page
```

---

## 🆘 TROUBLESHOOTING

### "twine: command not found"
```bash
pip install --upgrade twine
```

### "Invalid or expired authentication credentials"
- Check your token is correct (copy-paste from PyPI website)
- Make sure you entered it as password (not username)
- Username should be exactly: `__token__`

### "File already exists"
This means v2.3.0 was already uploaded. That's fine! You can:
- Upload again (overwrites)
- Or delete from PyPI and re-upload

### Upload succeeds but doesn't appear on PyPI
- Wait 5 minutes (sometimes takes time)
- Refresh page: https://pypi.org/project/bizlens/
- Check spelling of version number

### ".pypirc permission error"
```bash
# Fix permissions on Mac/Linux
chmod 600 ~/.pypirc
```

---

## ⏱️ TIMING

- Create token: 2 minutes
- Build distribution: 2 minutes
- Upload to PyPI: 1 minute
- Verify on PyPI: 2 minutes
- Deploy to GitHub: 2 minutes
- Test installation: 2 minutes

**Total: 10-15 minutes**

---

## 💡 TIPS

1. **One-time token:** Recommended to create a new token for each release
2. **Keep .pypirc safe:** Don't commit it to git (add to .gitignore)
3. **Test in virtual env:** Always test installation in isolated environment
4. **GitHub second:** Always upload to PyPI first, then deploy to GitHub

---

## ✨ NEXT ACTIONS

1. **Create PyPI API token** (Step 1)
2. **Build distribution files** (Step 2)
3. **Upload to PyPI** (Step 4)
4. **Verify on PyPI** (Step 5)
5. **Deploy to GitHub** (Step 6)

**Ready? Start with creating your API token!** 🚀


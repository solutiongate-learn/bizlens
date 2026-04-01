# BizLens Publication Guide 📦

**How to Publish BizLens to PyPI and GitHub**

---

## 📋 Prerequisites

Before publishing, ensure you have:

✅ Completed all testing from TESTING_GUIDE.md
✅ All tests passing
✅ Code reviewed and documented
✅ setup.py and pyproject.toml configured
✅ README and documentation finalized

---

## STEP 1: Prepare Your Local Repository

### 1.1 Initialize Git Repository
```bash
cd /path/to/bizlens

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: BizLens v0.6.0 ENHANCED"

# Create main branch
git branch -M main
```

### 1.2 Create .gitignore
Already provided in `.gitignore` - verify it's there:
```bash
ls -la .gitignore
```

### 1.3 Add License File
```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 Sudhanshu Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "Add MIT License"
```

---

## STEP 2: Configure PyPI Account

### 2.1 Create PyPI Account

1. Go to https://pypi.org
2. Click "Register"
3. Create account with email
4. Verify email address
5. Enable two-factor authentication (recommended)

### 2.2 Create API Token

1. Log in to PyPI
2. Go to Account Settings → API Tokens
3. Create new token:
   - Scope: "Entire account"
   - Name: "BizLens Upload"
4. Copy token (you won't see it again!)

### 2.3 Configure .pypirc File

Create `~/.pypirc` (in your home directory):

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5...  # Your actual token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-...  # Your TestPyPI token (optional)
```

**Security Note**: Protect this file:
```bash
chmod 600 ~/.pypirc
```

---

## STEP 3: Build the Package

### 3.1 Install Build Tools
```bash
pip install build twine wheel
```

### 3.2 Build Distribution
```bash
cd /path/to/bizlens

# Clean any previous builds
rm -rf build/ dist/ *.egg-info

# Build package
python -m build
```

This creates:
- `dist/bizlens-0.6.0.tar.gz` (source)
- `dist/bizlens-0.6.0-py3-none-any.whl` (wheel)

### 3.3 Verify Built Package
```bash
ls -lh dist/
```

Should show:
```
bizlens-0.6.0-py3-none-any.whl (X KB)
bizlens-0.6.0.tar.gz (Y KB)
```

---

## STEP 4: Test Upload to TestPyPI (Recommended)

### 4.1 Upload to TestPyPI
```bash
twine upload --repository testpypi dist/*
```

You should see:
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading bizlens-0.6.0-py3-none-any.whl
Uploading bizlens-0.6.0.tar.gz
```

### 4.2 Test Installation from TestPyPI
```bash
# Create test environment
python -m venv test_pypi_env
source test_pypi_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ bizlens

# Test import
python -c "import bizlens; print('✅ TestPyPI installation works')"

# Deactivate
deactivate
```

### 4.3 View on TestPyPI
Visit: https://test.pypi.org/project/bizlens/

---

## STEP 5: Upload to Production PyPI

### 5.1 Upload to PyPI
```bash
twine upload dist/*
```

You should see:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading bizlens-0.6.0-py3-none-any.whl
Uploading bizlens-0.6.0.tar.gz
```

### 5.2 Verify on PyPI
Visit: https://pypi.org/project/bizlens/

(May take a few minutes to appear)

### 5.3 Test Production Installation
```bash
# Create test environment
python -m venv test_prod_env
source test_prod_env/bin/activate

# Install from PyPI
pip install bizlens

# Test
python -c "import bizlens as bl; df = bl.load_dataset('iris'); bd = bl.BizDesc(df); bd.central_tendency()"

# Should print statistics without errors
```

---

## STEP 6: Setup GitHub Repository

### 6.1 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `bizlens`
3. Description: "Educational Analytics Platform - Descriptive Statistics + Advanced Visualizations"
4. Choose Public or Private
5. Initialize README: No (we have one)
6. Add .gitignore: No (we have one)
7. Add License: No (we have one)
8. Create repository

### 6.2 Add Remote and Push

```bash
cd /path/to/bizlens

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/bizlens.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 6.3 Create Release on GitHub

```bash
# Create annotated tag
git tag -a v0.6.0 -m "Release version 0.6.0 ENHANCED"

# Push tag
git push origin v0.6.0
```

Or on GitHub:
1. Go to Repository → Releases
2. Click "Create a new release"
3. Tag version: `v0.6.0`
4. Release title: "BizLens v0.6.0 ENHANCED"
5. Description: Paste from DELIVERY_SUMMARY.md
6. Upload files from `dist/` (optional)
7. Publish release

---

## STEP 7: Documentation Setup (Optional but Recommended)

### 7.1 Setup GitHub Pages

1. Go to Repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: main
4. Folder: /root (if docs in root) or /docs
5. Save

### 7.2 Add Documentation

Option A: Mkdocs
```bash
pip install mkdocs

# Create docs directory
mkdir docs
cat > docs/index.md << 'EOF'
# BizLens Documentation
See [README](../README_FINAL.md) for more information.
EOF

# Build and deploy
mkdocs build
git add docs/
git commit -m "Add documentation"
git push
```

Option B: Sphinx
```bash
pip install sphinx
sphinx-quickstart docs
```

---

## STEP 8: Post-Publication Tasks

### 8.1 Verify Everything Works

```bash
# Fresh environment
python -m venv verify_env
source verify_env/bin/activate

# Install from PyPI
pip install bizlens

# Run demo
python << 'EOF'
import bizlens as bl

# Load dataset
df = bl.load_dataset('iris')
print(f"✅ Dataset loaded: {df.shape}")

# Create analyzer
bd = bl.BizDesc(df, color_scheme='academic')

# Get statistics
cent_tend = bd.central_tendency()
print("✅ Central tendency calculated")

# Quick visualization test
print("✅ All tests passed!")
EOF

deactivate
```

### 8.2 Create Social Media Post (Optional)

```
🎉 BizLens v0.6.0 is now on PyPI!

Educational analytics platform with:
✅ Distribution visualization with automatic type identification
✅ 15+ integrated sample datasets
✅ 9 visualization types
✅ Professional color schemes

Install: pip install bizlens

GitHub: https://github.com/YOUR_USERNAME/bizlens
PyPI: https://pypi.org/project/bizlens/

Perfect for educators, students, and researchers!

#dataviz #statistics #education #python
```

### 8.3 Update Documentation References

If you have external docs, update links:
- Update GitHub URLs
- Update PyPI URLs
- Update installation instructions
- Update version numbers

---

## TROUBLESHOOTING

### Issue: "twine not found"
```bash
pip install twine
```

### Issue: "Build failed"
```bash
# Clean and retry
rm -rf build/ dist/ *.egg-info
python -m build
```

### Issue: "Authentication failed"
```bash
# Check credentials in ~/.pypirc
# Make sure API token is correct
# Check two-factor authentication settings
```

### Issue: "Package already exists"
```bash
# Update version in setup.py or pyproject.toml
# Rebuild and upload with new version
```

### Issue: "Requirements not installed"
```bash
# Test environment doesn't have dependencies
pip install bizlens[dev]  # Install with dev dependencies
```

---

## CHECKLIST: Before Uploading

- [ ] All tests passing
- [ ] setup.py configured correctly
- [ ] pyproject.toml configured correctly
- [ ] README_FINAL.md is good
- [ ] VERSION is correct (0.6.0)
- [ ] LICENSE file present
- [ ] .gitignore present
- [ ] MANIFEST.in present
- [ ] Built package verified
- [ ] TestPyPI upload successful
- [ ] Fresh environment installation works
- [ ] PyPI account created
- [ ] API token generated
- [ ] .pypirc configured
- [ ] GitHub account ready
- [ ] Repository created
- [ ] Ready to upload!

---

## QUICK REFERENCE: Command Sequence

```bash
# 1. Prepare
cd /path/to/bizlens
git init
git add .
git commit -m "Initial commit: BizLens v0.6.0"

# 2. Build
python -m build

# 3. Test on TestPyPI
twine upload --repository testpypi dist/*
# Test installation from TestPyPI

# 4. Upload to PyPI
twine upload dist/*

# 5. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/bizlens.git
git push -u origin main
git tag -a v0.6.0 -m "Release v0.6.0"
git push origin v0.6.0

# 6. Verify
python -m pip install --upgrade bizlens
python -c "import bizlens; print('✅ Success!')"
```

---

## 🎉 Success!

Your package is now:
- ✅ On PyPI (installable via `pip install bizlens`)
- ✅ On GitHub (source code & issue tracking)
- ✅ Publicly available
- ✅ Ready for the community

**Celebrate! You've published your first package!** 🚀

---

## Maintenance Going Forward

### To Update the Package

1. Make changes to code
2. Update version in setup.py/pyproject.toml
3. Update CHANGELOG
4. Commit: `git commit -m "Update: description"`
5. Tag: `git tag -a v0.6.1 -m "Release v0.6.1"`
6. Build: `python -m build`
7. Upload: `twine upload dist/*`
8. Push: `git push origin main && git push origin v0.6.1`

### Monitor Your Package

- PyPI stats: https://pypi.org/project/bizlens/
- GitHub insights: https://github.com/YOUR_USERNAME/bizlens/insights
- Issues: https://github.com/YOUR_USERNAME/bizlens/issues
- Stars: https://github.com/YOUR_USERNAME/bizlens

---

**Ready to publish? Start with STEP 1!** 📦

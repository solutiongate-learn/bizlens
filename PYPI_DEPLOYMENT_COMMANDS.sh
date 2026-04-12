#!/bin/bash

################################################################################
# BizLens v2.2.16 — PyPI Deployment Commands
# Run these commands in order in your terminal
# Date: April 9, 2026
################################################################################

# STEP 0: PREREQUISITES CHECK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check Python version (must be 3.8+)
python --version

# Check if build and twine are installed
python -m pip list | grep -E "build|twine"

# If build or twine missing, install them:
# python -m pip install build twine

################################################################################
# STEP 1: NAVIGATE TO PROJECT DIRECTORY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd /path/to/bizlens
# OR if you're already in the project, just confirm with:
pwd

################################################################################
# STEP 2: VERIFY VERSION BEFORE BUILD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check that version is 2.2.16 in key files:
echo "=== Checking version in setup.py ==="
grep 'version=' setup.py | head -1

echo "=== Checking version in pyproject.toml ==="
grep 'version =' pyproject.toml | head -1

echo "=== Checking version in __init__.py ==="
grep '__version__' src/bizlens/__init__.py

################################################################################
# STEP 3: CLEAN OLD BUILD ARTIFACTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Remove old build files (important!)
rm -rf build/
rm -rf dist/
rm -rf src/*.egg-info
rm -rf *.egg-info

# Verify they're gone:
ls -la dist/ 2>/dev/null || echo "✅ dist/ directory cleaned"

################################################################################
# STEP 4: BUILD THE DISTRIBUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Build wheel and source distribution
python -m build

# Check that files were created:
echo "=== Build artifacts created ==="
ls -lh dist/

# You should see:
# - bizlens-2.2.16-py3-none-any.whl (wheel)
# - bizlens-2.2.16.tar.gz (source)

################################################################################
# STEP 5: VERIFY BUILD CONTENTS (Optional but Recommended)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check what's in the wheel:
python -m zipfile -l dist/bizlens-2.2.16-py3-none-any.whl | head -20

# Check wheel metadata:
python -m zipfile -e dist/bizlens-2.2.16-py3-none-any.whl /tmp/bizlens_check
cat /tmp/bizlens_check/bizlens-2.2.16.dist-info/METADATA | head -20

################################################################################
# STEP 6a: UPLOAD TO PyPI TESTPYPI (OPTIONAL - TEST FIRST)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# OPTIONAL: Test upload to TestPyPI first (recommended for first-time deployers)
# This lets you verify everything works before uploading to live PyPI

python -m twine upload --repository testpypi dist/bizlens-2.2.16*

# You'll be prompted for username and password (or use .pypirc file)
# If successful, you can test install from TestPyPI:
# pip install --index-url https://test.pypi.org/simple/ bizlens==2.2.16

################################################################################
# STEP 6b: UPLOAD TO PRODUCTION PyPI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# PRODUCTION UPLOAD: This pushes to the real PyPI (users will see this!)
python -m twine upload dist/bizlens-2.2.16*

# Expected output:
# Uploading bizlens-2.2.16-py3-none-any.whl
# Uploading bizlens-2.2.16.tar.gz
# View at: https://pypi.org/project/bizlens/2.2.16/

# ⚠️  IMPORTANT: Enter your PyPI credentials when prompted
# You can also use ~/.pypirc file for authentication (more secure)

################################################################################
# STEP 7: VERIFY UPLOAD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Wait 1-2 minutes, then check PyPI page:
echo "Check PyPI page: https://pypi.org/project/bizlens/2.2.16/"

# OR use curl/wget to check:
curl -s https://pypi.org/pypi/bizlens/2.2.16/json | grep -o '"version":"[^"]*"'

################################################################################
# STEP 8: TEST INSTALLATION FROM PyPI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Fresh install test (use a virtual environment or separate machine if possible)
pip install --upgrade bizlens==2.2.16

# Verify installation:
python -c "import bizlens; print(f'✅ BizLens installed: {bizlens.__version__}')"

# Should output: ✅ BizLens installed: 2.2.16

################################################################################
# STEP 9: VERIFY ALL NOTEBOOKS ARE ACCESSIBLE (Optional)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check GitHub notebooks_v2215 folder content:
curl -s https://api.github.com/repos/solutiongate-learn/bizlens/contents/notebooks_v2215 | \
  grep '"name"' | head -15

################################################################################
# DEPLOYMENT COMPLETE! ✅
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Next step: Deploy to GitHub (run GITHUB_DEPLOYMENT_COMMANDS.sh)

echo "
✅ PyPI DEPLOYMENT COMPLETE!

What to do next:
1. Check https://pypi.org/project/bizlens/2.2.16/
2. Verify: pip install bizlens==2.2.16
3. Deploy to GitHub (see GITHUB_DEPLOYMENT_COMMANDS.sh)

Questions? See:
- DEPLOYMENT_CHECKLIST_v2.2.16.md
- FILE_SYNCHRONIZATION_AUDIT_v2.2.16.md
"

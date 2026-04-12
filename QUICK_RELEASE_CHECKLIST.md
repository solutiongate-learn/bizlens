# BizLens v2.0.0 - Quick Release Checklist

**Quick Reference for Version 2.0.0 Release**  
**Copy & Paste Commands Included**

---

## 🔴 CRITICAL ITEMS (MUST DO FIRST)

### 1. Fix File Permissions (10 min)
```bash
cd "/sessions/festive-nice-fermat/mnt/Package development"

# Remove extended attributes
find src/bizlens -type f -name "*.py" -exec xattr -c {} \;
find tests -type f -name "*.py" -exec xattr -c {} \;

# Set standard permissions
chmod 644 src/bizlens/*.py
chmod 644 tests/*.py
chmod 644 pyproject.toml setup.py

# Verify
ls -la src/bizlens/*.py | grep -v "+" | wc -l  # Should show 12
```
**Verification:** ✓ No + symbols in permissions listing

---

### 2. Clean Notebook Outputs (15 min)
```bash
cd "/sessions/festive-nice-fermat/mnt/Package development"

# Method A: Using Jupyter (Recommended)
pip install jupyter --break-system-packages

for file in notebooks/*.ipynb; do
    jupyter nbconvert --clear-output --inplace "$file"
done

# Verify size reduction
ls -lh notebooks/*.ipynb | head -3

# Method B: If jupyter fails, use Python script
python3 << 'ENDPYTHON'
import json
import os

for fname in os.listdir("notebooks"):
    if fname.endswith(".ipynb"):
        with open(f"notebooks/{fname}", 'r') as f:
            nb = json.load(f)
        for cell in nb.get('cells', []):
            if cell['cell_type'] == 'code':
                cell['outputs'] = []
                cell['execution_count'] = None
        with open(f"notebooks/{fname}", 'w') as f:
            json.dump(nb, f, indent=1)
        print(f"Cleaned: {fname}")
ENDPYTHON
```
**Verification:** ✓ New_Descriptive_Analytics.ipynb < 50 KB

---

### 3. Remove Development Files (5 min)
```bash
cd "/sessions/festive-nice-fermat/mnt/Package development"

# Delete scratch file
rm -f src/bizlens/scratch.py

# Clean caches
rm -rf dist/ build/ *.egg-info
rm -rf .pytest_cache

# Find and remove DS_Store
find . -name '.DS_Store' -delete

# Verify
ls src/bizlens/scratch.py 2>&1  # Should say: No such file
```
**Verification:** ✓ File not found message

---

### 4. Update Version Numbers (10 min)
```bash
cd "/sessions/festive-nice-fermat/mnt/Package development"

# Edit pyproject.toml
# Change: version = "1.0.0" to version = "2.0.0"
sed -i '' 's/version = "1.0.0"/version = "2.0.0"/' pyproject.toml

# Edit setup.py
sed -i '' 's/version="1.0.0"/version="2.0.0"/' setup.py

# Edit __init__.py
sed -i '' 's/__version__ = "1.0.0"/__version__ = "2.0.0"/' src/bizlens/__init__.py

# Verify
grep "2.0.0" pyproject.toml setup.py src/bizlens/__init__.py
```
**Verification:** ✓ All three files show 2.0.0

---

## 🟠 IMPORTANT ITEMS (DO NEXT)

### 5. Update Documentation (15 min)
```bash
cd "/sessions/festive-nice-fermat/mnt/Package development"

# Add to top of CHANGELOG.md:
cat << 'EOF' > CHANGELOG_v2.0.0
## [2.0.0] - 2026-04-19

### Added
- Comprehensive module test coverage (80%+)
- Enhanced docstrings in all public APIs
- Type hints for critical functions
- Troubleshooting guide

### Changed
- Refactored core.py for improved modularity
- Improved data validation in datasets.py
- Enhanced performance in process_mining.py

### Fixed
- Resolved file permission issues
- Cleaned up notebook output artifacts
- Fixed missing docstrings

### Removed
- Temporary development file (scratch.py)
- Old cache files and build artifacts

EOF

# Prepend to existing CHANGELOG.md
cat CHANGELOG_v2.0.0 > CHANGELOG_temp.md && cat CHANGELOG.md >> CHANGELOG_temp.md && mv CHANGELOG_temp.md CHANGELOG.md
rm CHANGELOG_v2.0.0
```
**Verification:** ✓ CHANGELOG.md starts with v2.0.0 entry

---

### 6. Quick Test Validation (20 min)
```bash
cd "/sessions/festive-nice-fermat/mnt/Package development"

# Install test tools
pip install pytest pytest-cov --break-system-packages

# Run tests
pytest tests/ --cov=src/bizlens -q

# Expected: Should see PASSED and coverage % > 80%
```
**Verification:** ✓ Tests pass, coverage reported

---

### 7. Build Package (5 min)
```bash
cd "/sessions/festive-nice-fermat/mnt/Package development"

# Install build tools
pip install build twine --break-system-packages

# Build distribution
python -m build

# Check results
ls -lh dist/
# Expected: 
#   bizlens-2.0.0-py3-none-any.whl (40-50 KB)
#   bizlens-2.0.0.tar.gz (30-40 KB)
```
**Verification:** ✓ Two files in dist/ directory

---

### 8. Validate Package (5 min)
```bash
cd "/sessions/festive-nice-fermat/mnt/Package development"

# Security check
twine check dist/*
# Expected: PASSED

# Check wheel contents
unzip -l dist/bizlens-2.0.0-py3-none-any.whl | grep "bizlens" | head -15
```
**Verification:** ✓ twine check shows PASSED

---

## 🟡 DEPLOYMENT ITEMS

### 9. Test Local Installation (10 min)
```bash
# Create test environment
mkdir /tmp/test_bizlens && cd /tmp/test_bizlens

python3 -m venv test_env
source test_env/bin/activate

# Install wheel
pip install "/sessions/festive-nice-fermat/mnt/Package development/dist/bizlens-2.0.0-py3-none-any.whl"

# Test import
python3 -c "import bizlens; print(f'✅ Version: {bizlens.__version__}')"

# Cleanup
deactivate && cd / && rm -rf /tmp/test_bizlens
```
**Verification:** ✓ Shows "✅ Version: 2.0.0"

---

### 10. Upload to PyPI (5 min)
```bash
cd "/sessions/festive-wise-fermat/mnt/Package development"

# Upload
twine upload dist/bizlens-2.0.0-py3-none-any.whl
twine upload dist/bizlens-2.0.0.tar.gz

# Expected: 100% completion messages

# Wait 5 minutes, then verify
pip install --upgrade bizlens
pip show bizlens
# Should show: Version: 2.0.0
```
**Verification:** ✓ pip show bizlens shows 2.0.0

---

## 🟢 GITHUB RELEASE

### 11. Commit & Tag (10 min)
```bash
cd "/sessions/festive-nice-fermat/mnt/Package development"

# Stage files
git add -A

# Commit
git commit -m "chore: release v2.0.0

- Bump version to 2.0.0
- Remove scratch.py
- Clean notebook outputs
- Fix file permissions
- Enhance test coverage"

# Create tag
git tag -a v2.0.0 -m "Release v2.0.0"

# Push
git push origin main
git push origin --tags
```
**Verification:** ✓ GitHub shows new commits and v2.0.0 tag

---

### 12. Create GitHub Release (5 min)
```bash
# Using GitHub CLI (if installed)
gh release create v2.0.0 \
  --title "Release v2.0.0" \
  --notes-from-file CHANGELOG.md

# OR manually at:
# https://github.com/yourusername/bizlens/releases/new
# Select tag: v2.0.0
# Title: Release v2.0.0
# Copy content from CHANGELOG.md
```
**Verification:** ✓ GitHub Release page shows v2.0.0

---

## 📋 FINAL VERIFICATION CHECKLIST

Complete this before considering release done:

- [ ] All Python files have standard permissions (644)
- [ ] No extended attributes on files
- [ ] scratch.py deleted
- [ ] Notebook outputs cleaned (Descriptive_Analytics.ipynb < 50 KB)
- [ ] Version updated in 3 places (pyproject.toml, setup.py, __init__.py)
- [ ] CHANGELOG.md has v2.0.0 entry at top
- [ ] Tests run successfully (pytest passes)
- [ ] Code coverage ≥ 80%
- [ ] Package builds without errors
- [ ] twine check passes
- [ ] Local installation works
- [ ] PyPI upload successful
- [ ] pip install bizlens==2.0.0 works
- [ ] Git commit created with version bump
- [ ] v2.0.0 tag created
- [ ] GitHub release created

**Total Checks:** 15  
**Required:** All 15 checked before release

---

## 🆘 TROUBLESHOOTING

### Issue: "Resource deadlock avoided" error
**Solution:**
```bash
# Restart system or clear file locks
killall python3
sleep 2
# Try command again
```

### Issue: File permissions still show "+"
**Solution:**
```bash
# Manually remove extended attributes
xattr -l src/bizlens/core.py  # View attributes
xattr -d com.apple.quarantine src/bizlens/core.py  # Remove specific one
xattr -c src/bizlens/core.py  # Clear all
```

### Issue: Notebook too large after cleaning
**Solution:**
```bash
# Manually clear outputs
python3 << 'EOF'
import json
with open('notebooks/notebook.ipynb', 'r') as f:
    nb = json.load(f)
for cell in nb.get('cells', []):
    cell['outputs'] = []
with open('notebooks/notebook.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)
print("Cleaned!")
EOF
```

### Issue: Git tag already exists
**Solution:**
```bash
# Delete local tag
git tag -d v2.0.0

# Delete remote tag (CAREFUL!)
git push origin --delete v2.0.0

# Recreate tag
git tag -a v2.0.0 -m "Release v2.0.0"
git push origin --tags
```

---

## ⏱️ TIME ESTIMATE

| Step | Time |
|------|------|
| Fix permissions & clean | 30 min |
| Update version & docs | 25 min |
| Run tests & build | 30 min |
| Test installation | 15 min |
| PyPI upload | 10 min |
| GitHub release | 15 min |
| **TOTAL** | **2.5 hours** |

---

## 📞 NEXT STEPS

After release is complete:

1. ✅ Announce on GitHub releases page
2. ✅ Monitor for issues first 24 hours
3. ✅ Update any external documentation
4. ✅ Respond to user questions
5. ✅ Plan v2.1 features if needed

---

**Release Date:** April 19-20, 2026  
**Status:** Ready to Execute  
**Complexity:** Moderate (All steps are straightforward)

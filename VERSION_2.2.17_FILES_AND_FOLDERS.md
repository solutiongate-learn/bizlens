# BizLens v2.2.17 Release - Files & Folders for Update

**Current Version:** 2.2.16  
**Target Version:** 2.2.17  
**Date:** April 12, 2026

---

## 📋 Overview

This document identifies all files and folders that need to be modified, reviewed, or regenerated when upgrading from v2.2.16 to v2.2.17 for PyPI and GitHub uploads.

---

## 🔴 CRITICAL FILES - MUST UPDATE (Version Strings)

These files contain hardcoded version numbers that **MUST be changed from `2.2.16` to `2.2.17`**:

### 1. **setup.py** (Root)
- **Location:** `/setup.py`
- **Contains:** `version="2.2.16"`
- **Action:** Update to `version="2.2.17"`
- **Importance:** CRITICAL - PyPI uses this for package version

### 2. **pyproject.toml** (Root)
- **Location:** `/pyproject.toml`
- **Contains:** Version specification (check `version` field)
- **Action:** Update version string to `2.2.17`
- **Importance:** CRITICAL - Modern Python packaging standard

### 3. **src/bizlens/__init__.py**
- **Location:** `/src/bizlens/__init__.py`
- **Contains:** `__version__ = "2.2.16"`
- **Action:** Update to `__version__ = "2.2.17"`
- **Importance:** CRITICAL - Used by `import bizlens; print(bizlens.__version__)`

---

## 📝 DOCUMENTATION FILES - SHOULD UPDATE

These files reference the version and should be updated for consistency:

### 1. **CHANGELOG.md** (Root)
- **Location:** `/CHANGELOG.md`
- **Action:** Add new section for v2.2.17 with release notes
- **Format:**
  ```markdown
  ## [2.2.17] - YYYY-MM-DD
  
  ### Added
  - [List new features]
  
  ### Fixed
  - [List bug fixes]
  
  ### Changed
  - [List changes]
  ```
- **Importance:** HIGH - Users check this for release notes

### 2. **README.md** (Root)
- **Location:** `/README.md`
- **Check for:** Any version-specific references or install instructions
- **Action:** Update if needed (usually just pip install commands don't need version)
- **Importance:** MEDIUM - Installation guide

### 3. **README_V2_RELEASE.md**
- **Location:** `/README_V2_RELEASE.md`
- **Action:** Optional - Update if it references specific versions
- **Importance:** LOW - Release notes document

---

## 📦 SOURCE CODE STRUCTURE (Review for changes)

### Primary Module Files (Check if modified for v2.2.17)
```
src/bizlens/
├── __init__.py              ← Contains __version__
├── core.py                  ← Main functionality
├── datasets.py              ← Dataset handling
├── deploy.py                ← Deployment utilities
├── diagnostic.py            ← Diagnostic tools
├── eda.py                   ← Exploratory Data Analysis
├── inference.py             ← Inference functionality
├── preprocess.py            ← Preprocessing
├── process_mining.py        ← Process mining
├── quality.py               ← Quality checks
├── scratch.py               ← Scratch utilities
├── tables.py                ← Table utilities
└── utils.py                 ← Utility functions
```

**Action:** Review any files you've modified in v2.2.17 development to ensure they're ready for upload.

---

## 🏗️ BUILD & DISTRIBUTION FOLDERS

### **dist/** (Distribution builds)
- **Location:** `/dist/`
- **Contains:** `bizlens-2.2.16.tar.gz`, `bizlens-2.2.16-py3-*.whl`
- **Action before upload:** 
  - **CLEAN this folder** - Delete all old builds
  - **Rebuild fresh** after version update
  - Only commit new v2.2.17 builds to PyPI
- **Importance:** CRITICAL - Old builds must not be uploaded

### **build/** (Build artifacts)
- **Location:** `/build/`
- **Contains:** Temporary build files
- **Action:** Auto-generated, can be deleted before build
- **Importance:** LOW - Regenerated during build

### **bizlens.egg-info/** (Package metadata)
- **Location:** `/src/bizlens.egg-info/` or similar
- **Contains:** PKG-INFO, SOURCES.txt, etc.
- **Action:** Regenerated during build process
- **Importance:** LOW - Regenerated automatically

---

## ✅ VERSION UPDATE COMMAND REFERENCE

### One-line version update (macOS/Linux):
```bash
cd /sessions/dreamy-eloquent-goodall/mnt/Package\ development

# Replace 2.2.16 with 2.2.17 in all critical files
sed -i '' 's/2.2.16/2.2.17/g' src/bizlens/__init__.py setup.py pyproject.toml
```

### Manual verification:
```bash
# Check setup.py
grep "version=" setup.py

# Check pyproject.toml
grep "version" pyproject.toml

# Check __init__.py
grep "__version__" src/bizlens/__init__.py
```

---

## 🔄 BUILD & UPLOAD WORKFLOW

### 1. **Prepare**
- [ ] Update version in 3 critical files (setup.py, pyproject.toml, __init__.py)
- [ ] Update CHANGELOG.md with v2.2.17 release notes
- [ ] Verify all source files are ready (src/bizlens/*.py)

### 2. **Clean Old Builds**
```bash
rm -rf dist/ build/ *.egg-info/
```

### 3. **Rebuild Distribution**
```bash
python setup.py sdist bdist_wheel
```

### 4. **Verify Builds**
```bash
ls -lh dist/  # Should show bizlens-2.2.17.tar.gz and .whl files
```

### 5. **Upload to PyPI**
```bash
twine upload dist/* --verbose
```

### 6. **Upload to GitHub**
```bash
git add .
git commit -m "Release v2.2.17"
git tag v2.2.17
git push origin main v2.2.17
```

---

## 📊 Summary Table

| File/Folder | Type | Priority | Action |
|---|---|---|---|
| setup.py | Configuration | 🔴 CRITICAL | Update `version="2.2.17"` |
| pyproject.toml | Configuration | 🔴 CRITICAL | Update version field |
| src/bizlens/__init__.py | Code | 🔴 CRITICAL | Update `__version__ = "2.2.17"` |
| CHANGELOG.md | Documentation | 🟡 HIGH | Add v2.2.17 section |
| README.md | Documentation | 🟠 MEDIUM | Review & update if needed |
| src/bizlens/*.py | Source Code | 🟠 MEDIUM | Verify recent changes |
| dist/ | Build Output | 🔴 CRITICAL | Clean before rebuild |
| build/ | Build Temp | 🟠 MEDIUM | Auto-generated, not critical |
| .egg-info/ | Metadata | 🟠 MEDIUM | Auto-generated, not critical |

---

## 🎯 Quick Checklist

```
VERSION UPDATE CHECKLIST FOR v2.2.17
=====================================

BEFORE UPLOAD:
☐ Update setup.py (version="2.2.17")
☐ Update pyproject.toml (version = "2.2.17")
☐ Update src/bizlens/__init__.py (__version__ = "2.2.17")
☐ Update CHANGELOG.md with release notes
☐ Review all src/bizlens/*.py files for correctness
☐ Delete old dist/ build files
☐ Rebuild with: python setup.py sdist bdist_wheel
☐ Verify dist/ contains bizlens-2.2.17 files

PYPI UPLOAD:
☐ Run: twine upload dist/*
☐ Verify on https://pypi.org/project/bizlens/

GITHUB UPLOAD:
☐ git add .
☐ git commit -m "Release v2.2.17"
☐ git tag v2.2.17
☐ git push origin main v2.2.17
☐ Verify on GitHub releases page
```

---

## 📞 Notes

- **All version strings must match** for consistency (2.2.17 across all files)
- **CHANGELOG.md is important** - Users check this to understand what's new
- **dist/ folder is critical** - Old builds contaminate PyPI uploads
- **Test locally first** - Install from dist/ wheel before uploading
- **GitHub tags** create formal release points and are important for version tracking


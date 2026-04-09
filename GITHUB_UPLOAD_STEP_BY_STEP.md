# BizLens v2.2.15 - GitHub Upload: Step-by-Step Walkthrough

**Goal:** Push v2.2.15 to GitHub so code is backed up, Colab links work, and users can access notebooks  
**Time Required:** 5-10 minutes  
**Difficulty:** Easy  
**Note:** Do this BEFORE PyPI upload so Colab links are live

---

## **STEP 1: Verify Your Git Setup**

Open Terminal and check if Git is configured:

```bash
# Navigate to your bizlens directory
cd /path/to/bizlens

# Check Git status
git status

# Expected output options:
# Option A: "On branch main" (already initialized)
# Option B: "fatal: not a git repository" (need to initialize)
```

### **If you see "On branch main" → Go to STEP 2**

### **If you see "fatal: not a git repository" → Initialize Git:**

```bash
# Initialize git repository
git init

# Check status
git status

# Now should show: "On branch master" or "main"
```

✅ **Git initialized - proceed to STEP 2**

---

## **STEP 2: Configure Git User (First Time Only)**

Tell Git who you are:

```bash
# Set your name
git config --global user.name "Sudhanshu Singh"

# Set your email
git config --global user.email "cc9n8y8tqc@privaterelay.appleid.com"

# Verify configuration
git config --global user.name
git config --global user.email

# Should show:
# Sudhanshu Singh
# cc9n8y8tqc@privaterelay.appleid.com
```

✅ **User configured - proceed to STEP 3**

---

## **STEP 3: Check Remote Repository**

Verify the GitHub repository is linked:

```bash
# Check remote configuration
git remote -v

# Expected output:
# origin https://github.com/solutiongate-learn/bizlens.git (fetch)
# origin https://github.com/solutiongate-learn/bizlens.git (push)
```

### **If you see the remote → Go to STEP 4**

### **If you don't see the remote → Add it:**

```bash
# Add the GitHub remote
git remote add origin https://github.com/solutiongate-learn/bizlens.git

# Verify it was added
git remote -v

# Should now show the remote URLs
```

✅ **Remote configured - proceed to STEP 4**

---

## **STEP 4: Check What Files Have Changed**

See what's ready to commit:

```bash
# Check status
git status

# Expected output shows files in red (unstaged)
# - src/bizlens/core.py
# - src/bizlens/tables.py
# - src/bizlens/process_mining.py
# - notebooks/... (all 14 notebooks)
# - pyproject.toml
# - README.md
# - ... (all documentation)

# You can also see exact changes:
git diff --stat

# Shows file change counts:
# src/bizlens/core.py | 5 changes
# notebooks/Linear_Regression.ipynb | 50 changes
# ... etc
```

✅ **Understand what's changed - proceed to STEP 5**

---

## **STEP 5: Stage All Files for Commit**

Prepare all changed files:

```bash
# Stage all changes
git add -A

# Verify everything is staged (should be green now)
git status

# Expected output:
# On branch main
# Changes to be committed:
#   modified: src/bizlens/core.py
#   modified: src/bizlens/tables.py
#   modified: src/bizlens/process_mining.py
#   ... (all files)
```

✅ **All files staged - proceed to STEP 6**

---

## **STEP 6: Create Commit with Release Message**

Write a meaningful commit message:

```bash
# Create commit with detailed message
git commit -m "Release v2.2.15: Bug fixes, process mining enhancements, Google Colab support

- Fixed 5 critical bugs (import, unpacking, serialization, rendering, dtype)
- Added 5 new process mining functions (Petri nets, causal nets, Alpha algorithm)
- Added Google Colab support to all 14 notebooks
- Enhanced matplotlib styling across all visualizations
- Updated dependencies: added networkx for graph visualization
- Tested: 166+ code cells executed successfully
- 0 errors in validation
- v2.2.14 → v2.2.15 production release"

# This creates a commit (doesn't push yet!)
# Expected output:
# [main xxxxx] Release v2.2.15: Bug fixes, process mining enhancements...
# 15 files changed, 2500 insertions(+), 100 deletions(-)
```

✅ **Commit created locally - proceed to STEP 7**

---

## **STEP 7: Push to GitHub (First Time - Might Prompt for Auth)**

Send your commits to GitHub:

```bash
# Push to main branch
git push -u origin main

# Expected output:
# Enumerating objects: 25, done.
# Counting objects: 100% (25/25), done.
# Delta compression using up to 8 threads
# Compressing objects: 100% (15/15), done.
# Writing objects: 100% (16/16), 1.2 MiB
# ...
# * [new branch] main -> main
# Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### **If push succeeds → Go to STEP 8**

### **If you get "Permission denied" error:**

You need to authenticate. Choose ONE method:

#### **Method A: Personal Access Token (Recommended - Easiest)**

```bash
# When prompted for password, use token instead:
# Prompt: "Username for 'https://github.com': " → Type: your GitHub username
# Prompt: "Password for 'https://...': " → Paste: your token (not password!)

# Get token: https://github.com/settings/tokens
# - Click "Generate new token"
# - Select scopes: repo (full control)
# - Copy token (starts with ghp_ or similar)
# - Use as password in prompt above
```

Then try push again:
```bash
git push -u origin main
```

#### **Method B: SSH Key (More Secure - Bit More Setup)**

```bash
# 1. Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "cc9n8y8tqc@privaterelay.appleid.com"

# Press Enter 3 times to use defaults
# Creates: ~/.ssh/id_ed25519 and ~/.ssh/id_ed25519.pub

# 2. Add key to SSH agent
ssh-add ~/.ssh/id_ed25519

# 3. Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub

# 4. Add to GitHub: https://github.com/settings/keys
#    - Click "New SSH key"
#    - Paste your public key
#    - Save

# 5. Change remote from HTTPS to SSH
git remote set-url origin git@github.com:solutiongate-learn/bizlens.git

# 6. Try push again
git push -u origin main
```

✅ **Push successful - proceed to STEP 8**

---

## **STEP 8: Create GitHub Release & Tag**

Tag this version in Git for release tracking:

```bash
# Create an annotated tag
git tag -a v2.2.15 -m "BizLens v2.2.15 - Bug fixes, features, Colab support"

# Push the tag to GitHub
git push origin v2.2.15

# Expected output:
# Enumerating objects: 1, done.
# Counting objects: 100% (1/1), done.
# Writing objects: 100% (1/1), 555 bytes
# * [new tag] v2.2.15 -> v2.2.15
```

✅ **Tag created - proceed to STEP 9**

---

## **STEP 9: Verify Files on GitHub Website**

Check that everything uploaded correctly:

```bash
# The URL will be:
# https://github.com/solutiongate-learn/bizlens

# Or open directly:
open https://github.com/solutiongate-learn/bizlens
# Or on Linux: xdg-open https://...
# Or on Windows: start https://...
```

### **On GitHub website, verify:**

✅ **Main branch shows all files**
```
src/bizlens/
├── __init__.py
├── core.py (check it's the fixed version)
├── tables.py (check it's the fixed version)
├── process_mining.py (check for 5 new functions)
... (all 8 modules)

notebooks/
├── Quick_Start_bizlens.ipynb
├── Descriptive_Analytics.ipynb
... (all 14 notebooks)

pyproject.toml, setup.py, LICENSE, README.md, ...
```

✅ **Release tag visible**
- Go to: https://github.com/solutiongate-learn/bizlens/releases
- Should see: "v2.2.15" tag with release date
- Should see commit message

✅ **Commits appear in history**
- Go to: https://github.com/solutiongate-learn/bizlens/commits/main
- Should see your commit: "Release v2.2.15: Bug fixes..."

---

## **STEP 10: Verify Colab Links Work**

Test that notebooks open in Google Colab:

### **Check a notebook file in GitHub:**

1. Go to: https://github.com/solutiongate-learn/bizlens/tree/main/notebooks
2. Click on: `Quick_Start_bizlens.ipynb` (or any notebook)
3. Look for the "Open in Colab" badge (should be visible in the notebook preview)
4. Click the badge → Should open Google Colab

### **Expected Colab Cell 1 (Markdown):**
```
# [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/Quick_Start_bizlens.ipynb)
```

### **Expected Colab Cell 2 (Setup):**
```python
!pip install bizlens>=2.2.15 matplotlib seaborn plotly
```

✅ **Colab links work - GitHub upload complete!**

---

## **STEP 11: Create GitHub Release Page (Optional but Recommended)**

Add nice release notes on the GitHub releases page:

1. Go to: https://github.com/solutiongate-learn/bizlens/releases
2. Click "Create a new release"
3. Fill in:

**Tag version:** `v2.2.15`

**Release title:** `BizLens v2.2.15 - Production Release`

**Description:** (Copy and paste this or from v2.2.15_RELEASE_SUMMARY.md)

```markdown
## 🎉 What's New in v2.2.15

### 🐛 Bug Fixes (5 total)
- Fixed critical import error in core.py (bl.describe() crash)
- Fixed variable unpacking in process_mining.transition_matrix()
- Fixed timedelta serialization in timeline visualization
- Fixed Rich table rendering for integer column names
- Fixed pandas boolean dtype compatibility with statsmodels

### ✨ New Features (5 total)
- Petri net generation and visualization
- Causal net analysis with interactive visualization
- Alpha algorithm for workflow discovery
- Workflow net validation and analysis
- Conformance checking with token replay

### 🚀 Enhancements
- Google Colab support for all 14 notebooks ("Open in Colab" badges)
- Consistent matplotlib styling across all visualizations
- NetworkX integration for graph visualization
- Complete documentation and upload guides

### 📊 Testing & Validation
- 166+ notebook code cells tested
- 0 errors in validation
- All modules and functions verified working
- Colab notebooks tested and working

### 📦 What's Included
- 8 Python modules with 50+ functions
- 14 Jupyter notebooks (all Colab-compatible)
- 9 comprehensive documentation files
- Distribution files (wheel + source)

### 📥 Installation
```bash
pip install bizlens==2.2.15
```

### 📚 Documentation
- See [v2.2.15_RELEASE_SUMMARY.md](./v2.2.15_RELEASE_SUMMARY.md) for detailed changes
- See [COLAB_NOTEBOOKS.md](./COLAB_NOTEBOOKS.md) for all Colab links
- See [CHANGELOG.md](./CHANGELOG.md) for complete changelog

### 🔗 Links
- **GitHub:** https://github.com/solutiongate-learn/bizlens
- **PyPI:** https://pypi.org/project/bizlens/
- **Documentation:** README.md
```

4. Click "Publish release"

✅ **Release page created - beautiful release notes visible!**

---

## **TROUBLESHOOTING**

### **Error: "fatal: not a git repository"**

**Solution:** Initialize Git:
```bash
git init
git config user.name "Sudhanshu Singh"
git config user.email "cc9n8y8tqc@privaterelay.appleid.com"
git add -A
git commit -m "Initial commit"
git remote add origin https://github.com/solutiongate-learn/bizlens.git
git push -u origin main
```

### **Error: "Permission denied (publickey)"**

**Solution:** Use HTTPS instead of SSH:
```bash
git remote set-url origin https://github.com/solutiongate-learn/bizlens.git
git push -u origin main
# Enter token when prompted for password
```

### **Error: "fatal: remote origin already exists"**

**Solution:** Update the existing remote:
```bash
git remote set-url origin https://github.com/solutiongate-learn/bizlens.git
git push -u origin main
```

### **Error: "Your branch is up to date"**

**Reason:** No new commits to push

**Solution:**
```bash
# Check if you have changes
git status

# If nothing to commit, that's OK - you're up to date!
# If you have changes, stage and commit:
git add -A
git commit -m "Your message"
git push origin main
```

### **Can't see Colab badge after pushing**

**Reason:** GitHub cache or notebook refresh

**Solution:**
```bash
# Try viewing raw notebook:
# https://raw.githubusercontent.com/solutiongate-learn/bizlens/main/notebooks/Quick_Start_bizlens.ipynb

# Or wait 1-2 minutes for cache refresh

# Or check that your notebook has badge in first cell:
cat notebooks/Quick_Start_bizlens.ipynb | grep "colab"
```

---

## **QUICK COMMAND SUMMARY**

```bash
# All steps in one command:
cd /path/to/bizlens && \
git config user.name "Sudhanshu Singh" && \
git config user.email "cc9n8y8tqc@privaterelay.appleid.com" && \
git add -A && \
git commit -m "Release v2.2.15: Bug fixes, features, Colab support" && \
git push -u origin main && \
git tag -a v2.2.15 -m "v2.2.15 release" && \
git push origin v2.2.15

# Verify
git remote -v
git tag -l
git log --oneline -5
```

---

## **SUCCESS CHECKLIST**

After completing all steps:

- [ ] Git initialized in project directory
- [ ] User configured (name, email)
- [ ] Remote added: origin → https://github.com/solutiongate-learn/bizlens.git
- [ ] All files staged: `git add -A`
- [ ] Commit created with meaningful message
- [ ] Push to main successful: `git push -u origin main`
- [ ] Tag created: v2.2.15
- [ ] Tag pushed: `git push origin v2.2.15`
- [ ] Files visible on GitHub website
- [ ] v2.2.15 tag visible on releases page
- [ ] Colab badges work in notebooks
- [ ] (Optional) Release page created with release notes

---

## **COMPARISON: PyPI vs GitHub Push**

| Step | PyPI | GitHub |
|------|------|--------|
| **Authentication** | PyPI token | Git credentials (token/SSH) |
| **File preparation** | Build distributions | Stage files (git add) |
| **Verification** | twine check | git status |
| **Upload command** | twine upload | git push |
| **Tagging** | In PyPI metadata | git tag + git push |
| **Verification** | pip install | Clone + verify files |
| **Time** | 2-3 minutes | 2-3 minutes |

**Both follow similar patterns:** Setup → Prepare → Verify → Upload → Confirm

---

## **NEXT: PyPI Upload**

After GitHub push is complete:
1. Wait 1-2 minutes for GitHub to sync
2. Follow `PYPI_UPLOAD_STEP_BY_STEP.md` for PyPI upload
3. Users can then `pip install bizlens==2.2.15`

---

## **FINAL: Announce Release**

Once both GitHub and PyPI are done:
1. Post on relevant channels
2. Update project documentation
3. Share Colab links with users

---

**Ready? Start with Step 1!**

Let me know if you get stuck on any step - I can help troubleshoot.

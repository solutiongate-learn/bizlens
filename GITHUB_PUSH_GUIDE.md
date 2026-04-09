# 📤 How to Push v2.2.15 to GitHub

This guide walks you through pushing all the v2.2.15 updates (new notebooks, Colab support, and bug fixes) to the GitHub repository.

---

## ✅ What's Ready to Push

```
✓ 14 Notebooks (all with Colab badges + setup cells)
  - 1 new: Process_Mining_Foundations.ipynb
  - 13 updated: with Colab support, bug fixes, beautiful formatting

✓ Updated Source Code (v2.2.15)
  - core.py (fixed import)
  - process_mining.py (new Petri net + Alpha functions)
  - tables.py (fixed column names)
  - __init__.py (version bumped to 2.2.15)
  - All dependencies updated (added networkx)

✓ Documentation
  - COLAB_NOTEBOOKS.md (this file)
  - Updated README.md
  - Updated pyproject.toml (v2.2.15 + networkx)
```

---

## 🚀 Step-by-Step GitHub Push

### **Step 1: Open Terminal and Navigate**

```bash
cd ~/Documents/Claude/Package\ development
```

### **Step 2: Initialize Git (if not already a repo)**

```bash
# Check if it's a git repo
git status

# If not, initialize
git init
git remote add origin https://github.com/solutiongate-learn/bizlens.git
git branch -M main
```

### **Step 3: Check What Changed**

```bash
# See all changes
git status

# See detailed changes
git diff --stat
```

### **Step 4: Stage All Changes**

```bash
# Stage everything
git add -A

# Or stage selectively
git add notebooks/
git add src/bizlens/
git add pyproject.toml
git add COLAB_NOTEBOOKS.md
git add README.md
```

### **Step 5: Commit Changes**

```bash
git commit -m "v2.2.15: Add Process Mining Foundations + Colab support

- NEW: Process_Mining_Foundations.ipynb with Petri nets, causal nets, Alpha algorithm
- ENHANCED: All 14 notebooks now have 'Open in Colab' badges
- ADDED: Colab auto-setup cells (pip install, Drive mount)
- FIXED: Import errors in core.py, process_mining.py, tables.py
- FIXED: pandas boolean dtype compatibility with statsmodels
- FIXED: Timedelta serialization in Plotly
- ADDED: networkx dependency for Petri net visualization
- ENHANCED: Beautiful matplotlib theme on all notebooks
- NEW: COLAB_NOTEBOOKS.md with direct Colab links

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

### **Step 6: Push to GitHub**

```bash
# First push (requires GitHub credentials)
git push -u origin main

# Subsequent pushes
git push origin main
```

### **Step 7: Verify on GitHub**

1. Go to: https://github.com/solutiongate-learn/bizlens
2. Verify notebooks folder shows all 14 notebooks
3. Check COLAB_NOTEBOOKS.md renders properly
4. Test one Colab link to ensure it works

---

## 🔐 GitHub Authentication

### **Option A: Personal Access Token (Recommended)**

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `write:packages`
4. Copy the token
5. When prompted for password during push:
   ```
   Username: your-github-username
   Password: [paste-token-here]
   ```

### **Option B: SSH Key**

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to SSH agent
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub:
# Go to Settings → SSH and GPG keys → New SSH key
# Paste contents of ~/.ssh/id_ed25519.pub

# Update remote to use SSH
git remote set-url origin git@github.com:solutiongate-learn/bizlens.git
```

### **Option C: Store Credentials**

```bash
# Configure git to remember credentials (for 15 minutes)
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=900'
```

---

## 📋 Commit Checklist

Before pushing, verify:

- [ ] All 14 notebooks in `notebooks/` folder
- [ ] Each notebook has Colab badge at top
- [ ] Each notebook has setup cell (installs bizlens)
- [ ] `src/bizlens/` has all fixed source files
- [ ] `pyproject.toml` version = 2.2.15
- [ ] `pyproject.toml` includes networkx dependency
- [ ] `COLAB_NOTEBOOKS.md` created
- [ ] No `.pyc` files or `__pycache__` folders
- [ ] No large temporary files

---

## 🔍 Troubleshooting

### **Problem: "permission denied"**
```bash
# Make sure you have push access
git remote -v  # Check if remote is correct
# Contact repo owner if needed
```

### **Problem: "conflict with existing commits"**
```bash
# Pull latest first
git pull origin main
# Then resolve conflicts and push
```

### **Problem: "Large file" warning**
```bash
# Remove large files before pushing
find . -size +50M -exec rm {} \;
git add -A && git commit -m "Remove large files"
```

### **Problem: ".ipynb file is binary"**
```bash
# Git treats notebooks as binary - this is normal
# No action needed, just push
```

---

## ✨ After Push Success

Once pushed, Colab links will be live:

### **Test Colab Access:**
```
https://colab.research.google.com/github/solutiongate-learn/bizlens/blob/main/notebooks/Process_Mining_Foundations.ipynb
```

Try clicking the link → should open in Colab immediately!

### **Update PyPI:**

Once v2.2.15 is on GitHub, upload to PyPI:

```bash
python3 -m twine upload ~/Documents/Claude/Package\ development/bizlens-2.2.15*
```

---

## 📚 Next Steps

1. ✅ Push to GitHub
2. 📤 Upload v2.2.15 to PyPI
3. 🎬 Phase 2: Add animated visualizations (Matplotlib + Plotly)
4. ✍️ Content enrichment: Add theory cells to all notebooks

---

**Questions?** Each Colab link follows this pattern:
```
https://colab.research.google.com/github/{owner}/{repo}/blob/{branch}/{path-to-notebook}
```

For BizLens:
- Owner: `solutiongate-learn`
- Repo: `bizlens`
- Branch: `main`
- Notebooks: `notebooks/*.ipynb`

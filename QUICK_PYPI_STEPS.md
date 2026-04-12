# Quick PyPI Upload - 5 Simple Steps

**Goal:** Upload BizLens v2.3.0 to PyPI

---

## ✅ ANSWER YOUR QUESTION

**"Should I upload to PyPI first?"**

**YES!** Upload to PyPI **first**, then GitHub. Here's why:
- PyPI is the package repository (where users install from)
- GitHub is the source code repository
- Upload to PyPI first, then tag on GitHub
- This way if something goes wrong with GitHub, PyPI is already safe

---

## 🚀 5 SIMPLE STEPS

### STEP 1: Create PyPI Token (2 minutes)

Go to: https://pypi.org/account/tokens/

1. Click **"Add API token"**
2. Name it: `bizlens-release`
3. Scope: **"Entire account"**
4. Click **"Create token"**
5. **Copy the token** (you won't see it again!)

Token looks like: `pypi-AgEIc...xyz`

---

### STEP 2: Build Distribution (2 minutes)

In your Terminal:
```bash
rm -rf dist/ build/ *.egg-info/
python setup.py sdist bdist_wheel
ls -lh dist/
```

You should see:
```
bizlens-2.3.0-py3-none-any.whl
bizlens-2.3.0.tar.gz
```

---

### STEP 3: Upload to PyPI (1 minute)

```bash
twine upload dist/*
```

When prompted:
- **Username:** `__token__`
- **Password:** Paste your token from Step 1

Wait for upload to complete.

---

### STEP 4: Verify on PyPI (2 minutes)

1. Visit: https://pypi.org/project/bizlens/
2. Look for version **2.3.0** in the release history
3. Click on **2.3.0** to see full details

✅ If you see it, your upload was successful!

---

### STEP 5: Deploy to GitHub (2 minutes)

```bash
git add .
git commit -m "Release v2.3.0 to PyPI"
git tag -a v2.3.0 -m "BizLens v2.3.0 - Now on PyPI"
git push origin main v2.3.0
```

Then visit: https://github.com/yourusername/bizlens/releases

You should see the **v2.3.0** tag.

---

## 📋 COPY-PASTE COMMANDS

Ready? Just copy and paste these in order:

```bash
# STEP 2: Build
rm -rf dist/ build/ *.egg-info/
python setup.py sdist bdist_wheel

# STEP 3: Upload (you'll need to paste your token)
twine upload dist/*

# STEP 5: GitHub (after verifying on PyPI)
git add .
git commit -m "Release v2.3.0 to PyPI"
git tag -a v2.3.0 -m "BizLens v2.3.0"
git push origin main v2.3.0
```

---

## 🔑 YOUR TOKEN

**⚠️ You need to:**
1. Go to https://pypi.org/account/tokens/
2. Create new token
3. Copy it (keep it safe!)
4. Use it when prompted for password in twine upload

---

## ⏱️ TOTAL TIME: 10 minutes

- Step 1 (Token): 2 min
- Step 2 (Build): 2 min
- Step 3 (Upload): 1 min
- Step 4 (Verify): 2 min
- Step 5 (GitHub): 2 min

---

## ✨ THAT'S IT!

**Order to do things:**

1. ✅ Create PyPI token
2. ✅ Build distribution
3. ✅ Upload to PyPI
4. ✅ Verify on PyPI website
5. ✅ Deploy to GitHub

**Then BizLens v2.3.0 is released!** 🚀

---

## ❓ QUESTIONS?

**What if upload fails?**
→ See PYPI_UPLOAD_GUIDE_WITH_TOKEN.md for troubleshooting

**Should I test the installation?**
→ Yes! After Step 4, run: `pip install bizlens==2.3.0`

**Can I upload to GitHub first?**
→ You *can*, but PyPI first is better practice

---

**Ready? Start with STEP 1 - create your PyPI token!** 🔑


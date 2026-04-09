# BizLens v2.2.15 - Terminal Commands to Copy & Paste

**Run these commands on YOUR computer in Terminal**, not in Cowork.

---

## 📍 FOLDER LOCATION

First, navigate to where your BizLens project is on YOUR machine:

```bash
# REPLACE /path/to/bizlens with your actual folder
cd /path/to/bizlens
```

**Example:** If your folder is `/Users/sudhanshu/bizlens`, run:
```bash
cd /Users/sudhanshu/bizlens
```

---

## 🔄 STEP 1: GITHUB CONFIGURATION (First Time Only)

**Copy & paste this entire block:**

```bash
git config --global user.name "Sudhanshu Singh"
git config --global user.email "cc9n8y8tqc@privaterelay.appleid.com"
git config --global user.name
```

**Expected output:** Should show `Sudhanshu Singh`

---

## 🔗 STEP 2: ADD GITHUB REMOTE

**Copy & paste this:**

```bash
git remote add origin https://github.com/solutiongate-learn/bizlens.git
git remote -v
```

**Expected output:**
```
origin https://github.com/solutiongate-learn/bizlens.git (fetch)
origin https://github.com/solutiongate-learn/bizlens.git (push)
```

**If you get error "fatal: remote origin already exists":**
```bash
git remote set-url origin https://github.com/solutiongate-learn/bizlens.git
```

---

## 📋 STEP 3: STAGE ALL FILES

**Copy & paste this:**

```bash
git add -A
git status
```

**Expected output:** Should show all files in green as "Changes to be committed"

---

## 💾 STEP 4: CREATE COMMIT

**Copy & paste this entire command:**

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

**Expected output:**
```
[main xxxxx] Release v2.2.15: Bug fixes, process mining...
 15 files changed, 2500 insertions(+), 100 deletions(-)
```

---

## 🚀 STEP 5: PUSH TO GITHUB

**Copy & paste this:**

```bash
git push -u origin main
```

**What happens:**
- First time: May ask for GitHub authentication
- **Username:** Your GitHub username
- **Password:** Your personal access token (NOT your password!)
  - Get token at: https://github.com/settings/tokens
  - Select scope: "repo"

**Expected output:**
```
Enumerating objects: 25, done.
Counting objects: 100% (25/25), done.
...
 * [new branch] main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## 🏷️ STEP 6: CREATE AND PUSH TAG

**Copy & paste this:**

```bash
git tag -a v2.2.15 -m "BizLens v2.2.15 - Bug fixes, features, Colab support"
git push origin v2.2.15
```

**Expected output:**
```
* [new tag] v2.2.15 -> v2.2.15
```

---

## ✅ STEP 7: VERIFY GITHUB PUSH

**Copy & paste this:**

```bash
git log --oneline -5
git tag -l
```

**Expected output:**
- Commit "Release v2.2.15..." at top
- Tag "v2.2.15" in list

---

## 🎉 GITHUB DONE!

**Verify on GitHub website:**
1. Go to: https://github.com/solutiongate-learn/bizlens
2. See all files there? ✅
3. See releases page? ✅

---

---

## 📦 STEP 8: PYPI - BUILD DISTRIBUTIONS

**After GitHub push succeeds, do PyPI.**

**First, in Terminal, still in your bizlens folder:**

```bash
python -m build
```

**Expected output:**
```
Successfully built bizlens-2.2.15-py3-none-any.whl
Successfully built bizlens-2.2.15.tar.gz
```

**Verify files exist:**

```bash
ls -lh dist/bizlens-2.2.15*
```

---

## 🔐 STEP 9: CREATE PYPI TOKEN

**Do this NOW while waiting:**

1. Go to: https://pypi.org/manage/account/
2. Log in (or create account)
3. Click "Create token"
4. Name: `bizlens-v2215`
5. Scope: "Entire account"
6. Click "Create"
7. **COPY the token** (starts with `pypi-`)
8. **SAVE IT** somewhere safe

**⚠️ You won't see it again!**

---

## 📤 STEP 10: UPLOAD TO PYPI

**Copy & paste this:**

```bash
twine upload dist/bizlens-2.2.15*
```

**When prompted:**
- **Username:** `__token__` (exactly this, not your username!)
- **Password:** Paste your token from Step 9

**Expected output:**
```
Uploading bizlens-2.2.15-py3-none-any.whl
100%|████████████| 34.0k/34.0k
Uploading bizlens-2.2.15.tar.gz
100%|████████████| 33.0k/33.0k

View at:
https://pypi.org/project/bizlens/2.2.15/
```

---

## ✔️ STEP 11: VERIFY INSTALLATION

**In a fresh Terminal window:**

```bash
pip install bizlens==2.2.15
python -c "import bizlens; print(f'✅ BizLens v{bizlens.__version__} installed!')"
```

**Expected output:**
```
✅ BizLens v2.2.15 installed!
```

---

## 📋 QUICK REFERENCE

### All Steps at Once (After GitHub):

```bash
# GitHub
cd /path/to/bizlens
git config --global user.name "Sudhanshu Singh"
git config --global user.email "cc9n8y8tqc@privaterelay.appleid.com"
git remote add origin https://github.com/solutiongate-learn/bizlens.git
git add -A
git commit -m "Release v2.2.15: Bug fixes, process mining enhancements, Google Colab support"
git push -u origin main
git tag -a v2.2.15 -m "v2.2.15"
git push origin v2.2.15

# PyPI (after creating token)
python -m build
twine upload dist/bizlens-2.2.15*
# (paste token when prompted)

# Verify
pip install bizlens==2.2.15
python -c "import bizlens; print(bizlens.__version__)"
```

---

## 🆘 TROUBLESHOOTING

### "fatal: not a git repository"
- Make sure you `cd` to your bizlens folder first
- Check with `pwd` - should show your bizlens path

### "Permission denied (publickey)"
- Use HTTPS instead of SSH
- When Git asks for password, paste your personal access token

### "fatal: remote origin already exists"
```bash
git remote set-url origin https://github.com/solutiongate-learn/bizlens.git
```

### "Authentication failed"
- Use `__token__` as username (not your GitHub username)
- Use your personal access token as password (not your account password)

### "pip install hangs"
- Wait 5-10 minutes for PyPI to index
- Then try again

---

## ✨ YOU'RE READY!

1. Copy each command block
2. Paste into Terminal
3. See the output
4. When done, you have v2.2.15 released! 🎉

---

**Questions about any step? Let me know!**

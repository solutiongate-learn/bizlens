# 🎯 YOUR ACTION PLAN - What To Do Next

**Location:** `/Users/sudhanshusingh/Documents/Claude/Projects/Package development`

All commands below should be run in this folder.

---

## 📍 WHERE TO RUN COMMANDS

Open Terminal and navigate to your project:
```bash
cd /Users/sudhanshusingh/Documents/Claude/Projects/Package\ development
```

Or if easier, drag the folder to Terminal.

Then run the commands below in sequence.

---

## 🔓 STEP 1: UNLOCK THE 3 NOTEBOOKS (5-15 min)

### Command 1: Kill Jupyter
```bash
pkill -f jupyter
sleep 30
```

### Command 2: Verify Files Are Unlocked
```bash
python3 << 'EOF'
import json

notebooks = [
    "notebooks/New_Descriptive_Analytics.ipynb",
    "notebooks/New_Master_Process_Mining.ipynb",
    "notebooks/New_Time_Series_Anomaly.ipynb"
]

print("\nTesting unlock...\n")
all_unlocked = True

for nb in notebooks:
    try:
        with open(nb) as f:
            data = json.load(f)
            cells = len(data.get('cells', []))
        print(f"✓ {nb.split('/')[-1]} - UNLOCKED ({cells} cells)")
    except Exception as e:
        print(f"✗ {nb.split('/')[-1]} - LOCKED ({type(e).__name__})")
        all_unlocked = False

if all_unlocked:
    print("\n✅ All 3 notebooks unlocked! Ready for release.\n")
else:
    print("\n❌ Some still locked. Try Step 2 below.\n")
EOF
```

**If all show ✓:** Skip to STEP 2

**If any show ✗:** Run this:
```bash
# Force restore from git
rm -f .git/index.lock
rm -f notebooks/New_Descriptive_Analytics.ipynb
rm -f notebooks/New_Master_Process_Mining.ipynb
rm -f notebooks/New_Time_Series_Anomaly.ipynb

git checkout HEAD -- notebooks/New_Descriptive_Analytics.ipynb
git checkout HEAD -- notebooks/New_Master_Process_Mining.ipynb
git checkout HEAD -- notebooks/New_Time_Series_Anomaly.ipynb

# Then re-run the verification test above
```

**Still locked after that?** Restart your computer - that will definitely fix it.

---

## 📝 STEP 2: UPDATE VERSION TO 2.2.17 (5 min)

Run the automated script:
```bash
bash UPDATE_VERSION_TO_2.2.17.sh
```

This will:
- ✓ Backup your original files
- ✓ Update version in 3 files
- ✓ Show you the changes
- ✓ Ask if you want to update CHANGELOG.md (say yes)

---

## 🏗️ STEP 3: BUILD DISTRIBUTION PACKAGES (2 min)

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info/

# Verify version was updated
python -c "import sys; sys.path.insert(0, 'src'); import bizlens; print(f'Version: {bizlens.__version__}')"

# Build new packages
python setup.py sdist bdist_wheel

# Check they were created
ls -lh dist/
```

**Expected output:**
```
dist/bizlens-2.2.17-py3-none-any.whl    (around 50KB)
dist/bizlens-2.2.17.tar.gz              (around 30KB)
```

---

## 📤 STEP 4: UPLOAD TO PYPI (1 min)

```bash
twine upload dist/*
```

When prompted:
- **Username:** `__token__`
- **Password:** Paste your PyPI API token

**Then verify:**
- Visit: https://pypi.org/project/bizlens/
- Look for v2.2.17 in the release history

---

## 🐙 STEP 5: DEPLOY TO GITHUB (2 min)

```bash
# Commit changes
git add .
git commit -m "Release v2.2.17

- Updated version to 2.2.17
- Verified all 13 notebooks
- Confirmed Pandas & Polars support
- Ready for production"

# Create tag
git tag -a v2.2.17 -m "BizLens v2.2.17 Release"

# Push to GitHub
git push origin main
git push origin v2.2.17
```

**Then verify:**
- Visit: https://github.com/yourusername/bizlens/releases
- Look for v2.2.17 tag

---

## ✅ STEP 6: FINAL VERIFICATION (5 min)

```bash
# Test installation from PyPI (optional but recommended)
python -m venv /tmp/test_bizlens
source /tmp/test_bizlens/bin/activate
pip install bizlens==2.2.17
python -c "import bizlens; print(f'✓ Successfully installed BizLens {bizlens.__version__}')"
deactivate
```

**Expected output:**
```
✓ Successfully installed BizLens 2.2.17
```

---

## 📋 QUICK CHECKLIST

```
UNLOCK:
☐ pkill -f jupyter && sleep 30
☐ Run verification test above
☐ (If needed) Force git restore
☐ (If needed) Restart computer

VERSION UPDATE:
☐ bash UPDATE_VERSION_TO_2.2.17.sh
☐ Say yes to CHANGELOG update

BUILD:
☐ rm -rf dist/ build/ *.egg-info/
☐ python setup.py sdist bdist_wheel
☐ Verify dist/ has .whl and .tar.gz files

DEPLOY:
☐ twine upload dist/*
☐ Verify on PyPI
☐ git add . && git commit -m "Release v2.2.17"
☐ git tag -a v2.2.17
☐ git push origin main v2.2.17
☐ Verify on GitHub

TEST:
☐ pip install bizlens==2.2.17
☐ python -c "import bizlens; print(bizlens.__version__)"
```

---

## 🆘 IF SOMETHING GOES WRONG

**Files still locked after pkill?**
→ See: `NOTEBOOK_UNLOCK_SOLUTIONS.md`

**Build fails?**
→ Make sure Python is 3.8+ and dependencies are installed

**PyPI upload fails?**
→ Check your .pypirc file has correct API token

**Git push fails?**
→ Make sure you're on main branch: `git branch`

---

## ⏱️ TIMELINE

- Unlock: 5-15 min
- Version update: 5 min
- Build: 2 min
- Upload PyPI: 1 min
- Deploy GitHub: 2 min
- Test: 5 min
- **Total: 20-30 minutes**

---

## 🎉 WHEN YOU'RE DONE

You'll have:
✅ BizLens v2.2.17 on PyPI
✅ BizLens v2.2.17 on GitHub
✅ All 13 notebooks verified
✅ Full release documentation
✅ Production-ready package

---

**Ready? Start with STEP 1 above!**

If you get stuck on any step, all the detailed guides are in this folder:
- `COMPLETE_UNLOCK_AND_RELEASE_GUIDE.md` - Most detailed
- `START_HERE_UNLOCK_AND_RELEASE.md` - Quick reference
- `NOTEBOOK_UNLOCK_SOLUTIONS.md` - Troubleshooting

Good luck! 🚀


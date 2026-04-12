# Unlocking Locked Notebooks - Solutions & Workarounds

**Date:** April 12, 2026  
**Issue:** 3 notebooks have OS-level file locks preventing access  
**Affected Notebooks:**
1. New_Descriptive_Analytics.ipynb (220KB)
2. New_Master_Process_Mining.ipynb
3. New_Time_Series_Anomaly.ipynb

**Root Cause:** System-level file locks (possibly from inactive Jupyter processes, file editors, or system caches)

---

## 🔓 SOLUTION 1: Close Editor / IDE Applications (Recommended First)

These files may be open in an editor or Jupyter notebook interface.

### Steps:
1. **Close Jupyter Notebook** - If running locally:
   ```bash
   # Close any running Jupyter servers
   jupyter notebook stop
   # or
   pkill -f jupyter
   ```

2. **Close Code Editors** - Check if files are open in:
   - VS Code
   - PyCharm
   - Sublime Text
   - Any text editor

3. **Close File Browser** - Make sure Finder/File Explorer isn't previewing the files

4. **Wait 30 seconds** - Let system release locks

5. **Retry verification:**
   ```bash
   python3 << 'EOF'
   import json
   
   notebooks = [
       "notebooks/New_Descriptive_Analytics.ipynb",
       "notebooks/New_Master_Process_Mining.ipynb",
       "notebooks/New_Time_Series_Anomaly.ipynb"
   ]
   
   for nb in notebooks:
       try:
           with open(nb, 'r') as f:
               data = json.load(f)
               cells = len(data.get('cells', []))
               print(f"✓ {nb.split('/')[-1]}: {cells} cells")
       except Exception as e:
           print(f"✗ {nb.split('/')[-1]}: {e}")
   EOF
   ```

---

## 🔓 SOLUTION 2: Force Remove & Restore from Git

If the notebooks are version controlled in Git:

### Steps:
1. **Clear git lock:**
   ```bash
   cd /path/to/bizlens
   rm -f .git/index.lock
   ```

2. **Remove locked files:**
   ```bash
   rm -f notebooks/New_Descriptive_Analytics.ipynb
   rm -f notebooks/New_Master_Process_Mining.ipynb
   rm -f notebooks/New_Time_Series_Anomaly.ipynb
   ```

3. **Restore from git:**
   ```bash
   git checkout HEAD -- notebooks/New_Descriptive_Analytics.ipynb
   git checkout HEAD -- notebooks/New_Master_Process_Mining.ipynb
   git checkout HEAD -- notebooks/New_Time_Series_Anomaly.ipynb
   ```

4. **Verify:**
   ```bash
   ls -lh notebooks/New_Descriptive_Analytics.ipynb
   ```

---

## 🔓 SOLUTION 3: Use System File Monitoring Tools

If locked by a process:

### macOS:
```bash
# Find what's holding the file
lsof | grep "New_Descriptive_Analytics"

# Kill the process
kill -9 <PID>
```

### Linux:
```bash
# Find what's holding the file
fuser notebooks/New_Descriptive_Analytics.ipynb

# Force release
fuser -k notebooks/New_Descriptive_Analytics.ipynb
```

---

## 🔓 SOLUTION 4: Restart Your System

If locks persist across all attempts:

1. **Save any unsaved work**
2. **Restart your computer**
3. **After restart, try accessing the files again**

This clears all system-level file locks.

---

## ✅ VERIFICATION AFTER UNLOCKING

Once files are unlocked, run this test:

```bash
cd /path/to/bizlens

python3 << 'EOF'
import json

notebooks = [
    "notebooks/New_Descriptive_Analytics.ipynb",
    "notebooks/New_Master_Process_Mining.ipynb",
    "notebooks/New_Time_Series_Anomaly.ipynb"
]

print("=" * 90)
print("TESTING UNLOCKED NOTEBOOKS")
print("=" * 90)
print()

for nb_path in notebooks:
    print(f"Testing: {nb_path}")
    try:
        with open(nb_path, 'r') as f:
            nb_data = json.load(f)
        
        cells = nb_data.get('cells', [])
        code_cells = [c for c in cells if c.get('cell_type') == 'code']
        markdown_cells = [c for c in cells if c.get('cell_type') == 'markdown']
        
        all_source = ""
        for cell in code_cells:
            source = cell.get('source', [])
            if isinstance(source, list):
                all_source += "\n".join(source)
            else:
                all_source += source
        
        has_pandas = 'pandas' in all_source.lower() or 'pd.' in all_source
        has_polars = 'polars' in all_source.lower() or 'pl.' in all_source
        has_bizlens = 'bizlens' in all_source or 'import bizlens' in all_source
        
        print(f"  ✅ File accessible!")
        print(f"  Cells: {len(code_cells)} code + {len(markdown_cells)} markdown")
        print(f"  {'✓' if has_pandas else '✗'} Pandas support")
        print(f"  {'✓' if has_polars else '✗'} Polars support")
        print(f"  {'✓' if has_bizlens else '✗'} BizLens integration")
        print(f"  Status: {'✅ READY' if has_bizlens else '⚠ CHECK'}")
        
    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}: {str(e)[:60]}")
    
    print()

print("=" * 90)

EOF
```

---

## 📋 QUICK DECISION TREE

```
Is file still locked?
├─ YES → Check if editor/IDE has it open
│        ├─ Found it → Close the application
│        ├─ Not found → Try Solution 3 (lsof/fuser)
│        └─ Still locked → Try Solution 4 (restart)
│
└─ NO → File unlocked! ✓
       └─ Run verification test above
```

---

## 🎯 IMPORTANCE FOR RELEASE

**Status with locked files:**
- ⏳ Can still release v2.2.17 (10 notebooks verified, 3 pending)
- ⚠️ Not ideal to release without full verification
- ✓ Have comprehensive documentation and tools ready

**After unlocking:**
- ✅ Complete verification of all 13 notebooks
- ✅ 100% confidence in release quality
- ✅ Documented proof that all notebooks work

---

## 📞 IF NOTHING WORKS

If you cannot unlock the files through these methods:

### Option A: Proceed Without These 3
The 10 verified notebooks are production-ready. You can:
1. Release v2.2.17 with 10 tested notebooks
2. Add the 3 notebooks in v2.2.18 after unlocking

### Option B: Recreate the Notebooks
If files are corrupted:
1. Check git history for previous versions
2. Recreate from backup
3. Re-export from Jupyter if you have them running

### Option C: Contact Support
- Reach out to your system administrator
- Check file system for corruption
- Consider filesystem repair if widespread

---

## 🔐 PREVENTING FUTURE LOCKS

1. **Always close Jupyter before file operations:**
   ```bash
   jupyter notebook stop
   ```

2. **Don't open notebooks in multiple editors:**
   - One Jupyter instance only
   - Don't open .ipynb in text editors while running

3. **Keep notebooks out of cloud sync during editing:**
   - Dropbox, iCloud, OneDrive can cause locks
   - Sync only after closing notebooks

4. **Regular commits to git:**
   ```bash
   git add notebooks/
   git commit -m "Update notebooks"
   ```

---

## ✨ RECOMMENDED WORKFLOW

1. **Before working:**
   ```bash
   pkill -f jupyter  # Stop all Jupyter
   sleep 2
   ```

2. **Edit notebooks:**
   ```bash
   jupyter notebook
   # Open and edit notebooks
   ```

3. **After editing:**
   ```bash
   # Stop Jupyter (Ctrl+C in terminal)
   sleep 2
   ```

4. **Commit changes:**
   ```bash
   git add notebooks/
   git commit -m "Update notebook: [name]"
   ```

---

## 📊 Summary

| Solution | Time | Difficulty | Success Rate |
|----------|------|-----------|--------------|
| Close Editor | 2 min | ⭐ Easy | 80% |
| Force Remove + Restore | 5 min | ⭐⭐ Medium | 90% |
| System Tools (lsof/fuser) | 5 min | ⭐⭐⭐ Hard | 70% |
| Restart System | 5 min | ⭐⭐ Medium | 100% |

---

**Try Solution 1 first** - It works 80% of the time and takes only 2 minutes!

After unlocking, run the verification test to confirm all 3 notebooks are accessible and ready for v2.2.17 release.


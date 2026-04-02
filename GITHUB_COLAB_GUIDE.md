# BizLens v2.2.11 - GitHub & Google Colab Integration Guide

## Quick Start: Open Notebooks in Colab (3 clicks!)

After pushing to GitHub, use these Colab links (replace `YOUR_USERNAME`):

- **[Quick Start (5 min)](https://colab.research.google.com/github/YOUR_USERNAME/bizlens/blob/main/notebooks/01_Quick_Start_Colab.ipynb)**
- **[Descriptive Analytics (15 min)](https://colab.research.google.com/github/YOUR_USERNAME/bizlens/blob/main/notebooks/02_Descriptive_Analytics_Colab.ipynb)**
- **[Process Mining (15 min)](https://colab.research.google.com/github/YOUR_USERNAME/bizlens/blob/main/notebooks/03_Process_Mining_Colab.ipynb)**
- **[Statistical Inference (20 min)](https://colab.research.google.com/github/YOUR_USERNAME/bizlens/blob/main/notebooks/04_Statistical_Inference_Colab.ipynb)**

## Three Ways to Use

### Option 1: Direct Colab Links (Easiest)
Modify template above with your GitHub username and click

### Option 2: Via Colab UI
1. Go to https://colab.research.google.com/
2. Click "GitHub" tab
3. Type: `YOUR_USERNAME/bizlens`
4. Select notebook from list

### Option 3: Local Jupyter
```bash
pip install bizlens jupyterlab
jupyter lab notebooks/01_Quick_Start_Colab.ipynb
```

## Notebook Overview

| # | Notebook | Duration | Topics |
|---|----------|----------|--------|
| 1 | Quick Start | 5 min | Overview, basics, quality checks |
| 2 | Descriptive | 15 min | Tables, distributions, analysis |
| 3 | Process Mining | 15 min | Event logs, workflows, bottlenecks |
| 4 | Inference | 20 min | Hypothesis testing, ANOVA, correlation |

## GitHub Setup

### Push Notebooks
```bash
cd /path/to/bizlens
git add notebooks/
git add GITHUB_COLAB_GUIDE.md
git add GITHUB_PUSH_INSTRUCTIONS.md
git add COLAB_*.md IMMEDIATE_ACTION_ITEMS.txt
git commit -m "feat: Add Colab notebooks for v2.2.11"
git push origin main
```

### Verify Links Work
1. Replace YOUR_USERNAME in links above
2. Click each link in browser
3. Notebook should open in Colab

## Installation

### In Colab (Automatic)
```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "bizlens"])
```

### Local Python
```bash
pip install bizlens
pip install bizlens==2.2.11  # Specific version
```

## Sharing

### Markdown for README
```markdown
## Try BizLens in Google Colab

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/bizlens/blob/main/notebooks/01_Quick_Start_Colab.ipynb)

- [Quick Start (5 min)](...)
- [Descriptive Analytics (15 min)](...)
- [Process Mining (15 min)](...)
- [Statistical Inference (20 min)](...)
```

### Social Media
"🎓 BizLens v2.2.11 - Learn in Google Colab (no install needed!)
✅ 4 interactive tutorials
✅ Free GPU compute
✅ 5-20 minute lessons
Quick Start: [YOUR_LINK]"

## FAQ

**Q: Can I edit notebooks in Colab?**
A: Yes! Download and push to Git to save changes.

**Q: Do I need to install BizLens first?**
A: No! First code cell auto-installs everything.

**Q: Can non-programmers use these?**
A: Yes! Just click link, run cells in order.

**Q: What if I see "Module not found"?**
A: Run first code cell (pip install) and wait.

**Q: Can I use offline?**
A: Download notebook and run locally with Jupyter.

## Support

- **User Guide:** See comprehensive GITHUB_COLAB_GUIDE.md
- **Deployment:** See GITHUB_PUSH_INSTRUCTIONS.md
- **Quick Ref:** See COLAB_QUICK_REFERENCE.md
- **Actions:** See IMMEDIATE_ACTION_ITEMS.txt

---

For detailed instructions, see the comprehensive documentation files included in your repo.

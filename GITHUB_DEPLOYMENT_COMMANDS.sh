#!/bin/bash

################################################################################
# BizLens v2.2.16 — GitHub Deployment Commands
# Run these AFTER PyPI deployment
# Date: April 9, 2026
################################################################################

# STEP 1: VERIFY GIT STATUS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Navigate to your bizlens git repository
cd /path/to/bizlens

# Check current branch (should be 'main')
git branch

# Show status (should show modified files)
git status

# You should see modified files like:
# - setup.py
# - pyproject.toml
# - src/bizlens/__init__.py
# - src/bizlens/core.py
# - ... (other modules)
# - CHANGELOG.md

################################################################################
# STEP 2: VERIFY REMOTE IS CORRECT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check your remote URL:
git remote -v

# Should show something like:
# origin  https://github.com/solutiongate-learn/bizlens.git (fetch)
# origin  https://github.com/solutiongate-learn/bizlens.git (push)

# If remote is wrong, update it:
# git remote set-url origin https://github.com/solutiongate-learn/bizlens.git

################################################################################
# STEP 3: PULL LATEST CHANGES (if working with others)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Get latest from remote to avoid conflicts:
git pull origin main

################################################################################
# STEP 4: ADD ALL MODIFIED FILES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Add source code changes
git add src/bizlens/

# Add configuration files
git add setup.py
git add pyproject.toml

# Add notebooks (v2215 folder)
git add notebooks_v2215/

# Add documentation
git add CHANGELOG.md
git add DEPLOYMENT_CHECKLIST_v2.2.16.md
git add FILE_SYNCHRONIZATION_AUDIT_v2.2.16.md
git add FINAL_STATUS_REPORT_v2.2.16.txt
git add PYPI_DEPLOYMENT_COMMANDS.sh
git add GITHUB_DEPLOYMENT_COMMANDS.sh

# Verify what will be committed:
git status

################################################################################
# STEP 5: CREATE COMMIT WITH DETAILED MESSAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create a detailed commit message
git commit -m "BizLens v2.2.16: hotfix for v2.2.15 bugs + complete notebooks

CRITICAL FIXES:
- Fix catastrophic bug in diagnostic.py (AI chat response removed)
- Implement 3 missing diagnostic methods (duplicate_analysis, data_type_consistency, cardinality_analysis)
- Unify version strings across all files (setup.py, pyproject.toml, all modules)

NEW CONTENT:
- Complete 8 empty notebooks with full analysis code
- 13 notebooks now fully functional (287 cells, 141 code cells)
- All notebooks at v2.2.16

DOCUMENTATION:
- Update CHANGELOG.md with v2.2.16 entry + deprecation notice for v2.2.15
- Add DEPLOYMENT_CHECKLIST_v2.2.16.md
- Add FILE_SYNCHRONIZATION_AUDIT_v2.2.16.md
- Add deployment command scripts

BREAKING CHANGES:
- None

DEPRECATIONS:
- v2.2.15 marked as buggy, users should upgrade to v2.2.16

Co-Authored-By: Claude AI <noreply@anthropic.com>"

################################################################################
# STEP 6: PUSH TO MAIN BRANCH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Push commits to main branch
git push origin main

# Expected output:
# Counting objects: ...
# Writing objects: ...
# main ... -> main

################################################################################
# STEP 7: CREATE GIT TAG FOR v2.2.16
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Create lightweight tag:
git tag v2.2.16

# OR create annotated tag with message (recommended):
git tag -a v2.2.16 -m "BizLens v2.2.16: Hotfix release for v2.2.15

Critical bugs fixed:
- diagnostic.py catastrophic bug removed
- 3 missing diagnostic methods implemented
- Version string synchronization

All 13 notebooks now complete with full analysis code.

See CHANGELOG.md for complete details."

# Verify tag was created:
git tag -l v2.2.16
git show v2.2.16

################################################################################
# STEP 8: PUSH TAG TO GITHUB
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Push the tag to remote
git push origin v2.2.16

# Expected output:
# Total 0 (delta 0), reused 0 (delta 0)
# To https://github.com/solutiongate-learn/bizlens.git
#  * [new tag]         v2.2.16 -> v2.2.16

################################################################################
# STEP 9: CREATE GITHUB RELEASE (Optional but Recommended)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Using GitHub CLI (if installed):
gh release create v2.2.16 \
  --title "BizLens v2.2.16 — Hotfix Release" \
  --notes "
## Critical Fixes
- Removed catastrophic bug from diagnostic.py (AI chat response)
- Implemented 3 missing diagnostic methods
- Unified version strings across all files

## What's New
- All 13 notebooks now complete with full analysis code (287 cells, 141 code cells)
- Comprehensive deployment documentation added

## Important Notes
- **v2.2.15 is deprecated** — contains bugs, upgrade immediately
- No breaking changes in this release
- All dependencies current and compatible

## Installation
\`\`\`bash
pip install --upgrade bizlens==2.2.16
\`\`\`

## Full Details
See CHANGELOG.md for complete list of changes
"

# OR create release manually on GitHub:
# 1. Go to https://github.com/solutiongate-learn/bizlens/releases
# 2. Click "Draft a new release"
# 3. Select tag v2.2.16
# 4. Copy content from CHANGELOG.md v2.2.16 section

################################################################################
# STEP 10: VERIFY DEPLOYMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check GitHub page:
echo "Check GitHub: https://github.com/solutiongate-learn/bizlens/releases/tag/v2.2.16"

# Or use GitHub CLI:
gh release view v2.2.16

# Check that commits are visible:
gh repo view solutiongate-learn/bizlens --web

################################################################################
# FINAL VERIFICATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo "
✅ GITHUB DEPLOYMENT COMPLETE!

Verify:
1. PyPI: https://pypi.org/project/bizlens/2.2.16/
2. GitHub: https://github.com/solutiongate-learn/bizlens/releases/tag/v2.2.16
3. Install: pip install --upgrade bizlens==2.2.16

Done! v2.2.16 is now live on both PyPI and GitHub.
"
